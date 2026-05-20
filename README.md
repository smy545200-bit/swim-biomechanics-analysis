# SwimBiomech Analyst

水下泳姿生物力学分析系统。

本项目面向竞技游泳训练与科研分析，第一阶段聚焦侧面水下自由泳视频的半自动分析：视频导入、关键帧截取、关键点标注、关节角度计算、左右对称性分析、技术问题登记与报告生成。

## Core pipeline

Video input -> Keypoint annotation or pose estimation -> Biomechanical metrics -> Technical diagnosis -> Training report.

## MVP modules

- PySide6 desktop interface
- OpenCV video processing
- Biomechanical angle calculation
- Symmetry analysis
- SQLite data storage
- Word report generation
- Future MMPose or RTMPose integration

## Run

```bash
pip install -r requirements.txt
python main.py
```
