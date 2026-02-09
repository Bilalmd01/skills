#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "yt-dlp>=2026.2.4",
# ]
# ///

from __future__ import annotations

import argparse
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yt_dlp

MAX_VIDEO_SIZE = 2_000 * 1024 * 1024  # 2000M
MAX_AUDIO_SIZE = 30 * 1024 * 1024  # 30M
PLAYLIST_LIMIT = 30


class MediaKind(Enum):
    VIDEO = "video"
    MUSIC = "music"


@dataclass(frozen=True)
class DownloadPlan:
    url: str
    kind: MediaKind
    is_playlist: bool
    extractor: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Smart media downloader with yt-dlp defaults from SKILL.md.",
    )
    parser.add_argument("url", help="Media URL to download")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Probe and print the plan without downloading",
    )
    return parser.parse_args()


def detect_kind(info: dict[str, Any], url: str) -> MediaKind:
    host = (urlparse(url).hostname or "").lower()
    if "music." in host:
        return MediaKind.MUSIC

    ie_key = (info.get("extractor_key") or info.get("extractor") or "").lower()
    if "music" in ie_key or "soundcloud" in ie_key or "spotify" in ie_key:
        return MediaKind.MUSIC

    categories = [c.lower() for c in info.get("categories") or []]
    if any("music" in cat for cat in categories):
        return MediaKind.MUSIC

    if info.get("track") or info.get("artist") or info.get("album"):
        return MediaKind.MUSIC

    return MediaKind.VIDEO


def detect_playlist(info: dict[str, Any]) -> bool:
    entry_type = info.get("_type")
    if entry_type in {"playlist", "multi_video", "multi_track", "multi_song"}:
        return True
    if "entries" in info:
        return True
    return bool(info.get("playlist_count"))


def probe(url: str) -> DownloadPlan:
    probe_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": "discard_in_playlist",
        "ignoreerrors": True,
        "noplaylist": False,
    }
    with yt_dlp.YoutubeDL(probe_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return DownloadPlan(
        url=url,
        kind=detect_kind(info, url),
        is_playlist=detect_playlist(info),
        extractor=info.get("extractor") or info.get("extractor_key") or "unknown",
    )


def build_options(plan: DownloadPlan) -> dict[str, Any]:
    outtmpl = (
        "%(playlist_title)s/%(title).240B.%(ext)s"
        if plan.is_playlist
        else "%(title).240B.%(ext)s"
    )

    opts: dict[str, Any] = {
        "outtmpl": {"default": outtmpl},
        "paths": {
            "home": str(
                Path.home() / ("Music" if plan.kind is MediaKind.MUSIC else "Movies"),
            ),
        },
        "noplaylist": not plan.is_playlist,
        "max_downloads": PLAYLIST_LIMIT if plan.is_playlist else None,
        "quiet": False,
        "concurrent_fragment_downloads": 4,
        "retries": 3,
    }

    if plan.kind is MediaKind.VIDEO:
        opts.update(
            format="bestvideo[vcodec^=avc1]+bestaudio/best",
            merge_output_format="mp4",
            max_filesize=MAX_VIDEO_SIZE,
        )
    else:
        opts.update(
            format="bestaudio/best",
            postprocessors=[
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                    "preferredquality": "0",
                },
            ],
            max_filesize=MAX_AUDIO_SIZE,
        )

    if opts["max_downloads"] is None:
        opts.pop("max_downloads")

    return opts


def print_plan(plan: DownloadPlan) -> None:
    playlist_label = "playlist" if plan.is_playlist else "single"
    print(
        f"[plan] {plan.kind.value} · {playlist_label} · extractor={plan.extractor}",
    )


def download(plan: DownloadPlan) -> None:
    opts = build_options(plan)
    print_plan(plan)
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([plan.url])


def main() -> None:
    args = parse_args()
    plan = probe(args.url)
    print_plan(plan)

    if args.dry_run:
        return

    try:
        download(plan)
    except yt_dlp.utils.DownloadError as exc:  # type: ignore[attr-defined]
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
