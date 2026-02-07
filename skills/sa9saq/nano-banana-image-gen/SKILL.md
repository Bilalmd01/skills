---
name: nano-banana-image-gen
description: AI image generation using Google Gemini API (Gemini 2.0 Flash). Generate SNS thumbnails, article images, banners, and more. Supports Japanese text rendering in images. Use when user says "generate image", "create thumbnail", "make banner", "image generation", or "Nano Banana".
---

# Nano Banana Image Gen

AI-powered image generation using Google Gemini API. Create SNS thumbnails, article cover images, banners, and promotional graphics with Japanese text support.

## Features

- **Gemini API**: Uses Gemini 2.0 Flash for high-quality image generation
- **Japanese text rendering**: Native support for Japanese text in generated images
- **Multiple aspect ratios**: 16:9 (thumbnails), 1:1 (SNS), 9:16 (stories)
- **Batch generation**: Generate multiple variations at once
- **Auto-save**: Output to specified directory with organized naming

## Quick Start

```bash
# Set API key
export GOOGLE_AI_API_KEY=your_key

# Generate an image
python3 {skill_dir}/generate.py \
  --prompt "A futuristic Tokyo cityscape at sunset" \
  --output "./output.png" \
  --aspect 16:9

# Generate SNS thumbnail
python3 {skill_dir}/generate.py \
  --prompt "仮想通貨AIトレーディング解説記事のサムネイル" \
  --output "./thumbnail.png" \
  --aspect 16:9

# Generate with text overlay
python3 {skill_dir}/generate.py \
  --prompt "Blog banner with text: AIエージェントの未来" \
  --output "./banner.png"
```

## Use Cases

1. **SNS Thumbnails** — Eye-catching images for Twitter/note.com posts
2. **Article Cover Images** — Professional headers for blog posts
3. **Banners** — Promotional graphics for services
4. **Profile Images** — Unique AI-generated avatars
5. **Presentation Slides** — Visual assets for decks

## Aspect Ratios

| Ratio | Use Case | Dimensions |
|-------|----------|------------|
| 16:9 | YouTube thumbnails, blog headers | 1792×1024 |
| 1:1 | Instagram, profile pics | 1024×1024 |
| 9:16 | Stories, vertical content | 1024×1792 |

## Configuration

Environment variables:
- `GOOGLE_AI_API_KEY` — Google AI Studio API key (required)

## Requirements

- Python 3.10+
- `google-genai` Python package
- Google AI Studio API key
