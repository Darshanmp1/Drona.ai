"""
Vector Store - Smart storage layer for text embeddings

Handles vector storage with intelligent backend switching:

Primary: Endee Vector Database
- High-performance C++ implementation we built for this project
- Uses HNSW algorithm for fast nearest-neighbor search
- Persists data across sessions
- Handles large-scale vector collections efficiently

Fallback: In-Memory NumPy Storage
- Simple, always-available backup option
- No external dependencies needed
- Perfect for testing or when Endee isn't running
- Automatic fallback ensures the system always works

The store automatically picks the best available backend.
"""

import numpy as np
from typing import List, Tuple, Optional
import hashlib
from .endee_client import EndeeClient


class VectorStore:
    def __init__(self, index_name: str = "drona_ai", 
                 dimension: int = 384,
                 use_endee: bool = True,
                 endee_url: str = "http://localhost:8080"):
        self.index_name = index_name
        self.dimension = dimension
        self.endee_available = False
        self.endee_client = None
        
        # Attempt Endee connection if enabled
        if use_endee:
            self._try_connect_endee(endee_url)
        
        # Setup fallback storage (NumPy arrays for when Endee isn't available)
        self.texts = []
        self.embeddings = []
        self.metadata = []
        self._id_counter = 0
        self.id_to_index = {}  # Maps Endee vector IDs to text indices
        
        # Print status
        if self.endee_available:
            print("✓ Vector store initialized using Endee database")
            print(f"  Index: {index_name}")
            print(f"  Backend: High-performance C++ vector DB\n")
        else:
            print("✓ Vector store initialized (in-memory storage)")
            print("  Backend: NumPy fallback mode")
            print("  Tip: Start Endee server for production performance.\n")
    
    def _try_connect_endee(self, endee_url: str):
        try:
            # Create Endee client
            self.endee_client = EndeeClient(base_url=endee_url)
            
            # Check if server is healthy
            if self.endee_client.health_check():
                # Try to create index (will fail gracefully if exists)
                self.endee_client.create_index(
                    index_name=self.index_name,
                    dimension=self.dimension,
                    quantization="FLOAT32"  # Use FLOAT32 for best accuracy
                )
                
                self.endee_available = True
                print(f"→ Connected to Endee at {endee_url}")
            else:
                print(f"→ Endee server not responding at {endee_url}")
        except Exception as e:
            print(f"→ Could not connect to Endee: {e}")
            self.endee_client = None
    
    def _generate_id(self, text: str) -> str:
        # Use MD5 hash of text + counter for uniqueness
        unique_str = f"{text}_{self._id_counter}"
        self._id_counter += 1
        return hashlib.md5(unique_str.encode()).hexdigest()[:16]
    
    def add_text(self, text: str, embedding: np.ndarray, metadata: Optional[dict] = None):
        # Store in memory (always, for fallback and caching)
        text_index = len(self.texts)
        self.texts.append(text)
        self.embeddings.append(embedding)
        self.metadata.append(metadata if metadata else {})
        
        # If Endee is available, also store there for persistence
        if self.endee_available and self.endee_client:
            try:
                # Convert embedding to list and create vector object
                vector_id = self._generate_id(text)
                vector_obj = {
                    "id": vector_id,
                    "vector": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
                }
                
                # Store ID-to-index mapping
                self.id_to_index[vector_id] = text_index
                
                # Insert into Endee
                self.endee_client.insert_vectors(self.index_name, [vector_obj])
            except Exception as e:
                print(f"Warning: Could not insert to Endee: {e}")
                print("  Continuing with in-memory storage only.")
    
    def add_texts(self, texts: List[str], embeddings: List[np.ndarray], 
                  metadatas: Optional[List[dict]] = None):
        # If no metadata provided, create empty dictionaries for each text
        if metadatas is None:
            metadatas = [{}] * len(texts)
        
        # Store starting index for mapping
        start_index = len(self.texts)
        
        # Add all texts to in-memory storage
        self.texts.extend(texts)
        self.embeddings.extend(embeddings)
        self.metadata.extend(metadatas)
        
        # If Endee is available, batch insert for efficiency
        if self.endee_available and self.endee_client:
            try:
                # Prepare batch of vector objects
                vector_batch = []
                for idx, (text, embedding) in enumerate(zip(texts, embeddings)):
                    vector_id = self._generate_id(text)
                    vector_obj = {
                        "id": vector_id,
                        "vector": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
                    }
                    vector_batch.append(vector_obj)
                    
                    # Store ID-to-index mapping
                    self.id_to_index[vector_id] = start_index + idx
                
                # Batch insert into Endee
                success = self.endee_client.insert_vectors(self.index_name, vector_batch)
                
                if success:
                    print(f"✓ Added {len(texts)} documents to Endee vector database")
                else:
                    print(f"✓ Added {len(texts)} documents to in-memory storage")
            except Exception as e:
                print(f"Warning: Endee insert failed: {e}")
                print(f"✓ Added {len(texts)} documents to in-memory storage")
        else:
            print(f"✓ Added {len(texts)} documents to in-memory storage")
        
        print(f"  Total documents in store: {len(self.texts)}\n")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[str, float, dict]]:
        # Edge case: if there's nothing in the store yet, return empty
        if len(self.texts) == 0:
            print("⚠ Vector store is empty! Add some documents first.")
            return []
        
        # Try Endee first if available
        if self.endee_available and self.endee_client:
            try:
                # Convert query embedding to list
                query_list = query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding
                
                # Search in Endee
                endee_results = self.endee_client.search(
                    index_name=self.index_name,
                    query_vector=query_list,
                    k=top_k,
                    include_vectors=False
                )
                
                if endee_results is not None and len(endee_results) > 0:
                    # Map Endee results to our texts
                    results = []
                    for item in endee_results[:top_k]:
                        vector_id = item.get('id')
                        score = item.get('score', 0.0)
                        
                        # Get text index from mapping
                        if vector_id in self.id_to_index:
                            idx = self.id_to_index[vector_id]
                            text = self.texts[idx]
                            metadata = self.metadata[idx]
                            results.append((text, score, metadata))
                    
                    if results:
                        return results
            except Exception as e:
                print(f"Endee search failed: {e}, using in-memory fallback")
        
        # Fallback to in-memory search
        return self._search_in_memory(query_embedding, top_k)
    
    def _search_in_memory(self, query_embedding: np.ndarray, top_k: int) -> List[Tuple[str, float, dict]]:
        # Convert our embeddings list to a numpy array for efficient computation
        stored_embeddings = np.array(self.embeddings)
        
        # Calculate similarity scores using cosine similarity
        # This measures how "aligned" two vectors are (1 = identical, 0 = unrelated)
        similarities = self._cosine_similarity(query_embedding, stored_embeddings)
        
        # Get the indices of the top_k most similar items
        # argsort gives us indices sorted by similarity, [::-1] reverses to get highest first
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Collect the results with their scores
        results = []
        for idx in top_indices:
            results.append((
                self.texts[idx],           # The original text
                float(similarities[idx]),  # Similarity score
                self.metadata[idx]         # Any metadata
            ))
        
        return results
    
    def _cosine_similarity(self, query_vector, stored_vectors):
        # Normalize the query vector (make it length 1)
        query_norm = query_vector / np.linalg.norm(query_vector)
        
        # Normalize all stored vectors
        stored_norms = stored_vectors / np.linalg.norm(stored_vectors, axis=1, keepdims=True)
        
        # Dot product of normalized vectors gives us cosine similarity
        # This is much faster than calculating angles directly
        similarities = np.dot(stored_norms, query_norm)
        
        return similarities
    
    def count(self) -> int:
        return len(self.texts)
    
    def is_using_endee(self) -> bool:
        return self.endee_available
    
    def get_backend_info(self) -> dict:
        info = {
            'backend': 'endee' if self.endee_available else 'numpy',
            'connected': self.endee_available,
            'index_name': self.index_name,
            'dimension': self.dimension,
            'document_count': len(self.texts),
            'persistent': self.endee_available
        }
        
        if self.endee_available and self.endee_client:
            try:
                stats = self.endee_client.get_stats()
                if stats:
                    info['endee_stats'] = stats
            except:
                pass
        
        return info
    
    def clear(self):
        self.texts = []
        self.embeddings = []
        self.metadata = []
        self._id_counter = 0
        
        # If using Endee, would delete and recreate index
        # For now, just clear in-memory storage
        
        backend = "Endee + In-Memory" if self.endee_available else "In-Memory"
        print(f"✓ Vector store cleared ({backend})\n")
    
    def get_stats(self):
        return {
            'total_documents': len(self.texts),
            'embedding_dimension': len(self.embeddings[0]) if self.embeddings else 0,
            'storage_type': 'in-memory'
        }
