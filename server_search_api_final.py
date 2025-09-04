#!/usr/bin/env python3
"""
Final server-side API for Payment Vector Testing.
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

from src.es_client import ElasticsearchClient
from src.ai_integration import AIProcessor, DataNormalizer
from config.config import config

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

# Dependency to get services
async def get_services():
    """Get initialized services."""
    global es_client, ai_processor, data_normalizer
    
    if es_client is None or ai_processor is None:
        raise HTTPException(status_code=503, detail="Services not initialized")
    
    return {
        "es_client": es_client,
        "ai_processor": ai_processor,
        "data_normalizer": data_normalizer
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global es_client, ai_processor, data_normalizer
    
    try:
        logger.info("Initializing server services...")
        
        # Initialize Elasticsearch
        es_client = ElasticsearchClient()
        
        # Initialize AI services
        ai_processor = AIProcessor()
        data_normalizer = DataNormalizer(ai_processor)
        
        logger.info("All services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Check Elasticsearch
        es_health = es_client.client.cluster.health()
        
        # Check AI service
        ai_health = {"status": "healthy" if ai_processor else "unhealthy"}
        
        # Check indices
        indices = {
            "sanctions": es_client.index_exists("sanctions"),
            "payment_vectors": es_client.index_exists(config.vector.index_name)
        }
        
        overall_status = "healthy" if es_health["status"] in ["green", "yellow"] else "unhealthy"
        
        return HealthResponse(
            status=overall_status,
            elasticsearch=es_health,
            ai_service=ai_health,
            indices=indices,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=str(e))

# Main search endpoint
@app.post("/search", response_model=SearchResult)
async def search(
    query: SearchQuery,
    services: dict = Depends(get_services)
):
    """
    Main search endpoint:
    1. Receive query (e.g., "Петро Порошенко")
    2. Normalize and vectorize with AI
    3. Search in Elasticsearch
    4. Return results
    """
    try:
        start_time = datetime.now()
        
        logger.info(f"Processing search query: '{query.query}'")
        
        # Step 1: Process query with AI (normalize + vectorize)
        ai_result = await services["ai_processor"].process_text(
            text=query.query,
            include_embeddings=True,
            include_variants=True
        )
        
        if not ai_result["success"]:
            raise HTTPException(status_code=400, detail=f"AI processing failed: {ai_result.get('error', 'Unknown error')}")
        
        query_vector = ai_result["embeddings"]
        normalized_query = ai_result.get("normalized_text", query.query)
        language = ai_result.get("language", "unknown")
        variants = ai_result.get("variants", [])
        
        logger.info(f"Query normalized: '{normalized_query}' (language: {language})")
        logger.info(f"Generated vector of length: {len(query_vector)}")
        
        # Step 2: Search in Elasticsearch
        results = []
        
        # Search in sanctions
        if query.index_type in ["sanctions", "both"]:
            sanctions_search = {
                "knn": {
                    "field": "vector",
                    "query_vector": query_vector,
                    "k": query.limit,
                    "num_candidates": query.limit * 2
                }
            }
            
            try:
                sanctions_results = services["es_client"].search(
                    index_name="sanctions",
                    query=sanctions_search
                )
                
                for hit in sanctions_results.get("hits", {}).get("hits", []):
                    if hit["_score"] >= query.threshold:
                        results.append({
                            "type": "sanctions",
                            "score": hit["_score"],
                            "data": hit["_source"]
                        })
                        
                logger.info(f"Found {len(results)} sanctions matches")
                
            except Exception as e:
                logger.warning(f"Sanctions search failed: {e}")
        
        # Search in payments
        if query.index_type in ["payments", "both"]:
            payment_search = {
                "knn": {
                    "field": "vector",
                    "query_vector": query_vector,
                    "k": query.limit,
                    "num_candidates": query.limit * 2
                }
            }
            
            try:
                payment_results = services["es_client"].search(
                    index_name=config.vector.index_name,
                    query=payment_search
                )
                
                for hit in payment_results.get("hits", {}).get("hits", []):
                    if hit["_score"] >= query.threshold:
                        results.append({
                            "type": "payment",
                            "score": hit["_score"],
                            "data": hit["_source"]
                        })
                        
                logger.info(f"Found {len(results)} total matches (including payments)")
                
            except Exception as e:
                logger.warning(f"Payment search failed: {e}")
        
        # Step 3: Sort by score and limit results
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:query.limit]
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Server info
        server_info = {
            "server_id": "payment-vector-search-server",
            "version": "1.0.0",
            "ai_processed": True,
            "normalized_query": normalized_query,
            "language": language,
            "variants": variants,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Search completed: {len(results)} results in {processing_time:.3f}s")
        
        return SearchResult(
            success=True,
            query=query.query,
            normalized_query=normalized_query,
            language=language,
            embeddings_length=len(query_vector),
            results=results,
            total=len(results),
            processing_time=processing_time,
            server_info=server_info
        )
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Statistics endpoint
@app.get("/stats")
async def get_statistics(services: dict = Depends(get_services)):
    """Get server statistics."""
    try:
        stats = {
            "server": {
                "id": "payment-vector-search-server",
                "version": "1.0.0",
                "description": "Query → Normalize → Vectorize → Search → Results"
            },
            "elasticsearch": {
                "sanctions_index_exists": services["es_client"].index_exists("sanctions"),
                "payment_index_exists": services["es_client"].index_exists(config.vector.index_name)
            },
            "ai_service": {
                "status": "healthy" if services["ai_processor"] else "unhealthy"
            }
        }
        
        # Get index stats
        try:
            if stats["elasticsearch"]["sanctions_index_exists"]:
                sanctions_stats = services["es_client"].client.indices.stats(index="sanctions")
                stats["sanctions_index"] = {
                    "document_count": sanctions_stats["indices"]["sanctions"]["total"]["docs"]["count"],
                    "size_bytes": sanctions_stats["indices"]["sanctions"]["total"]["store"]["size_in_bytes"]
                }
        except Exception as e:
            logger.warning(f"Failed to get sanctions stats: {e}")
        
        try:
            if stats["elasticsearch"]["payment_index_exists"]:
                payment_stats = services["es_client"].client.indices.stats(index=config.vector.index_name)
                stats["payment_index"] = {
                    "document_count": payment_stats["indices"][config.vector.index_name]["total"]["docs"]["count"],
                    "size_bytes": payment_stats["indices"][config.vector.index_name]["total"]["store"]["size_in_bytes"]
                }
        except Exception as e:
            logger.warning(f"Failed to get payment stats: {e}")
        
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Payment Vector Testing - Search API",
        "version": "1.0.0",
        "description": "Query → Normalize → Vectorize → Search → Results",
        "docs": "/docs",
        "health": "/health",
        "example": {
            "query": "Петро Порошенко",
            "endpoint": "POST /search",
            "description": "Send query, get normalized and vectorized search results"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "server_search_api_final:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
