"""
RAG (Retrieval-Augmented Generation) module.

This module provides the core components for RAG:
- Embedder: Converts text to vector embeddings
- VectorStore: Stores and searches embeddings (with Endee DB support)
- Retriever: Retrieves relevant documents for queries
- EndeeClient: Client for Endee vector database backend
"""

from .embedder import Embedder
from .vector_store import VectorStore
from .retriever import Retriever
from .endee_client import EndeeClient

__all__ = ['Embedder', 'VectorStore', 'Retriever', 'EndeeClient']
