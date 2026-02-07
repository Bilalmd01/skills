#!/usr/bin/env python3
"""
NIMA Heartbeat Service
======================
Generic background memory capture service.

Consumers provide a message_source function that returns new messages.
The service periodically calls it and processes through the NIMA pipeline.

Usage:
    from nima_core.services.heartbeat import NimaHeartbeat
    
    def my_source():
        return [{"who": "user", "what": "hello", "importance": 0.5}]
    
    heartbeat = NimaHeartbeat(nima, message_source=my_source, interval_minutes=10)
    heartbeat.start()  # Blocking
    # or
    heartbeat.start_background()  # Non-blocking thread

Author: NIMA Project
"""

import time
import signal
import logging
import threading
from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class NimaHeartbeat:
    """Generic heartbeat service for periodic memory capture."""
    
    def __init__(
        self,
        nima,  # NimaCore instance
        message_source: Optional[Callable[[], List[Dict]]] = None,
        interval_minutes: int = 10,
        consolidation_hour: int = 2,  # 2 AM
        markdown_dir: Optional[str] = None,
        markdown_export_path: Optional[str] = None,
        extra_markdown_files: Optional[List[str]] = None,
    ):
        """
        Args:
            nima: NimaCore instance
            message_source: Callable returning list of message dicts
            interval_minutes: Capture interval
            consolidation_hour: Hour for dream consolidation (0-23)
            markdown_dir: Directory with markdown memory files for bidirectional sync
            markdown_export_path: Where to export NIMA memories as markdown
            extra_markdown_files: Additional files to ingest (e.g. MEMORY.md)
        """
        self.nima = nima
        self.message_source = message_source
        self.interval = timedelta(minutes=interval_minutes)
        self.consolidation_hour = consolidation_hour
        self._shutdown = False
        self._thread = None
        
        # Markdown bridge config
        self.markdown_dir = markdown_dir
        self.markdown_export_path = markdown_export_path
        self.extra_markdown_files = extra_markdown_files
        self.last_capture = None
        self.last_consolidation = None
        self.stats = {"captures": 0, "memories_added": 0}
    
    def capture_once(self) -> Dict:
        """Run a single capture cycle."""
        if not self.message_source:
            return {"status": "no_source"}
        
        messages = self.message_source()
        added = 0
        for msg in messages:
            result = self.nima.experience(
                content=msg.get("what", ""),
                who=msg.get("who", "user"),
                importance=msg.get("importance", 0.5),
            )
            if result.get("stored"):
                added += 1
        
        self.last_capture = datetime.now()
        self.stats["captures"] += 1
        self.stats["memories_added"] += added
        
        # Export NIMA → markdown after capture (if configured)
        if added > 0 and self.markdown_export_path:
            try:
                from .markdown_bridge import MarkdownBridge
                bridge = MarkdownBridge(self.nima, agent_name=self.nima.name)
                bridge.export_to_markdown(self.markdown_export_path)
            except Exception as e:
                logger.debug(f"Markdown export skipped: {e}")
        
        logger.info(f"Heartbeat: {added}/{len(messages)} memories stored")
        return {"added": added, "total": len(messages)}
    
    def start(self):
        """Start heartbeat loop (blocking)."""
        logger.info(f"NIMA Heartbeat starting (interval={self.interval})")
        
        signal.signal(signal.SIGTERM, lambda s, f: setattr(self, '_shutdown', True))
        signal.signal(signal.SIGINT, lambda s, f: setattr(self, '_shutdown', True))
        
        # Initial capture
        self.capture_once()
        
        while not self._shutdown:
            now = datetime.now()
            
            # Check consolidation time
            if (now.hour == self.consolidation_hour and 
                now.minute < 10 and
                (self.last_consolidation is None or 
                 self.last_consolidation.date() != now.date())):
                
                # Ingest markdown → NIMA before consolidation
                if self.markdown_dir:
                    try:
                        from .markdown_bridge import MarkdownBridge
                        bridge = MarkdownBridge(self.nima, agent_name=self.nima.name)
                        result = bridge.sync(
                            markdown_dir=self.markdown_dir,
                            export_path=self.markdown_export_path or str(
                                Path(self.markdown_dir) / "nima_export.md"
                            ),
                            extra_files=self.extra_markdown_files,
                        )
                        logger.info(f"Markdown sync: {result['ingest']['added']} ingested, "
                                   f"{result['export']['memories_exported']} exported")
                    except Exception as e:
                        logger.warning(f"Markdown sync failed: {e}")
                
                logger.info("Running dream consolidation...")
                self.nima.dream()
                self.last_consolidation = now
            
            # Check capture interval
            if self.last_capture is None or (now - self.last_capture) >= self.interval:
                self.capture_once()
            
            time.sleep(60)
        
        logger.info("Heartbeat stopped")
    
    def start_background(self) -> threading.Thread:
        """Start heartbeat in background thread."""
        self._thread = threading.Thread(target=self.start, daemon=True)
        self._thread.start()
        return self._thread
    
    def stop(self):
        """Stop the heartbeat."""
        self._shutdown = True
