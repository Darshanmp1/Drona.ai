"""
Retriever Module - The brain that ties everything together

This module coordinates the embedder, vector store, and LLM to provide
intelligent retrieval and generation. It handles the workflow of:
1. Converting user queries to embeddings
2. Finding relevant stored information from Endee vector database
3. Generating natural language responses using LLaMA 3.2
"""

from .embedder import Embedder
from .vector_store import VectorStore
from ..llm.ollama_llm import OllamaLLM


class Retriever:
    def __init__(self, embedder=None, vector_store=None, use_llm=True):
        print("=" * 60)
        print("Initializing Drona AI Retriever (RAG with LLaMA 3.2)")
        print("=" * 60 + "\n")
        
        # The embedder converts text to vectors
        self.embedder = embedder if embedder is not None else Embedder()
        
        # The vector store keeps track of all our knowledge (Endee + fallback)
        self.vector_store = vector_store if vector_store is not None else VectorStore()
        
        # The LLM generates natural language responses
        self.use_llm = use_llm
        self.llm = None
        if use_llm:
            try:
                self.llm = OllamaLLM(model="llama3.2")
                if self.llm.is_available():
                    print("✓ LLaMA 3.2 connected via Ollama")
                else:
                    print("⚠ Ollama not running - responses will be retrieval-only")
                    print("  Tip: Start Ollama with 'ollama serve' for LLM generation\n")
            except Exception as e:
                print(f"⚠ Could not initialize LLM: {e}")
                print("  Continuing with retrieval-only mode\n")
        
        print("=" * 60)
        print("✓ Retriever ready! (Endee + LLaMA 3.2)")
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
    
    def add_document(self, text, metadata=None):
        texts = [text]
        metadatas = [metadata] if metadata is not None else None
        self.add_knowledge(texts, metadatas)
    
    def retrieve(self, query, top_k=3):
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
    
    def generate_response(self, query, top_k=3, use_llm=None):
        # Get relevant context from our knowledge base (Endee DB)
        results = self.retrieve(query, top_k=top_k)
        
        # Determine if we should use LLM
        should_use_llm = use_llm if use_llm is not None else self.use_llm
        
        # If we have results and LLM is available, generate natural response
        if results and should_use_llm and self.llm and self.llm.is_available():
            # Build context from retrieved documents
            context_parts = []
            for i, (text, score, metadata) in enumerate(results, 1):
                context_parts.append(f"[Document {i} - Relevance: {score:.2f}]\n{text}")
            
            context = "\n\n".join(context_parts)
            
            # Generate response using LLaMA 3.2
            print("🤖 Generating response with LLaMA 3.2...\n")
            response = self.llm.generate(
                prompt=query,
                context=context,
                max_tokens=500,
                temperature=0.7
            )
            
            return response
            
        # Fallback: Return formatted retrieval results if no LLM
        elif results:
            response = "Based on what I found (retrieval-only mode):\n\n"
            
            for i, (text, score, metadata) in enumerate(results, 1):
                response += f"{i}. [Relevance: {score:.2f}]\n"
                response += f"   {text}\n\n"
            
            response += "\n💡 Tip: Start Ollama with LLaMA 3.2 for AI-generated responses!"
            return response
            
        else:
            return "I don't have enough information to answer that yet. " \
                   "Try adding some knowledge to my database first!"
    
    def get_stats(self):
        return self.vector_store.get_stats()
    
    def clear_knowledge(self):
        self.vector_store.clear()
        print("✓ All knowledge cleared. Ready for new information!\n")
