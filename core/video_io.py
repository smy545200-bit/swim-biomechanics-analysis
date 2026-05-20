from pathlib import Path
import cv2


class VideoReader:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video file: {video_path}")

    def get_video_info(self) -> dict:
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0
        return {
            "fps": fps,
            "frame_count": frame_count,
            "width": width,
            "height": height,
            "duration_seconds": duration,
        }

    def read_frame_by_index(self, frame_index: int):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        success, frame = self.cap.read()
        if not success:
            return None
        return frame

    def save_frame(self, frame, frame_index: int, output_dir: str = "data/frames") -> str:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_path = Path(output_dir) / f"frame_{frame_index:06d}.jpg"
        cv2.imwrite(str(output_path), frame)
        return str(output_path)

    def release(self):
        if self.cap:
            self.cap.release()
