import subprocess
import json
import os
import re
import sys

# 👇 INPUT FILE NAME
INPUT_FILE = "hp4.m4b"
OUTPUT_FOLDER = "stream"


def sanitize_filename(name):
    """Illegal characters remove karta hai"""
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


def get_chapters(filename):
    """FFprobe se chapter metadata nikalta hai"""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_chapters",
        filename
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("❌ FFprobe run nahi hua properly.")
            print(result.stderr)
            return []

        data = json.loads(result.stdout)
        return data.get("chapters", [])

    except Exception as e:
        print("❌ Metadata read nahi ho paya:", e)
        return []


def split_audiobook():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ File '{INPUT_FILE}' nahi mili.")
        return

    print(f"🔍 Reading Chapters from {INPUT_FILE}...")

    chapters = get_chapters(INPUT_FILE)

    if not chapters:
        print("⚠️ Is file mein chapters nahi mile!")
        return

    print(f"✅ Total {len(chapters)} chapters mile. Cutting shuru... ✂️")

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for i, chapter in enumerate(chapters):

        start_time = chapter["start_time"]
        end_time = chapter["end_time"]

        meta_title = chapter.get("tags", {}).get("title", "")

        if meta_title:
            safe_title = sanitize_filename(meta_title)
            if safe_title.isdigit():
                file_name = f"Chapter_{i+1:02d}.m4a"
            else:
                file_name = f"Chapter_{i+1:02d}_{safe_title}.m4a"
        else:
            file_name = f"Chapter_{i+1:02d}.m4a"

        output_path = os.path.join(OUTPUT_FOLDER, file_name)

        print(f"   ⏳ Processing: {file_name}")

        cmd = [
            "ffmpeg",
            "-y",  # overwrite if exists
            "-i", INPUT_FILE,
            "-ss", str(start_time),
            "-to", str(end_time),
            "-c", "copy",
            output_path
        ]

        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )

    print(f"\n🎉 Ho gaya! '{OUTPUT_FOLDER}' folder check kar.")


if __name__ == "__main__":
    split_audiobook()