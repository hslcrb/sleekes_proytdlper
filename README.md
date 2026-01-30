# SLEEKES: Achromatic Archiving System

**SLEEKES** is a potent, minimalist video archiving solution built on the power of the `yt-dlp` engine. It is designed to secure digital heritage—descriptions, metadata, comments, and subtitles—with a focus on permanence and ultimate purity.

## Key Features

- **Achromatic Design Mode**: A high-contrast, distraction-free environment supporting both Pure Dark and Pure Light themes.
- **SVG Icon System**: All traditional emojis have been replaced with custom-coded SVG icons for a professional, consistent aesthetic.
- **403 Forbidden Protection**: Advanced anti-bot measures including Android/iOS client emulation and intelligent User-Agent rotation.
- **Precision Sleep Engine**: Configurable minute-based sleep intervals (e.g., 5m to 30m random range) to bypass the most aggressive IP blocks.
- **Complete Archiving**: Secures descriptions (.desc), metadata (.json), high-quality thumbnails, and all comments in a single session.
- **Audio Specialist Mode**: Extracts the highest fidelity audio streams with AI-enhanced post-processing to MP3 format.
- **Global Platform Support**: Securely archives content from YouTube, Instagram, TikTok, Facebook, and thousands of other platforms.

## Installation & Execution

### 1. Quick Start
Run the provided shell script to automatically configure the virtual environment and launch the system.
```bash
./run.sh
```

### 2. Manual Execution
```bash
# Activate environment
source venv/bin/activate

# Launch Achromatic GUI
python main.py

# CLI Mode Execution
python main.py [URL] --rec
```

## CLI Command Guide

- **Recommended Mode (Secure)**: `python main.py [URL] --rec`
- **Audio Extraction**: `python main.py [URL] -x`
- **Safe Full Archive**: `python main.py [URL] --archive --sleep 5`
- **Help/Manual**: `python main.py help`

## License
Licensed under the [Apache License 2.0](LICENSE).

---
*Developed by Antigravity. Potent . Pure . Permanent.*
