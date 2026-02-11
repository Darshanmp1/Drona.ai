"""
Embedder Module - Converts text into numerical vectors (embeddings)

Think of embeddings like coordinates that represent the "meaning" of text.
Similar texts will have similar coordinates, which lets us find related information.
"""

from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print(f"Loading embedding model: {model_name}")
        print("This might take a moment on first run (downloading model)...")
        
        # Load the pre-trained sentence transformer model
        self.model = SentenceTransformer(model_name)
        
        # Get the size of the embedding vectors this model produces
        self.embedding_size = self.model.get_sentence_embedding_dimension()
        
        print(f"✓ Model loaded! Each text will become a vector of {self.embedding_size} numbers.\n")
    
    def embed_text(self, text):
        # The model does the heavy lifting here - it understands the text
        # and converts it to a meaningful numerical representation
        embedding = self.model.encode(text, convert_to_numpy=True)
        
        return embedding
    
    def embed_batch(self, texts):
        # Batch processing is more efficient - the model can optimize
        # when it processes multiple texts together
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        
        return embeddings
    
    def get_embedding_size(self):
        return self.embedding_size
