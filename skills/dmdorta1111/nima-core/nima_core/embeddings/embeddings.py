#!/usr/bin/env python3
"""
Unified Embeddings Loader
=========================
Single cached load of sentence-transformers to avoid multiple slow loads.
Now with learned projection for energy-concentrated embeddings.

All modules should import from here instead of loading their own.

Author: NIMA Project
Date: 2026
Updated: 2026 - Added learned projection layer (Phase 1 integration)
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Union
import threading
import numpy as np

# Suppress tokenizers parallelism warnings (prevents deadlocks with multiprocessing)
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# Import config paths
from ..config import NIMA_MODELS_DIR

# Singleton state
_embedder = None
_embedder_lock = threading.Lock()
_model_name = "sentence-transformers/all-MiniLM-L6-v2"
_embedding_dim = 384
_projected_dim = 50000

# Learned projection paths
_projection_path = NIMA_MODELS_DIR / "learned_projection.pt"

# Feature flag for projection (can be overridden via env)
ENABLE_PROJECTION = os.environ.get("NIMA_PROJECTION", "true").lower() == "true"


class EmbeddingCache:
    """
    Cached embedding generator with optional learned projection.
    
    Loads sentence-transformers ONCE and reuses across all modules.
    Thread-safe singleton pattern.
    
    With projection enabled:
        text → MiniLM (384D) → W (50KD, concentrated)
    """
    
    def __init__(self, model_name: str = None, enable_projection: bool = None):
        self.model_name = model_name or _model_name
        self.model = None
        self.dimension = _embedding_dim
        self._loaded = False
        
        # Projection settings
        self.enable_projection = enable_projection if enable_projection is not None else ENABLE_PROJECTION
        self.projection_matrix = None  # W: (50K, 384)
        self._projection_loaded = False
        
    def _ensure_loaded(self):
        """Load model if not already loaded."""
        if self._loaded:
            return
            
        try:
            from sentence_transformers import SentenceTransformer
            print(f"📦 Loading embeddings model (cached): {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
            self._loaded = True
            print(f"✅ Embeddings ready (dim={self.dimension})")
            
            # Load projection if enabled
            if self.enable_projection:
                self._load_projection()
                
        except ImportError:
            print("⚠️ sentence-transformers not installed")
            self._loaded = False
        except Exception as e:
            print(f"⚠️ Embeddings load failed: {e}")
            self._loaded = False
    
    def _load_projection(self):
        """Load the learned projection matrix."""
        if self._projection_loaded:
            return
            
        if not _projection_path.exists():
            print(f"⚠️ Projection not found: {_projection_path}")
            print("   Running without projection (raw 384D embeddings)")
            self.enable_projection = False
            return
            
        try:
            from ..utils import safe_torch_load
            checkpoint = safe_torch_load(_projection_path)
            
            # Extract weight matrix from state dict
            if 'model_state_dict' in checkpoint:
                W = checkpoint['model_state_dict']['W.weight']
            else:
                W = checkpoint.get('W.weight', checkpoint)
            
            # Convert to numpy for fast CPU inference
            self.projection_matrix = W.numpy()  # Shape: (50K, 384)
            
            # CRITICAL: Free PyTorch tensors to prevent 76MB leak
            del W
            del checkpoint
            
            self._projection_loaded = True
            self.dimension = self.projection_matrix.shape[0]  # Now 50K
            
            print(f"🎯 Learned projection loaded: 384 → {self.dimension}D (concentrated)")
            
        except Exception as e:
            print(f"⚠️ Projection load failed: {e}")
            print("   Running without projection")
            self.enable_projection = False
    
    def _apply_projection(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Apply learned projection to concentrate energy.
        
        Args:
            embeddings: (N, 384) array
            
        Returns:
            (N, 50K) concentrated embeddings
        """
        if self.projection_matrix is None:
            return embeddings
            
        # W @ e.T = (50K, 384) @ (384, N) = (50K, N)
        projected = np.dot(embeddings, self.projection_matrix.T)  # (N, 50K)
        return projected
    
    def encode(self, texts: List[str], apply_projection: bool = True, **kwargs) -> Optional[np.ndarray]:
        """
        Encode texts to embeddings, optionally with learned projection.
        
        Args:
            texts: List of strings to encode
            apply_projection: Whether to apply learned projection (default True)
            **kwargs: Passed to model.encode()
            
        Returns:
            Numpy array of embeddings (N, D) where D=50K if projected, 384 otherwise
            Returns None if model not loaded
        """
        self._ensure_loaded()
        
        if not self._loaded or self.model is None:
            return None
            
        try:
            # Get base embeddings (384D)
            embeddings = self.model.encode(texts, **kwargs)
            
            if not isinstance(embeddings, np.ndarray):
                embeddings = np.array(embeddings)
            
            # Apply projection if enabled
            if apply_projection and self.enable_projection and self._projection_loaded:
                embeddings = self._apply_projection(embeddings)
            
            return embeddings
            
        except Exception as e:
            print(f"⚠️ Encoding failed: {e}")
            return None
    
    def encode_raw(self, texts: List[str], **kwargs) -> Optional[np.ndarray]:
        """Encode texts WITHOUT projection (raw 384D)."""
        return self.encode(texts, apply_projection=False, **kwargs)
    
    def encode_single(self, text: str, apply_projection: bool = True, **kwargs) -> Optional[np.ndarray]:
        """Encode a single text, optionally with projection."""
        result = self.encode([text], apply_projection=apply_projection, **kwargs)
        return result[0] if result is not None else None
    
    @property
    def is_loaded(self) -> bool:
        return self._loaded
    
    @property
    def is_projected(self) -> bool:
        """Whether projection is active."""
        return self._projection_loaded and self.enable_projection
    
    @property
    def output_dimension(self) -> int:
        """Get the output embedding dimension (384 raw, 50K projected)."""
        self._ensure_loaded()  # Must load to know actual dimension
        if self.is_projected and self.projection_matrix is not None:
            return self.projection_matrix.shape[0]
        return _embedding_dim


