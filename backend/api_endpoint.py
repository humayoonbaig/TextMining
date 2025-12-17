# backend/api_endpoint.py
"""
REST API endpoint for exam submission using FastAPI.
This provides an HTTP endpoint that can be called by the evaluation system.
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

from .config import RAGConfig
from .rag_pipeline import answer_question

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Legal RAG System API",
    description="REST API for multi-national legal RAG system",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def initialize_config() -> RAGConfig:
    """Initialize RAGConfig with production settings for exam submission."""
    config = RAGConfig()

    # LLM settings
    config.llm_provider = "openai"
    config.llm_model_name = "gpt-4o-mini"

    # Embedding settings
    config.embedding_provider = "huggingface"
    config.embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"

    # Data folders - adjust these paths to your Contest_Data structure
    config.json_folders = [
        "Contest_Data/Italy",
        "Contest_Data/Estonia",
        "Contest_Data/slovenia",
    ]

    # Vector store settings - these should point to your built vector stores
    config.vector_store_base_dir = "vector_store"
    config.vector_store_dir = "vector_store/default"

    # Get all vector store directories
    vector_store_dirs = []
    if os.path.exists("vector_store"):
        for item in os.listdir("vector_store"):
            path = os.path.join("vector_store", item)
            if os.path.isdir(path):
                vector_store_dirs.append(path)

    config.vector_store_dirs = vector_store_dirs if vector_store_dirs else ["vector_store/default"]

    # Retrieval settings - optimized for high precision
    config.top_k = 3  # Lower value for better precision
    config.use_rerank = True  # Always use similarity reranking

    # Use multi-agent by default for exam (Task B)
    # Set to False to use single-agent (Task A)
    config.use_multiagent = True
    config.agentic_mode = "standard_rag"

    return config


# Global config instance
_global_config = None


def get_config() -> RAGConfig:
    """Get or initialize the global config."""
    global _global_config
    if _global_config is None:
        _global_config = initialize_config()
    return _global_config


# Request/Response models
class QueryRequest(BaseModel):
    question: str = Field(..., description="The legal question to answer")
    system: Optional[str] = Field("multi-agent", description="System type: 'single-agent' or 'multi-agent'")


class QueryResponse(BaseModel):
    question: str
    answer: str
    contexts: List[str]
    source_ids: List[str]
    metadata: Dict[str, Any]


class BatchQueryRequest(BaseModel):
    questions: List[str] = Field(..., description="List of questions to process")
    system: Optional[str] = Field("multi-agent", description="System type: 'single-agent' or 'multi-agent'")


class BatchQueryResponse(BaseModel):
    results: List[Dict[str, Any]]


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class SystemInfoResponse(BaseModel):
    llm: Dict[str, str]
    embeddings: Dict[str, str]
    vector_stores: List[str]
    data_folders: List[str]
    retrieval: Dict[str, Any]
    system: Dict[str, Any]


@app.get('/health', response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Legal RAG System",
        "version": "1.0"
    }


@app.post('/query', response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Main query endpoint for exam submission.

    Processes a single legal question and returns the answer with supporting context.
    """
    try:
        question = request.question
        system_type = request.system or 'multi-agent'

        # Configure system
        config = get_config()

        # Override system type if specified
        if system_type == 'single-agent':
            config.use_multiagent = False
        else:
            config.use_multiagent = True

        # Get answer
        answer, docs, reasoning_trace = answer_question(
            question=question,
            config=config,
            show_reasoning=False  # Don't include reasoning for exam
        )

        # Extract contexts and source IDs
        contexts = [doc.page_content for doc in docs]
        source_ids = [doc.metadata.get("source", "unknown") for doc in docs]

        # Build response
        return {
            "question": question,
            "answer": answer,
            "contexts": contexts,
            "source_ids": source_ids,
            "metadata": {
                "system": system_type,
                "num_sources": len(docs),
                "countries_covered": list(set(
                    doc.metadata.get("state", "unknown") for doc in docs
                )),
                "law_types_covered": list(set(
                    doc.metadata.get("law", "unknown") for doc in docs
                ))
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")


@app.post('/batch_query', response_model=BatchQueryResponse)
async def batch_query_endpoint(request: BatchQueryRequest):
    """
    Batch query endpoint for processing multiple questions at once.

    Useful for testing or evaluating multiple queries in a single request.
    """
    try:
        questions = request.questions
        system_type = request.system or 'multi-agent'

        # Configure system
        config = get_config()

        if system_type == 'single-agent':
            config.use_multiagent = False
        else:
            config.use_multiagent = True

        # Process each question
        results = []
        for question in questions:
            try:
                answer, docs, _ = answer_question(
                    question=question,
                    config=config,
                    show_reasoning=False
                )

                contexts = [doc.page_content for doc in docs]
                source_ids = [doc.metadata.get("source", "unknown") for doc in docs]

                results.append({
                    "question": question,
                    "answer": answer,
                    "contexts": contexts,
                    "source_ids": source_ids,
                    "metadata": {
                        "system": system_type,
                        "num_sources": len(docs)
                    }
                })
            except Exception as e:
                results.append({
                    "question": question,
                    "error": str(e),
                    "type": type(e).__name__
                })

        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")


@app.get('/system_info', response_model=SystemInfoResponse)
async def system_info():
    """
    Get information about the configured RAG system.

    Returns configuration details for debugging and verification.
    """
    try:
        config = get_config()

        return {
            "llm": {
                "provider": config.llm_provider,
                "model": config.llm_model_name
            },
            "embeddings": {
                "provider": config.embedding_provider,
                "model": config.embedding_model_name
            },
            "vector_stores": config.vector_store_dirs,
            "data_folders": config.json_folders,
            "retrieval": {
                "top_k": config.top_k,
                "use_rerank": config.use_rerank
            },
            "system": {
                "multi_agent": config.use_multiagent,
                "agentic_mode": config.agentic_mode
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")


def run_server(host: str = '0.0.0.0', port: int = 8000):
    """Run the FastAPI server using uvicorn."""
    import uvicorn

    print(f"Starting Legal RAG API server on {host}:{port}")
    print(f"Multi-agent mode: {get_config().use_multiagent}")
    print(f"Vector stores: {get_config().vector_store_dirs}")
    print(f"\n📖 API Documentation available at: http://{host}:{port}/docs")
    print(f"📖 ReDoc available at: http://{host}:{port}/redoc")

    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    run_server()
