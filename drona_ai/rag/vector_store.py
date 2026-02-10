"""
Vector Store Module - Stores and manages our text embeddings

This is like a smart library where instead of alphabetical order,
we organize information by similarity. When you ask a question,
we can quickly find the most relevant stored information.
"""

import numpy as np
from typing import List, Tuple


class VectorStore:
    """
    A simple in-memory vector store that keeps track of:
    - The original text chunks
    - Their corresponding embeddings (vector representations)
    - Metadata about each chunk (optional info like source, date, etc.)
    
    Think of it as a database optimized for finding similar items.
    """
    
    def __init__(self):
        """
        Initialize an empty vector store.
        We'll store everything in simple lists for now.
        """
        # These lists will grow as we add more documents
        self.texts = []           # The actual text content
        self.embeddings = []      # The numerical representations
        self.metadata = []        # Extra info about each text
        
        print("✓ Vector store initialized (in-memory storage)")
        print("  You can add documents and search for similar content.\n")
    
    def add_text(self, text, embedding, metadata=None):
        """
        Add a single text with its embedding to the store.
        
        Args:
            text: The original text string
            embedding: The vector representation of the text
            metadata: Optional dictionary with extra info (like {'source': 'study_notes.pdf'})
        """
        self.texts.append(text)
        self.embeddings.append(embedding)
        
        # If no metadata provided, just use an empty dictionary
        self.metadata.append(metadata if metadata else {})
    
    def add_texts(self, texts, embeddings, metadatas=None):
        """
        Add multiple texts at once - more efficient for bulk uploads.
        
        Args:
            texts: List of text strings
            embeddings: List of corresponding embeddings
            metadatas: Optional list of metadata dictionaries
        """
        # If no metadata provided, create empty dictionaries for each text
        if metadatas is None:
            metadatas = [{}] * len(texts)
        
        # Add all the texts to our storage
        self.texts.extend(texts)
        self.embeddings.extend(embeddings)
        self.metadata.extend(metadatas)
        
        print(f"✓ Added {len(texts)} documents to the vector store")
        print(f"  Total documents in store: {len(self.texts)}\n")
    
    def search(self, query_embedding, top_k=3):
        """
        Find the most similar texts to a query embedding.
        
        This is the core of RAG - we compare the query to all stored embeddings
        and return the most similar ones.
        
        Args:
            query_embedding: The vector representation of the user's query
            top_k: How many similar results to return (default: 3)
            
        Returns:
            List of tuples: (text, similarity_score, metadata)
        """
        # Edge case: if there's nothing in the store yet, return empty
        if len(self.embeddings) == 0:
            print("⚠ Vector store is empty! Add some documents first.")
            return []
        
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
        """
        Calculate cosine similarity between query and all stored vectors.
        
        Cosine similarity measures the angle between vectors:
        - 1.0 means vectors point in exactly the same direction (very similar)
        - 0.0 means vectors are perpendicular (unrelated)
        - -1.0 means vectors point in opposite directions (very different)
        
        Args:
            query_vector: The query embedding
            stored_vectors: Array of all stored embeddings
            
        Returns:
            Array of similarity scores
        """
        # Normalize the query vector (make it length 1)
        query_norm = query_vector / np.linalg.norm(query_vector)
        
        # Normalize all stored vectors
        stored_norms = stored_vectors / np.linalg.norm(stored_vectors, axis=1, keepdims=True)
        
        # Dot product of normalized vectors gives us cosine similarity
        # This is much faster than calculating angles directly
        similarities = np.dot(stored_norms, query_norm)
        
        return similarities
    
    def count(self):
        """Return the number of documents in the store."""
        return len(self.texts)
    
    def clear(self):
        """Remove all documents from the store."""
        self.texts = []
        self.embeddings = []
        self.metadata = []
        print("✓ Vector store cleared\n")
    
    def get_stats(self):
        """Get some basic statistics about the vector store."""
        return {
            'total_documents': len(self.texts),
            'embedding_dimension': len(self.embeddings[0]) if self.embeddings else 0,
            'storage_type': 'in-memory'
        }
