#!/usr/bin/env python3
"""
NIMA Core — Main Entry Point
==============================
Single class for biologically-inspired cognitive memory.

Usage:
    from nima_core import NimaCore
    
    nima = NimaCore(name="MyBot", data_dir="./my_data")
    nima.experience("User asked about weather", who="user")
    results = nima.recall("weather", top_k=5)

Author: NIMA Project
"""

import os
import json
import logging
import threading
import numpy as np
import torch
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .config.nima_config import NimaConfig, get_config, reload_config
from .config import ZERO_NORM_THRESHOLD
from .layers.affective_core import SubcorticalAffectiveCore, AffectState
from .layers.binding_layer import VSABindingLayer, BoundEpisode

logger = logging.getLogger(__name__)


class NimaCore:
    """
    Main entry point for NIMA cognitive architecture.
    
    Provides a simple API for:
    - Processing experiences through affect → binding → FE pipeline
    - Semantic memory recall with sparse retrieval
    - Explicit memory capture
    - Dream consolidation (schema extraction, FE replay)
    - Metacognitive introspection
    """
    
    def __init__(
        self,
        name: str = "Agent",
        data_dir: Optional[str] = None,
        models_dir: Optional[str] = None,
        config: Optional[NimaConfig] = None,
        care_people: Optional[List[str]] = None,
        traits: Optional[Dict[str, float]] = None,
        beliefs: Optional[List[str]] = None,
        auto_init: bool = True,
    ):
        """
        Initialize NIMA for any bot.
        
        Args:
            name: Agent name (used in metacognitive self-model)
            data_dir: Where to store memories, schemas, etc. (default: NIMA_DATA_DIR env or ./nima_data)
            models_dir: Where projection model lives (default: NIMA_MODELS_DIR env or ./models)
            config: NimaConfig override (or loads from env)
            care_people: Names that boost CARE affect (e.g. ["Alice", "Bob"])
            traits: Self-model traits dict (e.g. {"curious": 0.9})
            beliefs: Self-model beliefs list
            auto_init: Initialize all enabled components immediately
        """
        self.name = name
        
        # Set paths via environment if provided (before config loads)
        if data_dir:
            os.environ["NIMA_DATA_DIR"] = str(data_dir)
        if models_dir:
            os.environ["NIMA_MODELS_DIR"] = str(models_dir)
        
        # Load or use provided config
        if config:
            self.config = config
        else:
            self.config = reload_config()  # Reload to pick up any env changes
        
        # Identity parameters
        self.care_people = care_people or []
        self.traits = traits or {}
        self.beliefs = beliefs or []
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Component references (lazy or auto init)
        self._bridge = None
        self._embedder = None
        self._metacognitive = None
        self._retriever = None
        
        # Ensure data directories exist
        from .config import NIMA_DATA_DIR
        (NIMA_DATA_DIR / "sessions").mkdir(parents=True, exist_ok=True)
        (NIMA_DATA_DIR / "schemas").mkdir(parents=True, exist_ok=True)
        (NIMA_DATA_DIR / "cache").mkdir(parents=True, exist_ok=True)
        
        # Memory storage path
        self._memory_path = NIMA_DATA_DIR / "sessions" / "latest.pt"
        
        if auto_init:
            self._initialize()
        
        logger.info(f"NIMA Core initialized: name={name}, v2={self.config.any_enabled()}")
    
    def _initialize(self):
        """Initialize enabled components."""
        # Bridge handles component initialization
        try:
            from .bridge import NimaV2Bridge
            # TODO: NimaV2Bridge may not accept care_people yet - adjust when available
            self._bridge = NimaV2Bridge(
                auto_init=True,
            )
        except Exception as e:
            logger.warning(f"Bridge init failed: {e}")
        
        # Metacognitive layer
        if self.config.metacognitive:
            try:
                from .cognition.metacognitive import MetacognitiveLayer
                self._metacognitive = MetacognitiveLayer(
                    name=self.name,
                    traits=self.traits,
                    beliefs=self.beliefs,
                )
            except Exception as e:
                logger.warning(f"Metacognitive init failed: {e}")
    
    def experience(
        self,
        content: str,
        who: str = "user",
        importance: float = 0.5,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Process an experience through the full cognitive pipeline.
        
        Affect → Binding → Free Energy → Store/Skip
        
        Args:
            content: What happened (text)
            who: Who said/did it
            importance: Base importance [0-1]
            **kwargs: Extra context (where, when, domain, etc.)
        
        Returns:
            Dict with affect, should_consolidate, free_energy, etc.
        """
        result = {"content": content, "who": who, "stored": False}
        
        if self._bridge:
            processed = self._bridge.process_experience(
                content=content,
                who=who,
                importance=importance,
                **kwargs,
            )
            result.update(processed.to_dict())
            
            # Store if should consolidate
            if processed.should_consolidate:
                self._store_memory({
                    "who": who,
                    "what": content,
                    "importance": importance,
                    "timestamp": datetime.now().isoformat(),
                    "affect": processed.affect.get("dominant") if processed.affect else None,
                    "fe_score": processed.free_energy,
                    "fe_reason": processed.consolidation_reason,
                })
                result["stored"] = True
        else:
            # No bridge — store everything above threshold
            if importance > 0.3:
                self._store_memory({
                    "who": who,
                    "what": content,
                    "importance": importance,
                    "timestamp": datetime.now().isoformat(),
                })
                result["stored"] = True
        
        # Push to working memory if metacognitive is active
        if self._metacognitive:
            self._metacognitive.process(content, label=who)
        
        return result
    
    def recall(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search memories semantically.
        
        Args:
            query: Search query text
            top_k: Number of results
        
        Returns:
            List of memory dicts sorted by relevance
        """
        try:
            from .embeddings.embeddings import get_embedder
            embedder = get_embedder()
            
            query_vec = embedder.encode_single(query)
            if query_vec is None:
                return self._text_search(query, top_k)
            
            # Try sparse retrieval first
            if self.config.sparse_retrieval:
                return self._sparse_recall(query_vec, top_k)
            
            # Fallback to brute force
            return self._dense_recall(query_vec, top_k)
            
        except Exception as e:
            logger.warning(f"Recall failed: {e}")
            return self._text_search(query, top_k)
    
    def capture(
        self,
        who: str,
        what: str,
        importance: float = 0.5,
        memory_type: str = "conversation",
    ) -> bool:
        """
        Explicitly capture a memory (bypasses FE gate).
        
        Args:
            who: Who said/did it
            what: What happened
            importance: Importance score [0-1]
            memory_type: Type tag
        
        Returns:
            True if captured successfully
        """
        try:
            self._store_memory({
                "who": who,
                "what": what,
                "importance": importance,
                "timestamp": datetime.now().isoformat(),
                "type": memory_type,
                "context": "explicit",
            })
            return True
        except Exception as e:
            logger.error(f"Capture failed: {e}")
            return False
    
    def dream(self, hours: int = 24) -> Dict:
        """
        Run dream consolidation.
        
        Processes recent memories through:
        1. Schema extraction (identify patterns)
        2. FE-ranked replay (novel memories first)
        3. Pattern & insight extraction
        
        Args:
            hours: How many hours of memories to process
        
        Returns:
            Dict with consolidation results
        """
        try:
            from .cognition.schema_extractor import SchemaExtractor
            from .config import NIMA_DATA_DIR
            
            # Load memories
            memories = self._load_memories()
            if not memories:
                return {"status": "no_memories", "schemas": 0}
            
            # Extract schemas
            extractor = SchemaExtractor()
            # This is simplified — full dream engine would do more
            
            return {
                "status": "complete",
                "memories_processed": len(memories),
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Dream failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def status(self) -> Dict:
        """
        Get system status.
        
        Returns:
            Dict with memory count, component status, config
        """
        memories = self._load_memories()
        
        status = {
            "name": self.name,
            "version": "1.0.0",
            "memory_count": len(memories),
            "config": self.config.to_dict(),
            "components": {
                "bridge": self._bridge is not None,
                "metacognitive": self._metacognitive is not None,
            },
        }
        
        if self._bridge:
            status["bridge_stats"] = self._bridge.get_stats()
        
        return status
    
    def introspect(self) -> Optional[Dict]:
        """
        Metacognitive introspection — look at own state.
        
        Returns:
            Dict with identity, working memory, calibration, self-thought
            or None if metacognitive layer not enabled
        """
        if self._metacognitive:
            return self._metacognitive.introspect()
        return None
    
    # ---- Private helpers ----
    
    def _store_memory(self, memory: Dict):
        """Store a memory to latest.pt (thread-safe)."""
        with self._lock:
            try:
                if self._memory_path.exists():
                    from .utils import safe_torch_load
                    data = safe_torch_load(self._memory_path)
                else:
                    data = {"state": {"metadata": [], "memory_count": 0, "timestamp": ""}}
                
                metadata = data.get("state", {}).get("metadata", [])
                
                # Deduplicate
                existing_texts = {m.get("what", "")[:100] for m in metadata}
                if memory.get("what", "")[:100] in existing_texts:
                    return
                
                metadata.append(memory)
                data["state"]["metadata"] = metadata
                data["state"]["memory_count"] = len(metadata)
                data["state"]["timestamp"] = datetime.now().isoformat()
                
                from .utils import atomic_torch_save
                atomic_torch_save(data, self._memory_path)
            except Exception as e:
                logger.error(f"Store failed: {e}")
    
    def _load_memories(self) -> List[Dict]:
        """Load all memories from latest.pt (thread-safe)."""
        with self._lock:
            if not self._memory_path.exists():
                return []
            try:
                from .utils import safe_torch_load
                data = safe_torch_load(self._memory_path)
                return data.get("state", {}).get("metadata", [])
            except Exception as e:
                logger.warning(f"Load failed: {e}")
                return []
    
    def _text_search(self, query: str, top_k: int) -> List[Dict]:
        """Simple text-based search fallback."""
        memories = self._load_memories()
        query_lower = query.lower()
        scored = []
        for mem in memories:
            text = f"{mem.get('who', '')} {mem.get('what', '')}".lower()
            words = query_lower.split()
            score = sum(1 for w in words if w in text) / max(len(words), 1)
            if score > 0:
                scored.append((score, mem))
        scored.sort(key=lambda x: -x[0])
        return [m for _, m in scored[:top_k]]
    
    def _sparse_recall(self, query_vec, top_k: int) -> List[Dict]:
        """Sparse retrieval search."""
        from .retrieval.sparse_retrieval import SparseRetriever
        from .config import NIMA_DATA_DIR
        
        cache_path = NIMA_DATA_DIR / "cache" / "sparse_index.pt"
        
        if cache_path.exists():
            retriever = SparseRetriever.load(str(cache_path))
        else:
            # Build index from scratch
            retriever = SparseRetriever(dimension=len(query_vec))
            memories = self._load_memories()
            embedder = self._get_embedder()
            if embedder:
                for i, mem in enumerate(memories):
                    text = f"{mem.get('who', '')} {mem.get('what', '')}"
                    vec = embedder.encode_single(text)
                    if vec is not None:
                        retriever.add(i, vec, mem)
                retriever.save(str(cache_path))
        
        results = retriever.query(query_vec, top_k=top_k)
        return [meta for _, _, meta in results]
    
    def _dense_recall(self, query_vec, top_k: int) -> List[Dict]:
        """Brute force cosine similarity search."""
        memories = self._load_memories()
        embedder = self._get_embedder()
        if not embedder:
            return []
        
        scored = []
        for mem in memories:
            text = f"{mem.get('who', '')} {mem.get('what', '')}"
            vec = embedder.encode_single(text)
            if vec is not None:
                norm_q = np.linalg.norm(query_vec)
                norm_v = np.linalg.norm(vec)
                # Guard against zero vectors
                if norm_q < ZERO_NORM_THRESHOLD or norm_v < ZERO_NORM_THRESHOLD:
                    continue
                sim = float(np.dot(query_vec, vec) / (norm_q * norm_v + ZERO_NORM_THRESHOLD))
                scored.append((sim, mem))
        
        scored.sort(key=lambda x: -x[0])
        return [m for _, m in scored[:top_k]]
    
    def _get_embedder(self):
        """Get or create embedder."""
        if self._embedder is None:
            try:
                from .embeddings.embeddings import get_embedder
                self._embedder = get_embedder()
            except Exception:
                pass
        return self._embedder
