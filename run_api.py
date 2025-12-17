#!/usr/bin/env python3
"""
Script to run the FastAPI server for exam submission.

Usage:
    python run_api.py [--port PORT] [--host HOST] [--single-agent]

Examples:
    python run_api.py                    # Run on default port 8000 with multi-agent
    python run_api.py --port 8080        # Run on port 8080
    python run_api.py --single-agent     # Use single-agent system (Task A)
"""

import argparse
import sys
import os
import uvicorn

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.api_endpoint import app, get_config


def main():
    parser = argparse.ArgumentParser(
        description='Run the Legal RAG API server for exam submission (FastAPI)'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host to bind to (default: 0.0.0.0)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port to bind to (default: 8000)'
    )
    parser.add_argument(
        '--single-agent',
        action='store_true',
        help='Use single-agent system (Task A) instead of multi-agent (Task B)'
    )
    parser.add_argument(
        '--reload',
        action='store_true',
        help='Enable auto-reload on code changes (development mode)'
    )

    args = parser.parse_args()

    # Configure system type
    config = get_config()
    if args.single_agent:
        config.use_multiagent = False
        print("🔧 Configured for SINGLE-AGENT mode (Task A)")
    else:
        config.use_multiagent = True
        print("🔧 Configured for MULTI-AGENT mode (Task B)")

    print(f"\n📡 API Endpoints available:")
    print(f"   - Health check: http://{args.host}:{args.port}/health")
    print(f"   - Query: http://{args.host}:{args.port}/query (POST)")
    print(f"   - Batch query: http://{args.host}:{args.port}/batch_query (POST)")
    print(f"   - System info: http://{args.host}:{args.port}/system_info (GET)")
    print(f"\n📖 Interactive API docs: http://{args.host}:{args.port}/docs")
    print(f"📖 ReDoc: http://{args.host}:{args.port}/redoc")
    print(f"\n🚀 Starting FastAPI server...\n")

    uvicorn.run(
        "backend.api_endpoint:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == '__main__':
    main()
