---
name: seisoai
description: AI media generation. 50+ tools for images, videos, music, audio, 3D, speech. x402 pay-per-request on Base. Highly optimized for agentic workflows.
metadata: {"openclaw":{"homepage":"https://seisoai.com","emoji":"🎨"}}
---

# Seisoai

**Base:** `https://seisoai.com`  
**Endpoint:** `POST /api/gateway/invoke/{toolId}`  
**Auth:** `X-API-Key: sk_live_...` or x402 payment

**Optimized for agentic, pay-per-job workflows.** Each tool call is stateless—no sessions, no accounts required. Perfect for AI agents that need to generate media on demand.

---

## Quick Start

```http
POST https://seisoai.com/api/gateway/invoke/image.generate.flux-2
Content-Type: application/json
X-API-Key: sk_live_xxx

{"prompt": "a sunset over mountains"}
```

That's it. Just `prompt` and you get an image. One API call = one job = one payment.

---

## Tools (50+)

### Image Generation

| Task | toolId | Just need |
|------|--------|-----------|
| Image (fast) | `image.generate.flux-2` | `prompt` |
| Image (cinematic) | `image.generate.kling-image-v3` | `prompt` |
| Image (aesthetic) | `image.generate.grok-imagine` | `prompt` |
| Image (consistent) | `image.generate.kling-image-o3` | `prompt` |
| Image (360°) | `image.generate.nano-banana-pro` | `prompt` |
| Edit image | `image.generate.flux-pro-kontext` | `prompt` + `image_url` |
| Face swap | `image.face-swap` | `source_image_url` + `target_image_url` |
| Remove BG | `image.extract-layer` | `image_url` |
| Upscale | `image.upscale` | `image_url` |

### Video Generation

| Task | toolId | Just need |
|------|--------|-----------|
| Video (fast) | `video.generate.ltx-2` | `prompt` |
| Video (quality) | `video.generate.veo3` | `prompt` |
| Video (cinematic) | `video.generate.kling-3-pro-text` | `prompt` |
| Video (stylized) | `video.generate.grok-imagine-text` | `prompt` |
| Animate image | `video.generate.kling-3-pro-image` | `prompt` + `image_url` |
| Motion transfer | `video.generate.dreamactor-v2` | `source_url` + `driver_url` |

### Audio & Speech

| Task | toolId | Just need |
|------|--------|-----------|
| Music | `music.generate` | `prompt` |
| Sound FX | `audio.sfx` | `prompt` |
| TTS (voice clone) | `audio.tts` | `text` + `voice_url` |
| TTS (high quality) | `audio.tts.minimax-hd` | `text` |
| TTS (fast) | `audio.tts.minimax-turbo` | `text` |
| Transcribe | `audio.transcribe` | `audio_url` |

### 3D Generation

| Task | toolId | Just need |
|------|--------|-----------|
| 3D from image | `3d.image-to-3d.hunyuan-pro` | `image_url` |
| 3D from text | `3d.text-to-3d.hunyuan-pro` | `prompt` |
| 3D (fast) | `3d.image-to-3d.hunyuan-rapid` | `image_url` |

---

## Why Seisoai for Agents?

**Pay-per-job**: Each API call is billed independently. No subscriptions, no credits to manage.

**Stateless**: No sessions, no auth tokens to refresh. Just API key or x402 signature per request.

**Smart defaults**: Most tools only need `prompt`. We handle model selection, sizing, and optimization.

**50+ tools**: One endpoint, unified interface. Your agent doesn't need to integrate multiple APIs.

**Fast routing**: Automatic model selection based on task. Ask for "cinematic video" and we route to Kling 3.0 Pro.

---

## Flexible Input

The API normalizes your input automatically:

| You send | We accept |
|----------|-----------|
| `"imageUrl"` | → `image_url` |
| `"sourceImageUrl"` | → `source_image_url` |
| `"numImages"` | → `num_images` |
| `"generateAudio"` | → `generate_audio` |
| `"duration": "60"` | → `60` (number) |
| `"duration": 60` | → `"60s"` (string, for video) |

**camelCase or snake_case** — both work.  
**Strings or numbers** — we coerce to the right type.  
**Missing defaults** — we apply them from the schema.

---

## Common Options

**Image:** `image_size` (square, landscape_16_9, portrait_16_9), `num_images` (1-4)

**Video:** `duration` (4s, 6s, 8s, 10s), `generate_audio` (true/false)

**Music:** `duration` (10-180 seconds)

**3D:** `format` (glb, obj, fbx)

---

## Response

```json
{
  "success": true,
  "result": {
    "images": [{"url": "https://..."}]
  }
}
```

- Images: `result.images[0].url`
- Video: `result.video.url`
- Audio/Music: `result.audio_file.url`
- 3D: `result.model_mesh.url`

---

## Auth Options

**API Key** (easiest): Get at `https://seisoai.com/settings/api-keys`, add header `X-API-Key: sk_live_...`

**x402** (agentic): No key needed. First call returns 402 with payment details, sign USDC on Base, retry with signature. Perfect for autonomous agents with wallets.

---

## Pricing (Pay-per-job)

| Category | Cost |
|----------|------|
| Image (standard) | ~$0.03-0.05 |
| Image (premium) | ~$0.04-0.065 |
| Video (per second) | ~$0.10-0.20 |
| Music (per minute) | ~$0.02 |
| TTS | ~$0.02-0.04 |
| 3D | ~$0.04-0.15 |

All prices include 30% markup over raw API costs. x402 payments are in USDC on Base.

---

## Errors

| Code | Meaning |
|------|---------|
| 400 | Missing required field (usually just `prompt`) |
| 402 | Add API key or sign payment |
| 500 | Retry |

---

## Discovery

```
GET /api/gateway/tools
```

Returns all 50+ tools with JSON schemas. For agents, use this to discover available capabilities dynamically.
