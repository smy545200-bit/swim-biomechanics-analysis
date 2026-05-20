from __future__ import annotations

from typing import Dict, List, Tuple

import cv2
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QLabel


class VideoCanvas(QLabel):
    point_clicked = Signal(str, float, float)

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(820, 520)
        self.setStyleSheet("border: 1px solid #888; background: #111; color: #ddd;")
        self.setText("Import a video to display frames here")
        self.original_pixmap: QPixmap | None = None
        self.frame_shape: Tuple[int, int] | None = None
        self.current_keypoint_name = "left_shoulder"
        self.points: List[Dict[str, float | str]] = []

    def set_current_keypoint(self, name: str) -> None:
        self.current_keypoint_name = name

    def set_frame(self, frame_bgr) -> None:
        if frame_bgr is None:
            self.clear()
            self.setText("No frame")
            return

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        height, width, channels = frame_rgb.shape
        bytes_per_line = channels * width
        qimage = QImage(frame_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888).copy()
        self.original_pixmap = QPixmap.fromImage(qimage)
        self.frame_shape = (height, width)
        self._render()

    def set_points(self, points: List[Dict[str, float | str]]) -> None:
        self.points = points
        self._render()

    def clear_points(self) -> None:
        self.points = []
        self._render()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._render()

    def mousePressEvent(self, event):
        if self.original_pixmap is None or self.frame_shape is None:
            return
        if event.button() != Qt.LeftButton:
            return

        display_rect = self._display_rect()
        pos = event.position()
        if not display_rect[0] <= pos.x() <= display_rect[0] + display_rect[2]:
            return
        if not display_rect[1] <= pos.y() <= display_rect[1] + display_rect[3]:
            return

        height, width = self.frame_shape
        x = (pos.x() - display_rect[0]) / display_rect[2] * width
        y = (pos.y() - display_rect[1]) / display_rect[3] * height
        self.point_clicked.emit(self.current_keypoint_name, float(x), float(y))

    def _display_rect(self) -> Tuple[float, float, float, float]:
        if self.original_pixmap is None:
            return (0, 0, 0, 0)
        scaled = self.original_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        x0 = (self.width() - scaled.width()) / 2
        y0 = (self.height() - scaled.height()) / 2
        return (x0, y0, scaled.width(), scaled.height())

    def _render(self) -> None:
        if self.original_pixmap is None:
            return

        scaled = self.original_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        canvas = QPixmap(scaled)
        painter = QPainter(canvas)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.yellow, 3)
        painter.setPen(pen)

        if self.frame_shape is not None:
            height, width = self.frame_shape
            sx = scaled.width() / width
            sy = scaled.height() / height
            for point in self.points:
                x = float(point["x"]) * sx
                y = float(point["y"]) * sy
                name = str(point["name"])
                painter.drawEllipse(int(x) - 5, int(y) - 5, 10, 10)
                painter.drawText(int(x) + 8, int(y) - 8, name)

        painter.end()
        self.setPixmap(canvas)
