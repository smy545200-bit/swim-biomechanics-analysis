from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QTextEdit, QSpinBox, QFormLayout

from core.video_io import VideoReader
from core.biomechanics import calculate_joint_angle
from core.symmetry import summarize_symmetry


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SwimBiomech Analyst")
        self.resize(1280, 800)
        self.video_path = None
        self.video_reader = None
        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        control_layout = QFormLayout()

        self.video_label = QLabel("Video preview area. Later versions will display frames and keypoints here.")
        self.video_label.setMinimumSize(800, 500)
        self.video_label.setStyleSheet("border: 1px solid #999; padding: 12px;")

        self.frame_spin = QSpinBox()
        self.frame_spin.setRange(0, 999999)
        self.frame_spin.setValue(0)

        self.load_button = QPushButton("Import underwater video")
        self.load_button.clicked.connect(self.load_video)

        self.extract_button = QPushButton("Extract selected frame")
        self.extract_button.clicked.connect(self.extract_key_frame)

        self.analyze_button = QPushButton("Run sample biomechanical calculation")
        self.analyze_button.clicked.connect(self.run_analysis)

        control_layout.addRow("Frame index", self.frame_spin)
        self.log_box = QTextEdit()
        self.log_box.setPlaceholderText("Analysis logs and diagnostic results will be displayed here.")

        left_layout.addWidget(self.video_label)
        left_layout.addLayout(control_layout)
        left_layout.addWidget(self.load_button)
        left_layout.addWidget(self.extract_button)
        left_layout.addWidget(self.analyze_button)

        right_layout.addWidget(QLabel("Technical diagnosis and report area"))
        right_layout.addWidget(self.log_box)

        main_layout.addLayout(left_layout, stretch=3)
        main_layout.addLayout(right_layout, stretch=1)
        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose underwater swimming video", "", "Video Files (*.mp4 *.avi *.mov *.mkv)")
        if file_path:
            self.video_path = file_path
            self.video_reader = VideoReader(file_path)
            info = self.video_reader.get_video_info()
            self.log_box.append(f"Imported video: {file_path}")
            self.log_box.append(f"Video info: {info}")
            self.frame_spin.setRange(0, max(0, info["frame_count"] - 1))

    def extract_key_frame(self):
        if not self.video_reader:
            self.log_box.append("Please import a video first.")
            return
        frame_index = self.frame_spin.value()
        frame = self.video_reader.read_frame_by_index(frame_index)
        if frame is not None:
            out_path = self.video_reader.save_frame(frame, frame_index)
            self.log_box.append(f"Extracted frame {frame_index}: {out_path}")
        else:
            self.log_box.append("Frame extraction failed.")

    def run_analysis(self):
        angle = calculate_joint_angle((100, 200), (150, 250), (200, 200))
        symmetry = summarize_symmetry(left_value=42.0, right_value=36.0)
        self.log_box.append(f"Sample elbow angle: {angle:.2f} deg")
        self.log_box.append(f"Sample symmetry analysis: {symmetry}")
