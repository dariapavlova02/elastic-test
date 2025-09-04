#!/usr/bin/env python3
"""
Final search client for Payment Vector Testing.
Sends query to server → gets normalized and vectorized search results.
"""
import requests
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

class FinalSearchClient:
    """Client for sending search queries to the server."""
    
    def __init__(self, server_url: str, api_key: Optional[str] = None):
        """
        Initialize search client.
        
        Args:
            server_url: Base URL of the server (e.g., http://your-server:8000)
            api_key: Optional API key for authentication
        """
        self.server_url = server_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
        
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to server."""
        url = f"{self.server_url}{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Server request failed: {e}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check server health."""
        return self._make_request("GET", "/health")
    
    def search(self, query: str, limit: int = 10, threshold: float = 0.7, 
              index_type: str = "both") -> Dict[str, Any]:
        """
        Search for entities.
        
        Args:
            query: Search query (e.g., "Петро Порошенко")
            limit: Maximum number of results
            threshold: Similarity threshold (0.0 to 1.0)
            index_type: Type of index to search ("payments", "sanctions", "both")
        """
        search_data = {
            "query": query,
            "limit": limit,
            "threshold": threshold,
            "index_type": index_type
        }
        return self._make_request("POST", "/search", json=search_data)
    
    def search_sanctions(self, query: str, limit: int = 10, threshold: float = 0.7) -> Dict[str, Any]:
        """Search only in sanctions."""
        return self.search(query, limit, threshold, "sanctions")
    
    def search_payments(self, query: str, limit: int = 10, threshold: float = 0.7) -> Dict[str, Any]:
        """Search only in payments."""
        return self.search(query, limit, threshold, "payments")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get server statistics."""
        return self._make_request("GET", "/stats")
    
    def test_connection(self) -> bool:
        """Test connection to server."""
        try:
            health = self.health_check()
            return health.get("status") == "healthy"
        except Exception:
            return False

def main():
    """Example usage of the final search client."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Final search client for Payment Vector Testing")
    parser.add_argument("--server-url", default="http://localhost:8000", help="Server URL")
    parser.add_argument("--query", default="Петро Порошенко", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Maximum results")
    parser.add_argument("--threshold", type=float, default=0.7, help="Similarity threshold")
    parser.add_argument("--index-type", default="both", choices=["payments", "sanctions", "both"], help="Index type to search")
    parser.add_argument("--test-queries", action="store_true", help="Test multiple queries")
    
    args = parser.parse_args()
    
    print("Payment Vector Testing - Final Search Client")
    print("=" * 50)
    print(f"Server URL: {args.server_url}")
    print(f"Query: {args.query}")
    print(f"Index type: {args.index_type}")
    print()
    
    # Initialize client
    client = FinalSearchClient(args.server_url)
    
    try:
        # Test connection
        print("Testing connection...")
        if not client.test_connection():
            print("❌ Cannot connect to server")
            return 1
        print("✅ Connected to server")
        
        # Perform search
        print(f"\nSearching for: '{args.query}'")
        print("Processing: Query → Normalize → Vectorize → Search → Results")
        
        result = client.search(args.query, args.limit, args.threshold, args.index_type)
        
        if result["success"]:
            print(f"✅ Search successful!")
            print(f"  Original query: {result['query']}")
            print(f"  Normalized query: {result['normalized_query']}")
            print(f"  Language: {result['language']}")
            print(f"  Embeddings length: {result['embeddings_length']}")
            print(f"  Found {result['total']} matches in {result['processing_time']:.3f}s")
            
            # Display results
            if result["results"]:
                print(f"\nResults:")
                print("-" * 50)
                
                for i, match in enumerate(result["results"], 1):
                    print(f"\n{i}. {match['type'].upper()} (score: {match['score']:.3f})")
                    data = match["data"]
                    
                    if match["type"] == "sanctions":
                        print(f"   Entity ID: {data.get('entity_id', 'N/A')}")
                        print(f"   Name: {data.get('name', 'N/A')}")
                        print(f"   Type: {data.get('entity_type', 'N/A')}")
                        print(f"   Country: {data.get('country', 'N/A')}")
                        print(f"   Sanctions List: {data.get('sanctions_list', 'N/A')}")
                        print(f"   Description: {data.get('description', 'N/A')}")
                        if data.get('aliases'):
                            print(f"   Aliases: {data.get('aliases', 'N/A')}")
                    
                    elif match["type"] == "payment":
                        print(f"   Payment ID: {data.get('payment_id', 'N/A')}")
                        print(f"   Sender: {data.get('sender', 'N/A')}")
                        print(f"   Receiver: {data.get('receiver', 'N/A')}")
                        print(f"   Amount: {data.get('amount', 'N/A')} {data.get('currency', '')}")
                        print(f"   Description: {data.get('description', 'N/A')}")
                        print(f"   Risk Score: {data.get('risk_score', 'N/A')}")
                        print(f"   Sanctions Matches: {len(data.get('sanctions_matches', []))}")
            else:
                print("  No matches found")
        else:
            print(f"❌ Search failed: {result.get('error', 'Unknown error')}")
            return 1
        
        # Test multiple queries
        if args.test_queries:
            print("\n" + "=" * 50)
            print("Testing multiple queries:")
            print("=" * 50)
            
            test_queries = [
                "Петро Порошенко",
                "Petro Poroshenko", 
                "Порошенко Петр",
                "ABC Corporation",
                "John Smith payment",
                "international transfer",
                "suspicious transaction"
            ]
            
            for query in test_queries:
                print(f"\nTesting: '{query}'")
                try:
                    result = client.search(query, limit=3)
                    if result["success"]:
                        print(f"  ✅ Found {result['total']} matches (normalized: '{result['normalized_query']}')")
                    else:
                        print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")
                except Exception as e:
                    print(f"  ❌ Error: {e}")
        
        # Get statistics
        print("\n" + "=" * 50)
        print("Server Statistics:")
        stats = client.get_statistics()
        print(json.dumps(stats, indent=2))
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
