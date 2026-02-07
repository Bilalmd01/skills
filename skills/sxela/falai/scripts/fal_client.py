#!/usr/bin/env python3
"""
fal.ai API client for OpenClaw.
Handles queue-based requests with polling.

Usage:
  python fal_client.py submit <model_id> '<json_input>'
  python fal_client.py status <model_id> <request_id>
  python fal_client.py result <model_id> <request_id>
  python fal_client.py poll   # Poll all pending requests

Environment:
  FAL_KEY - API key (or reads from TOOLS.md)
"""

import os
import sys
import json
import time
import re
import requests
from pathlib import Path
from datetime import datetime

FAL_API_BASE = "https://queue.fal.run"
FAL_UPLOAD_URL = "https://fal.ai/api/storage/upload/initiate"
PENDING_FILE = Path(os.environ.get("FAL_PENDING_FILE", 
    Path.home() / ".openclaw/workspace/fal-pending.json"))
TOOLS_FILE = Path.home() / ".openclaw/workspace/TOOLS.md"

def get_api_key():
    """Get API key from env, openclaw.json, or TOOLS.md"""
    # 1. Environment variable (highest priority)
    key = os.environ.get("FAL_KEY")
    if key:
        return key
    
    # 2. OpenClaw config (integrations.fal.apiKey)
    config_file = Path.home() / ".openclaw/openclaw.json"
    if config_file.exists():
        try:
            config = json.loads(config_file.read_text())
            key = config.get("integrations", {}).get("fal", {}).get("apiKey")
            if key:
                return key
        except:
            pass
    
    # 3. TOOLS.md fallback
    if TOOLS_FILE.exists():
        content = TOOLS_FILE.read_text()
        # Look for FAL_KEY: xxx or fal.ai key: xxx patterns
        patterns = [
            r'FAL_KEY[:\s]+["\']?([a-zA-Z0-9_-]+)["\']?',
            r'fal\.ai.*key[:\s]+["\']?([a-zA-Z0-9_-]+)["\']?',
            r'fal.*api.*key[:\s]+["\']?([a-zA-Z0-9_-]+)["\']?',
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
    
    return None

def get_headers():
    key = get_api_key()
    if not key:
        print("ERROR: No FAL_KEY found. Set FAL_KEY env var or add to TOOLS.md:")
        print("  ### fal.ai")
        print("  FAL_KEY: your-key-here")
        sys.exit(1)
    return {
        "Authorization": f"Key {key}",
        "Content-Type": "application/json"
    }

def load_pending():
    """Load pending requests from file"""
    if PENDING_FILE.exists():
        try:
            return json.loads(PENDING_FILE.read_text())
        except:
            return {"requests": []}
    return {"requests": []}

def save_pending(data):
    """Save pending requests to file"""
    PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
    PENDING_FILE.write_text(json.dumps(data, indent=2))

def submit(model_id: str, input_data: dict) -> dict:
    """Submit a request to the queue"""
    url = f"{FAL_API_BASE}/{model_id}"
    resp = requests.post(url, headers=get_headers(), json=input_data)
    resp.raise_for_status()
    result = resp.json()
    
    # Add to pending
    pending = load_pending()
    pending["requests"].append({
        "request_id": result["request_id"],
        "model_id": model_id,
        "input": input_data,
        "status": "IN_QUEUE",
        "submitted_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    })
    save_pending(pending)
    
    return result

def get_base_model(model_id: str) -> str:
    """Extract base model path for queue URLs (fal-ai/flux/dev/image-to-image -> fal-ai/flux)"""
    parts = model_id.split('/')
    if len(parts) >= 2:
        return '/'.join(parts[:2])  # fal-ai/flux, fal-ai/nano-banana-pro, etc.
    return model_id

def check_status(model_id: str, request_id: str) -> dict:
    """Check status of a queued request"""
    base_model = get_base_model(model_id)
    url = f"{FAL_API_BASE}/{base_model}/requests/{request_id}/status"
    resp = requests.get(url, headers=get_headers())
    resp.raise_for_status()
    return resp.json()

def get_result(model_id: str, request_id: str) -> dict:
    """Get result of a completed request"""
    base_model = get_base_model(model_id)
    url = f"{FAL_API_BASE}/{base_model}/requests/{request_id}"
    resp = requests.get(url, headers=get_headers())
    resp.raise_for_status()
    return resp.json()

def poll_pending() -> list:
    """Poll all pending requests, return completed ones"""
    pending = load_pending()
    completed = []
    still_pending = []
    
    for req in pending["requests"]:
        try:
            status = check_status(req["model_id"], req["request_id"])
            req["status"] = status.get("status", "UNKNOWN")
            req["updated_at"] = datetime.utcnow().isoformat()
            
            if status.get("status") == "COMPLETED":
                # Fetch full result
                result = get_result(req["model_id"], req["request_id"])
                req["result"] = result
                completed.append(req)
            elif status.get("status") in ["FAILED", "CANCELLED"]:
                req["error"] = status.get("error", "Unknown error")
                completed.append(req)
            else:
                # Still in progress
                req["queue_position"] = status.get("queue_position")
                still_pending.append(req)
        except Exception as e:
            req["error"] = str(e)
            req["updated_at"] = datetime.utcnow().isoformat()
            still_pending.append(req)  # Keep trying
    
    # Update pending file
    pending["requests"] = still_pending
    save_pending(pending)
    
    return completed

def list_pending() -> list:
    """List all pending requests"""
    pending = load_pending()
    return pending["requests"]

def image_to_data_uri(file_path: str) -> str:
    """Convert local image to base64 data URI"""
    import base64
    import mimetypes
    
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "image/jpeg"
    
    with open(file_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    
    return f"data:{mime_type};base64,{data}"

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "submit":
        if len(sys.argv) < 4:
            print("Usage: fal_client.py submit <model_id> '<json_input>'")
            sys.exit(1)
        model_id = sys.argv[2]
        input_data = json.loads(sys.argv[3])
        result = submit(model_id, input_data)
        print(json.dumps(result, indent=2))
    
    elif cmd == "status":
        if len(sys.argv) < 4:
            print("Usage: fal_client.py status <model_id> <request_id>")
            sys.exit(1)
        result = check_status(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))
    
    elif cmd == "result":
        if len(sys.argv) < 4:
            print("Usage: fal_client.py result <model_id> <request_id>")
            sys.exit(1)
        result = get_result(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2))
    
    elif cmd == "poll":
        completed = poll_pending()
        print(json.dumps({"completed": completed, "count": len(completed)}, indent=2))
    
    elif cmd == "list":
        pending = list_pending()
        print(json.dumps({"pending": pending, "count": len(pending)}, indent=2))
    
    elif cmd == "check-key":
        key = get_api_key()
        if key:
            print(f"OK: Key found ({key[:8]}...)")
        else:
            print("ERROR: No key found")
            sys.exit(1)
    
    elif cmd == "to-data-uri":
        if len(sys.argv) < 3:
            print("Usage: fal_client.py to-data-uri <image_path>")
            sys.exit(1)
        uri = image_to_data_uri(sys.argv[2])
        print(uri)
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