def get_embedder() -> EmbeddingCache:
    """
    Get the singleton embedder instance.
    
    Thread-safe. All modules should use this instead of creating their own.
    
    Returns:
        EmbeddingCache instance
    """
    global _embedder
    
    if _embedder is None:
        with _embedder_lock:
            if _embedder is None:  # Double-check
                _embedder = EmbeddingCache()
    
    return _embedder


def preload():
    """
    Preload the embeddings model.
    
    Call at startup to avoid first-use delay.
    """
    embedder = get_embedder()
    embedder._ensure_loaded()


# Convenience functions
def encode(texts: List[str], apply_projection: bool = True, **kwargs) -> Optional[np.ndarray]:
    """Encode texts using the cached embedder (with projection by default)."""
    return get_embedder().encode(texts, apply_projection=apply_projection, **kwargs)


def encode_raw(texts: List[str], **kwargs) -> Optional[np.ndarray]:
    """Encode texts WITHOUT projection (raw 384D)."""
    return get_embedder().encode_raw(texts, **kwargs)


def encode_single(text: str, apply_projection: bool = True, **kwargs) -> Optional[np.ndarray]:
    """Encode single text using the cached embedder."""
    return get_embedder().encode_single(text, apply_projection=apply_projection, **kwargs)


def get_dimension() -> int:
    """Get output embedding dimension (50K if projected, 384 raw)."""
    embedder = get_embedder()
    embedder._ensure_loaded()  # Must load to know actual dimension
    return embedder.output_dimension


def get_raw_dimension() -> int:
    """Get raw embedding dimension (always 384)."""
    return _embedding_dim


def is_projection_enabled() -> bool:
    """Check if projection is active."""
    embedder = get_embedder()
    embedder._ensure_loaded()  # Must load to know if projection worked
    return embedder.is_projected


if __name__ == "__main__":
    # Test
    print("=" * 60)
    print("Testing unified embeddings with learned projection")
    print("=" * 60)
    
    preload()
    
    # Test with projection
    print("\n📊 With projection:")
    result = encode_single("Hello, this is a test sentence.")
    if result is not None:
        print(f"   Dimension: {len(result)}")
        print(f"   Projection enabled: {is_projection_enabled()}")
        
        # Check energy concentration
        energy = result ** 2
        total = energy.sum()
        top_10_pct = int(len(result) * 0.1)
        top_indices = np.argsort(energy)[-top_10_pct:]
        top_energy = energy[top_indices].sum()
        concentration = top_energy / total
        print(f"   Energy concentration (top 10%): {concentration*100:.1f}%")
    
    # Test without projection
    print("\n📊 Without projection (raw):")
    result_raw = encode_single("Hello, this is a test sentence.", apply_projection=False)
    if result_raw is not None:
        print(f"   Dimension: {len(result_raw)}")
    
    # Batch test
    print("\n📊 Batch encoding:")
    texts = ["First sentence", "Second sentence", "Third sentence"]
    batch_result = encode(texts)
    if batch_result is not None:
        print(f"   Shape: {batch_result.shape}")
    
    print("\n✅ Unified embeddings with projection working!")
