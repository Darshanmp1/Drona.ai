"""
Embedder Module - Converts text into numerical vectors (embeddings)

Think of embeddings like coordinates that represent the "meaning" of text.
Similar texts will have similar coordinates, which lets us find related information.
"""

from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    """
    The Embedder takes text and turns it into a vector of numbers.
    We use a pre-trained model that already knows how to capture meaning from text.
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the embedder with a specific model.
        
        We're using 'all-MiniLM-L6-v2' because:
        - It's lightweight and fast
        - Good balance between quality and speed
        - Works well for general text understanding
        """
        print(f"Loading embedding model: {model_name}")
        print("This might take a moment on first run (downloading model)...")
        
        # Load the pre-trained sentence transformer model
        self.model = SentenceTransformer(model_name)
        
        # Get the size of the embedding vectors this model produces
        self.embedding_size = self.model.get_sentence_embedding_dimension()
        
        print(f"✓ Model loaded! Each text will become a vector of {self.embedding_size} numbers.\n")
    
    def embed_text(self, text):
        """
        Convert a single piece of text into an embedding.
        
        Args:
            text: The text string you want to convert
            
        Returns:
            A numpy array representing the text as numbers
        """
        # The model does the heavy lifting here - it understands the text
        # and converts it to a meaningful numerical representation
        embedding = self.model.encode(text, convert_to_numpy=True)
        
        return embedding
    
    def embed_batch(self, texts):
        """
        Convert multiple texts into embeddings at once.
        This is faster than converting them one by one.
        
        Args:
            texts: A list of text strings
            
        Returns:
            A numpy array where each row is an embedding
        """
        # Batch processing is more efficient - the model can optimize
        # when it processes multiple texts together
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        
        return embeddings
    
    def get_embedding_size(self):
        """
        Returns the size of the embedding vectors.
        Useful when setting up the vector store.
        """
        return self.embedding_size
