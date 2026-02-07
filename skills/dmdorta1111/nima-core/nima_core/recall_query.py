"""Query NIMA memories.

Usage:
    python3 -m nima_core.recall_query "search query" [--top-k 5] [--json-output]
"""

import argparse
import json
import sys
from typing import Any

from nima_core import NimaCore
from nima_core.config.auto import get_nima_config

__all__ = ["format_human_readable", "main"]


def format_human_readable(results: list[dict[str, Any]]) -> str:
    """Format recall results in a human-readable way."""
    if not results:
        return "No memories found."
    
    formatted = []
    for i, result in enumerate(results, 1):
        who = str(result.get('who', 'Unknown')).replace('\n', ' ')
        what = str(result.get('what', '')).replace('\n', ' ')
        importance = result.get('importance', 0)
        timestamp = result.get('timestamp', '')
        
        formatted.append(f"{i}. [{importance:.2f}] {who}: {what}")
        if timestamp:
            formatted.append(f"   Timestamp: {timestamp}")
        formatted.append("")
    
    return '\n'.join(formatted)


def main(argv=None) -> int:
    """Main entry point for querying memories.
    
    Args:
        argv: Command line arguments (defaults to sys.argv)
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("--json-output", action="store_true", dest="json_output", help="Output as JSON (default: human-readable)")
    parser.add_argument("--data-dir", help="Override data directory path")
    
    args = parser.parse_args(argv)
    
    if args.top_k < 1:
        parser.error("--top-k must be a positive integer")
    
    try:
        # Get configuration
        config = get_nima_config()
        if args.data_dir:
            config["data_dir"] = args.data_dir
        
        # Initialize NimaCore
        nima = NimaCore(
            name="CLI Recall",
            data_dir=config["data_dir"]
        )
        
        # Query memories
        results = nima.recall(args.query, top_k=args.top_k)
        
        # Output results
        if args.json_output:
            print(json.dumps(results, indent=2))
        else:
            print(format_human_readable(results))
        
        return 0
        
    except Exception as e:
        error_data = {"error": str(e)}
        print(json.dumps(error_data), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
