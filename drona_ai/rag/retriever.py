"""
Retriever Module - The brain that ties everything together

This module coordinates the embedder and vector store to provide
intelligent retrieval. It handles the workflow of:
1. Converting user queries to embeddings
2. Finding relevant stored information
3. Returning contextual results
"""

from rag.embedder import Embedder
from rag.vector_store import VectorStore


class Retriever:
    """
    The Retriever is your intelligent assistant that:
    - Takes your question
    - Understands what you're asking (via embeddings)
    - Finds the most relevant information it knows
    - Gives you back useful context
    """
    
    def __init__(self):
        """
        Set up the retriever with an embedder and vector store.
        These work together to provide semantic search.
        """
        print("=" * 60)
        print("Initializing Drona AI Retriever")
        print("=" * 60 + "\n")
        
        # The embedder converts text to vectors
        self.embedder = Embedder()
        
        # The vector store keeps track of all our knowledge
        self.vector_store = VectorStore()
        
        print("=" * 60)
        print("✓ Retriever ready!")
        print("=" * 60 + "\n")
    
    def add_knowledge(self, texts, metadatas=None):
        """
        Add new information to the retriever's knowledge base.
        
        This is how you "teach" the AI - give it documents, facts,
        study materials, etc., and it will remember them for later.
        
        Args:
            texts: List of text strings to add (can be paragraphs, facts, etc.)
            metadatas: Optional list of dictionaries with extra info about each text
        """
        print(f"Adding {len(texts)} new pieces of knowledge...")
        
        # Step 1: Convert all the texts into embeddings
        # This captures the "meaning" of each text as numbers
        embeddings = self.embedder.embed_batch(texts)
        
        # Step 2: Store the texts along with their embeddings
        # Now we can search through them later
        self.vector_store.add_texts(texts, embeddings, metadatas)
        
        print(f"✓ Knowledge base updated! Total items: {self.vector_store.count()}\n")
    
    def retrieve(self, query, top_k=3):
        """
        Retrieve the most relevant information for a given query.
        
        This is the core RAG operation - given a question or search query,
        we find the most relevant stored knowledge.
        
        Args:
            query: The user's question or search text
            top_k: How many relevant results to return (default: 3)
            
        Returns:
            List of tuples: (relevant_text, similarity_score, metadata)
        """
        print(f"🔍 Searching for: '{query}'")
        
        # Step 1: Convert the query into an embedding
        # This lets us compare it to our stored knowledge
        query_embedding = self.embedder.embed_text(query)
        
        # Step 2: Search the vector store for similar embeddings
        # This finds the most relevant pieces of information
        results = self.vector_store.search(query_embedding, top_k=top_k)
        
        # Let the user know what we found
        if results:
            print(f"✓ Found {len(results)} relevant result(s)\n")
        else:
            print("⚠ No results found. Try adding some knowledge first!\n")
        
        return results
    
    def generate_response(self, query, top_k=3):
        """
        Generate a response to a user query.
        
        This combines retrieval with response generation.
        For now, we return a simple formatted response with context.
        Later, this can be enhanced with an LLM.
        
        Args:
            query: The user's question
            top_k: How many context pieces to retrieve
            
        Returns:
            A formatted string response
        """
        # Get relevant context from our knowledge base
        results = self.retrieve(query, top_k=top_k)
        
        # If we found relevant information, format a nice response
        if results:
            response = "Based on what I know, here's the relevant information:\n\n"
            
            for i, (text, score, metadata) in enumerate(results, 1):
                response += f"{i}. [Relevance: {score:.2f}]\n"
                response += f"   {text}\n\n"
            
            # This is where you'd integrate an LLM in the future
            # For now, we just return the retrieved context
            response += "💡 Note: In the full version, this context will be used to generate "
            response += "a natural language answer using an AI model."
            
        else:
            response = "I don't have enough information to answer that yet. "
            response += "Try adding some knowledge to my database first!"
        
        return response
    
    def get_stats(self):
        """Get statistics about the retriever's knowledge base."""
        return self.vector_store.get_stats()
    
    def clear_knowledge(self):
        """Clear all stored knowledge - start fresh."""
        self.vector_store.clear()
        print("✓ All knowledge cleared. Ready for new information!\n")
