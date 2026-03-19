#!/usr/bin/env python3
"""
note記事用画像生成スクリプト
Gemini API (google-genai) を使用してインフォグラフィック画像を生成
"""

import os
import sys
import json
import base64
from pathlib import Path

def _load_dotenv():
    """プロジェクトルートの .env からAPIキーを読み込み"""
    for env_path in [Path(__file__).resolve().parent.parent / ".env", Path.cwd() / ".env"]:
        if env_path.exists():
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key, value = key.strip(), value.strip()
                    if key and key not in os.environ:
                        os.environ[key] = value
            break

_load_dotenv()

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: google-genai not installed. Run: pip install google-genai", file=sys.stderr)
    sys.exit(1)

try:
    from PIL import Image
    import io
except ImportError:
    Image = None
    print("WARNING: Pillow not installed. Images will be saved as raw bytes.", file=sys.stderr)


def generate_image(api_key: str, prompt: str, output_path: str, aspect_ratio: str = "16:9") -> bool:
    """Gemini APIで画像を生成して保存"""
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                mime_type = part.inline_data.mime_type

                Path(output_path).parent.mkdir(parents=True, exist_ok=True)

                if Image is not None:
                    img = Image.open(io.BytesIO(image_data))
                    img.save(output_path)
                else:
                    ext = ".png" if "png" in mime_type else ".jpg"
                    if not output_path.endswith(ext):
                        output_path = output_path.rsplit(".", 1)[0] + ext
                    with open(output_path, "wb") as f:
                        f.write(image_data)

                print(f"OK: {output_path} ({len(image_data)} bytes)")
                return True

        print(f"WARN: No image in response for {output_path}", file=sys.stderr)
        return False

    except Exception as e:
        print(f"ERROR generating {output_path}: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python note-image-gen.py <config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    api_key = config.get("api_key") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: No API key provided", file=sys.stderr)
        sys.exit(1)

    results = []
    for item in config["images"]:
        ok = generate_image(
            api_key=api_key,
            prompt=item["prompt"],
            output_path=item["output_path"],
            aspect_ratio=item.get("aspect_ratio", "16:9"),
        )
        results.append({"path": item["output_path"], "success": ok})

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
