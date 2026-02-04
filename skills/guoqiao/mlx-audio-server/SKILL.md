---
name: mlx-audio-server
description: The best audio processing library built on Apple's MLX framework, providing fast and efficient text-to-speech (TTS), speech-to-text (STT), and speech-to-speech (STS) on Apple Silicon, at your service as OpenAI Compatible API server.
metadata: {"openclaw":{"always":true,"emoji":"🦞","homepage":"https://github.com/guoqiao/skills/blob/main/mlx-audio-server/src/SKILL.md","os":["darwin"],"tags":["latest","asr","stt","speech-to-text","tts","text-to-speech","mlx","audio","mlx-audio","glm","glm-asr","glm-asr-nano-2512","glm-asr-nano-2512-8bit","macOS","MacBook","Mac mini","Apple Silicon","server","local","openai","api","compatible","openai-compatible","transcription"],"requires":{"bins":["brew"]}}}
---

# MLX Audio Server

The best audio processing library built on Apple's MLX framework, providing fast and efficient text-to-speech (TTS), speech-to-text (STT), and speech-to-speech (STS) on Apple Silicon, at your service as OpenAI Compatible API server.

Default Models:

- STT: `mlx-community/glm-asr-nano-2512-8bit`
- TTS: `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16`

More choices here: https://github.com/Blaizzy/mlx-audio?tab=readme-ov-file#supported-models

## Requirements

- `mlx`: macOS with Apple Silicon
- `brew`: used to install deps if not available

## Installation

```bash
bash ${baseDir}/install.sh
```
This script will:
- clone (forked) mlx-audio repo into `~/opt/mlx-audio`
- use `uv` to create a venv and install deps in it: `~/opt/mlx-audio/.venv`
- create a plist service file to run mlx-audio server as a launchd daemon in user domain
- run as a OpenAI compatible API server, on port 8899 by default.

## Usage

STT/Speech-To-Text:
```bash
# input will be converted to wav with ffmpeg, if not yet.
# output will be transcript text only.
bash ${baseDir}/run_stt.sh <audio_or_video_path>
```

TTS/Text-To-Speech:
```bash
# audio will be saved into a tmp dir, with default name `speech.wav`, and print to stdout.
bash ${baseDir}/run_tts.sh "Hello, Human!"
# or you can specify a output dir
bash ${baseDir}/run_tts.sh "Hello, Human!" ./output
# output will be audio path only.
```

NOTE:

- First runs will be a little slow, since the server will need to download models (a few GBs) from Hugging Face.
- Both scripts can be used directly, or as example/reference.
