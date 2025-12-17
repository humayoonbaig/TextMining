#!/usr/bin/env python3
"""
Test script for the Legal RAG API endpoint.

This script tests both single-agent and multi-agent systems using the test set.

Usage:
    python test_api.py [--url URL] [--test-set TEST_SET_PATH]
"""

import argparse
import json
import requests
import time
from pathlib import Path
from typing import Dict, Any, List


def load_test_set(path: str = "test_set.json") -> Dict[str, Any]:
    """Load the test question set."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_health_check(base_url: str) -> bool:
    """Test the health check endpoint."""
    print("\n🔍 Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_system_info(base_url: str) -> bool:
    """Test the system info endpoint."""
    print("\n🔍 Testing system info endpoint...")
    try:
        response = requests.get(f"{base_url}/system_info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ System info retrieved:")
            print(f"   - LLM: {data['llm']['provider']} / {data['llm']['model']}")
            print(f"   - Embeddings: {data['embeddings']['provider']} / {data['embeddings']['model']}")
            print(f"   - Vector stores: {len(data['vector_stores'])} databases")
            print(f"   - Multi-agent: {data['system']['multi_agent']}")
            return True
        else:
            print(f"❌ System info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ System info error: {e}")
        return False


def test_single_query(base_url: str, question: str, system: str = "multi-agent") -> Dict[str, Any]:
    """Test a single query."""
    payload = {
        "question": question,
        "system": system
    }

    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/query",
            json=payload,
            timeout=60
        )
        elapsed_time = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            data['response_time'] = elapsed_time
            return data
        else:
            return {
                "error": f"HTTP {response.status_code}",
                "detail": response.text,
                "response_time": elapsed_time
            }
    except Exception as e:
        return {
            "error": str(e),
            "type": type(e).__name__
        }


def run_test_suite(base_url: str, test_set_path: str = "test_set.json"):
    """Run the complete test suite."""
    print(f"\n{'='*60}")
    print(f"🧪 Legal RAG API Test Suite")
    print(f"{'='*60}")
    print(f"API Base URL: {base_url}")
    print(f"Test Set: {test_set_path}")

    # Test health and system info
    if not test_health_check(base_url):
        print("\n❌ Health check failed. Ensure the API server is running.")
        return

    test_system_info(base_url)

    # Load test set
    try:
        test_set = load_test_set(test_set_path)
        questions = test_set['test_questions']
        print(f"\n📋 Loaded {len(questions)} test questions")
    except Exception as e:
        print(f"\n❌ Failed to load test set: {e}")
        return

    # Test both systems
    systems = ["single-agent", "multi-agent"]
    results = {system: [] for system in systems}

    for system in systems:
        print(f"\n{'='*60}")
        print(f"🤖 Testing {system.upper()} System (Task {'A' if system == 'single-agent' else 'B'})")
        print(f"{'='*60}")

        for i, test_item in enumerate(questions[:5], 1):  # Test first 5 questions
            question = test_item['question']
            print(f"\n[{i}/5] Question: {question[:80]}...")

            result = test_single_query(base_url, question, system)

            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                results[system].append({
                    "question_id": test_item['id'],
                    "status": "error",
                    "error": result.get('error'),
                    "response_time": result.get('response_time', 0)
                })
            else:
                print(f"✅ Answer received ({result['response_time']:.2f}s)")
                print(f"   Sources: {result['metadata']['num_sources']}")
                print(f"   Countries: {result['metadata'].get('countries_covered', [])}")
                print(f"   Answer preview: {result['answer'][:150]}...")

                results[system].append({
                    "question_id": test_item['id'],
                    "status": "success",
                    "answer": result['answer'],
                    "num_sources": result['metadata']['num_sources'],
                    "response_time": result['response_time'],
                    "contexts": result['contexts']
                })

    # Save results
    output_file = f"test_results_{int(time.time())}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_set": test_set_path,
            "base_url": base_url,
            "timestamp": time.time(),
            "results": results
        }, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"📊 Test Summary")
    print(f"{'='*60}")

    for system in systems:
        successful = sum(1 for r in results[system] if r['status'] == 'success')
        total = len(results[system])
        avg_time = sum(r['response_time'] for r in results[system]) / total if total > 0 else 0

        print(f"\n{system.upper()}:")
        print(f"  Success rate: {successful}/{total} ({successful/total*100:.1f}%)")
        print(f"  Average response time: {avg_time:.2f}s")

    print(f"\n💾 Results saved to: {output_file}")
    print(f"\n✅ Test suite completed!")


def test_batch_query(base_url: str, questions: List[str], system: str = "multi-agent"):
    """Test the batch query endpoint."""
    print(f"\n🔍 Testing batch query endpoint ({system})...")

    payload = {
        "questions": questions,
        "system": system
    }

    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/batch_query",
            json=payload,
            timeout=120
        )
        elapsed_time = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            results = data['results']
            print(f"✅ Batch query completed ({elapsed_time:.2f}s)")
            print(f"   Processed {len(results)} questions")
            successful = sum(1 for r in results if 'error' not in r)
            print(f"   Success rate: {successful}/{len(results)}")
            return data
        else:
            print(f"❌ Batch query failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Batch query error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Test the Legal RAG API endpoint'
    )
    parser.add_argument(
        '--url',
        type=str,
        default='http://localhost:8000',
        help='Base URL of the API (default: http://localhost:8000)'
    )
    parser.add_argument(
        '--test-set',
        type=str,
        default='test_set.json',
        help='Path to the test set JSON file (default: test_set.json)'
    )
    parser.add_argument(
        '--batch-test',
        action='store_true',
        help='Also test the batch query endpoint'
    )

    args = parser.parse_args()

    # Run main test suite
    run_test_suite(args.url, args.test_set)

    # Optional batch test
    if args.batch_test:
        test_set = load_test_set(args.test_set)
        sample_questions = [q['question'] for q in test_set['test_questions'][:3]]
        test_batch_query(args.url, sample_questions, "multi-agent")


if __name__ == '__main__':
    main()
