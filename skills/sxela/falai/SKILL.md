---
name: fal-ai
description: Generate images and media using fal.ai API (Flux, Gemini image, etc.). Use when asked to generate images, run AI image models, create visuals, or anything involving fal.ai. Handles queue-based requests with automatic polling.
---

# fal.ai Integration

Generate and edit images via fal.ai's queue-based API.

## Setup

Add your API key to `TOOLS.md`:

```markdown
### fal.ai
FAL_KEY: your-key-here
```

Get a key at: https://fal.ai/dashboard/keys

The script checks (in order): `FAL_KEY` env var → `TOOLS.md`

## Supported Models

### fal-ai/nano-banana-pro (Text → Image)
Google's Gemini 3 Pro for text-to-image generation.

```python
input_data = {
    "prompt": "A cat astronaut on the moon",      # required
    "aspect_ratio": "1:1",                        # auto|21:9|16:9|3:2|4:3|5:4|1:1|4:5|3:4|2:3|9:16
    "resolution": "1K",                           # 1K|2K|4K
    "output_format": "png",                       # jpeg|png|webp
    "safety_tolerance": "4"                       # 1 (strict) to 6 (permissive)
}
```

### fal-ai/nano-banana-pro/edit (Image → Image)
Gemini 3 Pro for image editing. Slower (~20s) but handles complex edits well.

```python
input_data = {
    "prompt": "Transform into anime style",       # required
    "image_urls": [image_data_uri],               # required - array of URLs or base64 data URIs
    "aspect_ratio": "auto",
    "resolution": "1K",
    "output_format": "png"
}
```

### fal-ai/flux/dev/image-to-image (Image → Image)
FLUX.1 dev model. Faster (~2-3s) for style transfers.

```python
input_data = {
    "prompt": "Anime style portrait",             # required
    "image_url": image_data_uri,                  # required - single URL or base64 data URI
    "strength": 0.85,                             # 0-1, higher = more change
    "num_inference_steps": 40,
    "guidance_scale": 7.5,
    "output_format": "png"
}
```

## Usage

### CLI Commands

```bash
# Check API key
python3 scripts/fal_client.py check-key

# Submit a request
python3 scripts/fal_client.py submit "fal-ai/nano-banana-pro" '{"prompt": "A sunset over mountains"}'

# Check status
python3 scripts/fal_client.py status "fal-ai/nano-banana-pro" "<request_id>"

# Get result
python3 scripts/fal_client.py result "fal-ai/nano-banana-pro" "<request_id>"

# Poll all pending requests
python3 scripts/fal_client.py poll

# List pending requests
python3 scripts/fal_client.py list

# Convert local image to base64 data URI
python3 scripts/fal_client.py to-data-uri /path/to/image.jpg
```

### Python Usage

```python
import sys
sys.path.insert(0, 'scripts')
from fal_client import submit, check_status, get_result, image_to_data_uri, poll_pending

# Text to image
result = submit('fal-ai/nano-banana-pro', {
    'prompt': 'A futuristic city at night'
})
print(result['request_id'])

# Image to image (with local file)
img_uri = image_to_data_uri('/path/to/photo.jpg')
result = submit('fal-ai/nano-banana-pro/edit', {
    'prompt': 'Transform into watercolor painting',
    'image_urls': [img_uri]
})

# Poll until complete
completed = poll_pending()
for req in completed:
    if 'result' in req:
        print(req['result']['images'][0]['url'])
```

## Queue System

fal.ai uses async queues. Requests go through stages:
- `IN_QUEUE` → waiting
- `IN_PROGRESS` → generating
- `COMPLETED` → done, fetch result
- `FAILED` → error occurred

Pending requests are saved to `~/. openclaw/workspace/fal-pending.json` and survive restarts.

### Polling Strategy

**Manual:** Run `python3 scripts/fal_client.py poll` periodically.

**Heartbeat:** Add to `HEARTBEAT.md`:
```markdown
- Poll fal.ai pending requests if any exist
```

**Cron:** Schedule polling every few minutes for background jobs.

## Adding New Models

1. Find the model on fal.ai and check its `/api` page
2. Add entry to `references/models.json` with input/output schema
3. Test with a simple request

**Note:** Queue URLs use base model path (e.g., `fal-ai/flux` not `fal-ai/flux/dev/image-to-image`). The script handles this automatically.

## Files

```
skills/fal-ai/
├── SKILL.md                    ← This file
├── scripts/
│   └── fal_client.py           ← CLI + Python library
└── references/
    └── models.json             ← Model schemas
```

## Troubleshooting

**"No FAL_KEY found"** → Add key to TOOLS.md or set FAL_KEY env var

**405 Method Not Allowed** → URL routing issue, ensure using base model path for status/result

**Request stuck** → Check `fal-pending.json`, may need manual cleanup
