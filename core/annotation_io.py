from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


def save_annotation_json(video_path: str, frame_index: int, points: List[Dict[str, float | str]], output_dir: str = "data/annotations") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    stem = Path(video_path).stem if video_path else "unknown_video"
    output_path = Path(output_dir) / f"{stem}_frame_{frame_index:06d}_annotation.json"
    payload = {
        "video_path": video_path,
        "frame_index": frame_index,
        "points": points,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(output_path)
