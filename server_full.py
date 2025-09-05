#!/usr/bin/env python3
"""
Full server-side API for Payment Vector Testing.
Runs on server with AI service + Elasticsearch.
Receives query → normalizes → vectorizes → searches → returns results.
"""
import sys
import os
import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Payment Vector Testing - Search API",
    description="Server-side API: Query → Normalize → Vectorize → Search → Results",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for services
es_client = None
ai_processor = None
data_normalizer = None

# Pydantic models
class SearchQuery(BaseModel):
    query: str
    limit: int = Field(default=10, ge=1, le=100)
    threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    index_type: str = Field(default="both", pattern="^(payments|sanctions|both)$")

class SearchResult(BaseModel):
    success: bool
    query: str
    normalized_query: str
    language: str
    embeddings_length: int
    results: List[Dict[str, Any]]
    total: int
    processing_time: float
    server_info: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    elasticsearch: Dict[str, Any]
    ai_service: Dict[str, Any]
    indices: Dict[str, Any]
    timestamp: datetime

class IndexRequest(BaseModel):
    """Index document request."""
    index: str = Field(..., description="Index name")
    document: dict = Field(..., description="Document to index")
    doc_id: Optional[str] = Field(None, description="Optional document ID")
    routing: Optional[str] = Field(None, description="Optional routing key for parent-child")
    
    class Config:
        arbitrary_types_allowed = True

