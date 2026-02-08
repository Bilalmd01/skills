"""NIMA Core cognition module."""
from .free_energy import FreeEnergyConsolidation, FreeEnergyResult, ConsolidationReason
from .schema_extractor import SchemaExtractor, Schema, SchemaConfig
from .temporal_encoder import TemporalEncoder, TemporalConfig, SequenceEncoding
from .sequence_predictor import SequenceCorpus, NextTurnPredictor
from .active_inference import ActiveInferenceEngine
from .hyperbolic_memory import HyperbolicTaxonomy
from .metacognitive import MetacognitiveLayer
from .dream_engine import DreamEngine, DreamSession, Insight, Pattern

__all__ = [
    "FreeEnergyConsolidation",
    "FreeEnergyResult",
    "ConsolidationReason",
    "SchemaExtractor",
    "Schema",
    "SchemaConfig",
    "TemporalEncoder",
    "TemporalConfig",
    "SequenceEncoding",
    "SequenceCorpus",
    "NextTurnPredictor",
    "ActiveInferenceEngine",
    "HyperbolicTaxonomy",
    "MetacognitiveLayer",
    "DreamEngine",
    "DreamSession",
    "Insight",
    "Pattern",
]
