#!/usr/bin/env python3
"""
Transcribe YouTube videos or audio files for Poliittinen Muisti.

Usage:
    python transcribe.py "https://youtube.com/watch?v=..."
    python transcribe.py /path/to/audio.mp3
"""

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Check for required packages
try:
    import openai
except ImportError:
    print("Error: openai package not installed. Run: pip install openai")
    sys.exit(1)

try:
    import yt_dlp
except ImportError:
    yt_dlp = None  # Optional, only needed for YouTube


def download_youtube_audio(url: str, output_dir: str) -> str:
    """Download audio from YouTube video."""
    if yt_dlp is None:
        raise ImportError("yt-dlp not installed. Run: pip install yt-dlp")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        mp3_path = os.path.splitext(filename)[0] + '.mp3'
        return mp3_path, info.get('title', 'Unknown')


def transcribe_audio(audio_path: str) -> dict:
    """Transcribe audio file using OpenAI Whisper."""
    client = openai.OpenAI()

    with open(audio_path, 'rb') as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="fi",
            response_format="verbose_json"
        )

    return response


def save_transcript(
    transcript: dict,
    title: str,
    source_url: str,
    output_dir: str
) -> str:
    """Save transcript as markdown file."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-")[:50]
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(output_dir, filename)

    # Build markdown content
    content = f"""# {title}

**Date:** {date_str}
**Source:** {source_url}
**Duration:** {transcript.get('duration', 'Unknown')} seconds

---

## Transcript

"""

    # Add segments with timestamps if available
    if hasattr(transcript, 'segments'):
        for segment in transcript.segments:
            start = int(segment.get('start', 0))
            mins, secs = divmod(start, 60)
            timestamp = f"[{mins:02d}:{secs:02d}]"
            text = segment.get('text', '').strip()
            content += f"**{timestamp}** {text}\n\n"
    else:
        content += transcript.text if hasattr(transcript, 'text') else str(transcript)

    content += """
---

## Metadata

- **Transcribed by:** AI (Whisper)
- **Transcription date:** """ + date_str + """
- **Status:** pending review

---

*Add extracted statements to `data/statements/` after review.*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe video/audio for Poliittinen Muisti"
    )
    parser.add_argument(
        "source",
        help="YouTube URL or path to audio file"
    )
    parser.add_argument(
        "--output-dir",
        default="transcripts",
        help="Output directory for transcripts"
    )

    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Determine if source is URL or file
    is_youtube = args.source.startswith(('http://', 'https://'))

    if is_youtube:
        print(f"Downloading audio from: {args.source}")
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path, title = download_youtube_audio(args.source, tmpdir)
            print(f"Downloaded: {title}")
            print("Transcribing...")
            transcript = transcribe_audio(audio_path)
            output_path = save_transcript(
                transcript, title, args.source, args.output_dir
            )
    else:
        if not os.path.exists(args.source):
            print(f"Error: File not found: {args.source}")
            sys.exit(1)

        title = Path(args.source).stem
        print(f"Transcribing: {args.source}")
        transcript = transcribe_audio(args.source)
        output_path = save_transcript(
            transcript, title, args.source, args.output_dir
        )

    print(f"\nTranscript saved to: {output_path}")
    print("\nNext steps:")
    print("1. Review the transcript for accuracy")
    print("2. Extract statements to data/statements/")
    print("3. Commit and push changes")


if __name__ == "__main__":
    main()