# Dependency to get services
async def get_services():
    """Get initialized services."""
    global es_client, ai_processor, data_normalizer
    
    if es_client is None:
        raise HTTPException(status_code=503, detail="Elasticsearch service not initialized")
    
    return {
        "es_client": es_client,
        "ai_processor": ai_processor,
        "data_normalizer": data_normalizer
    }

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global es_client, ai_processor, data_normalizer
    
    try:
        logger.info("Initializing server services...")
        
        # Force Elasticsearch host for Docker environment
        es_host = os.getenv('ELASTICSEARCH_HOST', 'elasticsearch')
        es_port = int(os.getenv('ELASTICSEARCH_PORT', '9200'))
        
        logger.info(f"ELASTICSEARCH_HOST: {es_host}")
        logger.info(f"ELASTICSEARCH_PORT: {es_port}")
        
        # Initialize Elasticsearch with direct connection
        from elasticsearch import Elasticsearch
        es_client_direct = Elasticsearch(
            hosts=[f"http://{es_host}:{es_port}"],
            verify_certs=False
        )
        
        # Test connection
        info = es_client_direct.info()
        logger.info(f"✅ Connected to Elasticsearch: {info['version']['number']}")
        
        # Create wrapper client
        from src.es_client.client import ElasticsearchClient
        es_client = ElasticsearchClient.__new__(ElasticsearchClient)
        es_client.client = es_client_direct
        
        # Initialize AI services (graceful fallback if not available)
        try:
            from src.ai_integration import AIProcessor, DataNormalizer
            ai_processor = AIProcessor()
            data_normalizer = DataNormalizer(ai_processor)

            # Quick runtime self-test – ensure the processor can handle a simple text.
            try:
                test_result = await ai_processor.process_text(
                    text="healthcheck",
                    generate_embeddings=False,
                    generate_variants=False
                )
                if not test_result.get("success", False):
                    raise RuntimeError("AI processor self-test failed")
            except Exception as ai_e:
                logger.warning(f"AI processor failed self-test: {ai_e}. Switching to stub implementation.")
                from src.ai_integration.ai_stub import (
                    AIProcessor as AIProcessorStub,
                    DataNormalizer as DataNormalizerStub,
                )
                ai_processor = AIProcessorStub()
                data_normalizer = DataNormalizerStub(ai_processor)
                logger.info("✅ Stub AI services initialized successfully (self-test fallback)")

            else:
                logger.info("✅ AI services initialized successfully and passed self-test")
        except Exception as e:
            logger.warning(f"AI services unavailable: {e}")
            logger.info("API will work with limited functionality (no AI processing)")
            from src.ai_integration.ai_stub import AIProcessor as AIProcessorStub, DataNormalizer as DataNormalizerStub
            ai_processor = AIProcessorStub()
            data_normalizer = DataNormalizerStub(ai_processor)
            logger.info("✅ Stub AI services initialized successfully")
        
        logger.info("✅ All available services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Payment Vector Testing API", 
        "status": "running",
        "features": {
            "elasticsearch": es_client is not None,
            "ai_processing": ai_processor is not None,
            "normalization": data_normalizer is not None
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        health_info = {
            "status": "healthy",
            "elasticsearch": {"connected": False},
            "ai_service": {"status": "unavailable"},
            "indices": {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Check Elasticsearch
        if es_client:
            try:
                es_info = es_client.client.info()
                cluster_health = es_client.client.cluster.health()
                health_info["elasticsearch"] = {
                    "connected": True,
                    "version": es_info['version']['number'],
                    "cluster": es_info['cluster_name'],
                    "status": cluster_health['status']
                }
                
                # Check indices
                try:
                    from config.config import config
                    health_info["indices"] = {
                        "sanctions": es_client.index_exists("sanctions"),
                        "payment_vectors": es_client.index_exists(config.vector.index_name)
                    }
                except:
                    health_info["indices"] = {"error": "Could not check indices"}
                    
            except Exception as e:
                health_info["elasticsearch"]["error"] = str(e)
                health_info["status"] = "unhealthy"
        
        # Check AI service
        if ai_processor:
            health_info["ai_service"] = {"status": "available"}
        
        return health_info
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

@app.post("/search")
async def search(
    query: SearchQuery,
    services: dict = Depends(get_services)
):
    """
    Main search endpoint:
    1. Receive query (e.g., "Петро Порошенко")
    2. Normalize and vectorize with AI (if available)
    3. Search in Elasticsearch
    4. Return results
    """
    try:
        start_time = datetime.now()
        
        logger.info(f"Processing search query: '{query.query}'")
        
        es_client = services["es_client"]
        ai_processor = services["ai_processor"]
        
        results = []
        query_vector = None
        normalized_query = query.query
        language = "unknown"
        
        # Step 1: AI Processing (if available)
        if ai_processor:
            try:
                ai_result = await ai_processor.process_text(
                    text=query.query,
                    generate_embeddings=True,
                    generate_variants=True
                )
                
                logger.info(f"AI result: {ai_result}")
                if ai_result["success"]:
                    # Flatten embeddings if shape is [1, D] or already [D]
                    emb = ai_result.get("embeddings", [])
                    if isinstance(emb, list):
                        if len(emb) == 1 and isinstance(emb[0], list):
                            query_vector = emb[0]
                        elif emb and isinstance(emb[0], (int, float)):
                            query_vector = emb
                        else:
                            logger.warning(f"Embeddings shape not usable for kNN: {type(emb)} length={len(emb)}")
                            query_vector = None
                    else:
                        query_vector = None
                    normalized_query = ai_result.get("normalized_text", query.query)
                    language = ai_result.get("language", "unknown")
                    
                    logger.info(f"Query normalized: '{normalized_query}' (language: {language})")
                    if query_vector:
                        logger.info(f"Generated vector of length: {len(query_vector)}")
                else:
                    logger.warning(f"AI processing failed: {ai_result.get('error', 'Unknown error')}")
                    logger.warning(f"Full AI result: {ai_result}")
            except Exception as e:
                logger.warning(f"AI processing error: {e}")
        
        # Step 2: Search in Elasticsearch
        if query_vector and query.index_type in ["sanctions", "both"]:
            # Vector search in sanctions
            try:
                sanctions_search = {
                    "knn": {
                        "field": "vector",
                        "query_vector": query_vector,
                        "k": query.limit,
                        "num_candidates": max(query.limit * 10, 50)
                    },
                    "min_score": query.threshold
                }
                
                sanctions_results = es_client.search(
                    index_name="sanctions",
                    query=sanctions_search,
                    size=query.limit
                )
                
                for hit in sanctions_results.get("hits", {}).get("hits", []):
                    results.append({
                        "id": hit["_id"],
                        "score": hit["_score"],
                        "source": hit["_source"],
                        "index": "sanctions"
                    })
                    
            except Exception as e:
                logger.warning(f"Sanctions search failed: {e}")
            
            # Optional: script_score using variant vectors (best-effort; guarded)
            try:
                # Use companion variants index for kNN
                variant_knn = {
                    "knn": {
                        "field": "vector",
                        "query_vector": query_vector,
                        "k": query.limit,
                        "num_candidates": max(query.limit * 10, 50)
                    }
                }
                variant_scores = es_client.search(index_name="sanctions_variants", query=variant_knn, size=query.limit)
                for hit in variant_scores.get("hits", {}).get("hits", []):
                    parent_id = hit.get("_source", {}).get("parent_id")
                    if not parent_id:
                        continue
                    # Avoid duplicates by parent id
                    if any(r["id"] == parent_id for r in results):
                        continue
                    # Fetch parent doc from sanctions
                    try:
                        parent = es_client.client.get(index="sanctions", id=parent_id)
                        results.append({
                            "id": parent_id,
                            "score": hit.get("_score", 0.0),
                            "source": parent.get("_source", {}),
                            "index": "sanctions"
                        })
                    except Exception as ge:
                        logger.info(f"Failed to fetch parent {parent_id}: {ge}")
            except Exception as e:
                logger.info(f"Variant vector kNN skipped: {e}")

            # Parent-child index kNN (sanctions_pc), on children (variant docs) with routing
            try:
                pc_knn = {
                    "knn": {
                        "field": "vector",
                        "query_vector": query_vector,
                        "k": query.limit,
                        "num_candidates": max(query.limit * 10, 50)
                    },
                    "query": {
                        "term": {"doc_rel": "variant"}
                    }
                }
                pc_scores = es_client.search(index_name="sanctions_pc", query=pc_knn, size=query.limit)
                for hit in pc_scores.get("hits", {}).get("hits", []):
                    parent_id = hit.get("_routing") or hit.get("fields", {}).get("_routing")
                    # Fetch parent via routing
                    if not parent_id:
                        continue
                    if any(r["id"] == parent_id for r in results):
                        continue
                    try:
                        parent = es_client.client.get(index="sanctions_pc", id=parent_id, routing=parent_id)
                        results.append({
                            "id": parent_id,
                            "score": hit.get("_score", 0.0),
                            "source": parent.get("_source", {}),
                            "index": "sanctions_pc"
                        })
                    except Exception as ge:
                        logger.info(f"Failed to fetch PC parent {parent_id}: {ge}")
            except Exception as e:
                logger.info(f"Parent-child kNN skipped: {e}")
        
        # Fallback: text search if no vector or additional results needed
        if len(results) < query.limit:
            try:
                # Combine multi_match across top-level fields with nested variants.text
                should_clauses = [
                    {"multi_match": {
                        "query": normalized_query,
                        "fields": ["name", "name_en", "name_ru", "entity_type", "source"],
                        "fuzziness": "AUTO"
                    }},
                    {"nested": {
                        "path": "variants",
                        "query": {"match": {"variants.text": {"query": normalized_query, "fuzziness": "AUTO"}}},
                        "score_mode": "max"
                    }}
                ]
                # Multi-token boost (phrase query) for name fields
                should_clauses.append({"match_phrase": {"name": {"query": normalized_query, "boost": 2.0}}})
                should_clauses.append({"match_phrase": {"name_ru": {"query": normalized_query, "boost": 1.5}}})
                should_clauses.append({"match_phrase": {"name_en": {"query": normalized_query, "boost": 1.5}}})
                # Phrase boost on nested variants
                should_clauses.append({
                    "nested": {
                        "path": "variants",
                        "query": {"match_phrase": {"variants.text": {"query": normalized_query, "boost": 1.8}}},
                        "score_mode": "max"
                    }
                })
                # Catch-all across all fields to avoid mapping mismatches
                should_clauses.append({
                    "multi_match": {
                        "query": normalized_query,
                        "fields": ["*"],
                        "fuzziness": "AUTO"
                    }
                })
                text_search = {
                    "query": {
                        "bool": {
                            "should": should_clauses
                        }
                    }
                }
                # Dynamic min_score for short queries to cut FP
                # Relaxed thresholds to avoid false zero results on mixed mappings
                if len((normalized_query or '').strip()) <= 8:
                    text_search["min_score"] = 1.0
                elif len((normalized_query or '').strip()) <= 12:
                    text_search["min_score"] = 0.5
                
                # Search in available indices, include variants companion (without index_exists gating)
                for index_name in ["sanctions", "payment_vectors", "test_index", "sanctions_variants"]:
                    try:
                        text_results = es_client.search(
                            index_name=index_name,
                            query=text_search,
                            size=query.limit - len(results)
                        )
                        for hit in text_results.get("hits", {}).get("hits", []):
                            if index_name == "sanctions_variants":
                                parent_id = hit.get("_source", {}).get("parent_id")
                                if not parent_id or any(r["id"] == parent_id for r in results):
                                    continue
                                try:
                                    parent = es_client.client.get(index="sanctions", id=parent_id)
                                    results.append({
                                        "id": parent_id,
                                        "score": hit.get("_score", 0.0),
                                        "source": parent.get("_source", {}),
                                        "index": "sanctions"
                                    })
                                except Exception as ge:
                                    logger.info(f"Failed to fetch parent {parent_id}: {ge}")
                            else:
                                if not any(r["id"] == hit["_id"] for r in results):
                                    results.append({
                                        "id": hit["_id"],
                                        "score": hit["_score"],
                                        "source": hit["_source"],
                                        "index": index_name
                                    })
                            if len(results) >= query.limit:
                                break
                    except Exception as e:
                        logger.warning(f"Text search in {index_name} failed: {e}")
                    if len(results) >= query.limit:
                        break
                        
            except Exception as e:
                logger.warning(f"Text search failed: {e}")
        
        # Combine duplicates and fuse scores (vector vs text)
        fused = {}
        def add_hit(h, method):
            _id = h["id"]
            e = fused.setdefault(_id, {"id": _id, "source": h.get("source", {}), "index": h.get("index", "sanctions"), "vector_score": 0.0, "text_score": 0.0})
            sc = h.get("score", 0.0)
            if method in ("vector", "variant_vector"):
                e["vector_score"] = max(e["vector_score"], sc)
            else:
                e["text_score"] = max(e["text_score"], sc)

        # Divide results into vector/text heuristically by index and availability of query_vector
        for r in results:
            if query_vector and r.get("index") in ("sanctions", "sanctions_variants") and r.get("score"):
                add_hit(r, "vector" if r.get("index") == "sanctions" else "variant_vector")
            else:
                add_hit(r, "text")

        fused_list = []
        for _id, e in fused.items():
            vs = e["vector_score"]; ts = e["text_score"]
            # Weighted fusion; if both present, combine, else use max
            if vs > 0 and ts > 0:
                final = 0.7 * vs + 0.3 * ts
            else:
                final = max(vs, ts)
            fused_list.append({
                "id": _id,
                "score": final,
                "source": e["source"],
                "index": e["index"]
            })

        fused_list.sort(key=lambda x: x.get("score", 0.0), reverse=True)
        fused_list = fused_list[:query.limit]

        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "success": True,
            "query": query.query,
            "normalized_query": normalized_query,
            "language": language,
            "embeddings_length": len(query_vector) if query_vector else 0,
            "results": fused_list,
            "total": len(fused_list),
            "processing_time": processing_time,
            "server_info": {
                "elasticsearch_available": es_client is not None,
                "ai_processing_available": ai_processor is not None,
                "search_type": "vector+text" if query_vector else "text_only"
            }
        }
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index")
async def index_document(request: IndexRequest, services: dict = Depends(get_services)):
    """Index a document."""
    try:
        es_client = services["es_client"]
        
        # Convert document to dict if it's not already
        document = dict(request.document) if hasattr(request.document, '__dict__') else request.document
        
        response = es_client.index_document(
            index_name=request.index,
            document=document,
            doc_id=request.doc_id,
            routing=request.routing
        )
        
        return {
            "success": True,
            "result": response,
            "message": f"Document indexed in {request.index}"
        }
    except Exception as e:
        logger.error(f"Failed to index document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indices")
async def list_indices(services: dict = Depends(get_services)):
    """List available indices."""
    try:
        es_client = services["es_client"]
        indices = es_client.client.indices.get_alias(index="*")
        return {"indices": list(indices.keys())}
    except Exception as e:
        logger.error(f"Failed to list indices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/index/{index_name}")
async def delete_index(index_name: str, services: dict = Depends(get_services)):
    """Delete an index."""
    try:
        es_client = services["es_client"]
        response = es_client.delete_index(index_name)
        return {
            "success": True,
            "message": f"Index {index_name} deleted",
            "result": response
        }
    except Exception as e:
        logger.error(f"Failed to delete index {index_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class NormalizeRequest(BaseModel):
    """Normalize text request."""
    text: str = Field(..., description="Text to normalize")

@app.post("/normalize")
async def normalize_text(
    request: NormalizeRequest,
    services: dict = Depends(get_services)
):
    """Normalize text using AI service."""
    try:
        if not services["ai_processor"]:
            return {
                "success": False,
                "error": "AI processing not available",
                "original_text": request.text,
                "normalized_text": request.text
            }
        
        result = await services["ai_processor"].process_text(
            text=request.text,
            generate_embeddings=False,
            generate_variants=True
        )
        
        return {
            "success": result["success"],
            "original_text": request.text,
            "normalized_text": result.get("normalized_text", request.text),
            "language": result.get("language", "unknown"),
            "variants": result.get("variants", []),
            "processing_info": result.get("processing_info", {})
        }
        
    except Exception as e:
        logger.error(f"Text normalization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "server_full:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
