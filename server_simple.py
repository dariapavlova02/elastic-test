#!/usr/bin/env python3
"""
Simplified server API for Elasticsearch testing.
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
from config.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Elasticsearch Testing - Search API",
    description="Simple API for Elasticsearch connection testing",
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

# Global variables
es_client: Optional[ElasticsearchClient] = None

class SearchQuery(BaseModel):
    """Search query model."""
    query: str = Field(..., description="Search query text")
    index: str = Field(default="test_index", description="Elasticsearch index to search")
    size: int = Field(default=10, ge=1, le=100, description="Number of results to return")

class SearchResponse(BaseModel):
    """Search response model."""
    query: str
    index: str
    results: List[Dict[str, Any]]
    total: int
    took: int

class IndexRequest(BaseModel):
    """Index document request."""
    index: str = Field(..., description="Index name")
    document: Dict[str, Any] = Field(..., description="Document to index")
    doc_id: Optional[str] = Field(None, description="Optional document ID")

@app.on_event("startup")
async def startup_event():
    """Initialize server services."""
    global es_client
    
    logger.info("Initializing server services...")
    
    # Force Elasticsearch host for Docker environment
    import os
    es_host = os.getenv('ELASTICSEARCH_HOST', 'elasticsearch')
    es_port = int(os.getenv('ELASTICSEARCH_PORT', '9200'))
    
    logger.info(f"ELASTICSEARCH_HOST: {es_host}")
    logger.info(f"ELASTICSEARCH_PORT: {es_port}")
    
    try:
        # Create direct Elasticsearch client bypassing config
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
        
        logger.info("✅ Server services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Elasticsearch Testing API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        if es_client:
            # Try to ping Elasticsearch
            info = es_client.client.info()
            return {
                "status": "healthy",
                "elasticsearch": {
                    "connected": True,
                    "version": info.get("version", {}).get("number", "unknown"),
                    "cluster": info.get("cluster_name", "unknown")
                },
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return {"status": "unhealthy", "error": "Elasticsearch client not initialized"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

@app.post("/index", response_model=dict)
async def index_document(request: IndexRequest):
    """Index a document."""
    try:
        if not es_client:
            raise HTTPException(status_code=500, detail="Elasticsearch client not initialized")
        
        response = es_client.index_document(
            index_name=request.index,
            document=request.document,
            doc_id=request.doc_id
        )
        
        return {
            "success": True,
            "result": response,
            "message": f"Document indexed in {request.index}"
        }
    except Exception as e:
        logger.error(f"Failed to index document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=SearchResponse)
async def search_documents(query: SearchQuery):
    """Search documents."""
    try:
        if not es_client:
            raise HTTPException(status_code=500, detail="Elasticsearch client not initialized")
        
        # Simple text search query
        search_query = {
            "query": {
                "multi_match": {
                    "query": query.query,
                    "fields": ["*"]
                }
            }
        }
        
        response = es_client.search(
            index_name=query.index,
            query=search_query,
            size=query.size
        )
        
        results = []
        for hit in response["hits"]["hits"]:
            results.append({
                "id": hit["_id"],
                "score": hit["_score"],
                "source": hit["_source"]
            })
        
        return SearchResponse(
            query=query.query,
            index=query.index,
            results=results,
            total=response["hits"]["total"]["value"],
            took=response["took"]
        )
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indices")
async def list_indices():
    """List available indices."""
    try:
        if not es_client:
            raise HTTPException(status_code=500, detail="Elasticsearch client not initialized")
        
        indices = es_client.client.indices.get_alias(index="*")
        return {"indices": list(indices.keys())}
    except Exception as e:
        logger.error(f"Failed to list indices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/index/{index_name}")
async def delete_index(index_name: str):
    """Delete an index."""
    try:
        if not es_client:
            raise HTTPException(status_code=500, detail="Elasticsearch client not initialized")
        
        response = es_client.delete_index(index_name)
        return {
            "success": True,
            "message": f"Index {index_name} deleted",
            "result": response
        }
    except Exception as e:
        logger.error(f"Failed to delete index {index_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "server_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )