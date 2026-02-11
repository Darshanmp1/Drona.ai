"""
Endee Vector Database Client

Python interface for Endee, our custom C++ vector database built for this project.
Handles all communication with the Endee server including index creation, vector
insertion, and similarity search operations.
"""

import requests
import json
from typing import List, Dict, Optional, Tuple
import numpy as np


class EndeeClient:
    def __init__(self, base_url: str = "http://localhost:8080", 
                 auth_token: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.session = requests.Session()
        
        # Configure session headers for API requests
        if auth_token:
            self.session.headers.update({
                'Authorization': auth_token,
                'Content-Type': 'application/json'
            })
        else:
            self.session.headers.update({
                'Content-Type': 'application/json'
            })
    
    def health_check(self) -> bool:
        try:
            response = self.session.get(f"{self.base_url}/api/v1/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def create_index(self, index_name: str, dimension: int, 
                     quantization: str = "INT8") -> bool:
        try:
            payload = {
                "index_name": index_name,
                "dimension": dimension,
                "quant": quantization
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/index/create",
                json=payload,
                timeout=10
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Error creating index: {e}")
            return False
    
    def insert_vectors(self, index_name: str, vectors: List[Dict]) -> bool:
        """
        Insert vectors into the index.
        
        Args:
            index_name: Name of the index
            vectors: List of vector objects with format:
                     [{"id": "doc1", "vector": [0.1, 0.2, ...]}, ...]
                     
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/index/{index_name}/vector/insert",
                json=vectors,
                timeout=30
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Error inserting vectors: {e}")
            return False
    
    def search(self, index_name: str, query_vector: List[float], 
               k: int = 5, include_vectors: bool = False) -> Optional[List[Dict]]:
        """
        Search for similar vectors in the index.
        
        Args:
            index_name: Name of the index
            query_vector: Query vector as list of floats
            k: Number of nearest neighbors to return
            include_vectors: Whether to include vectors in response
            
        Returns:
            List of results with format:
            [{"id": "doc1", "score": 0.95, "vector": [...]}, ...]
            Returns None if search fails
        """
        try:
            payload = {
                "vector": query_vector,
                "k": k,
                "include_vectors": include_vectors
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/index/{index_name}/search",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                # Endee returns MessagePack by default, but we can parse JSON
                # For simplicity, we expect JSON response
                try:
                    # Try to parse as JSON first
                    result = response.json()
                    return result.get('results', [])
                except:
                    # If MessagePack, would need msgpack library
                    # For now, return None
                    print("Response in MessagePack format. Install msgpack-python for full support.")
                    return None
            else:
                return None
        except Exception as e:
            print(f"Error searching: {e}")
            return None
    
    def delete_index(self, index_name: str) -> bool:
        try:
            response = self.session.delete(
                f"{self.base_url}/api/v1/index/{index_name}",
                timeout=10
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Error deleting index: {e}")
            return False
    
    def get_stats(self) -> Optional[Dict]:
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/stats",
                timeout=5
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error getting stats: {e}")
            return None
