import math
from typing import Tuple

Point2D = Tuple[float, float]


def calculate_joint_angle(point_a: Point2D, point_b: Point2D, point_c: Point2D) -> float:
    ax, ay = point_a
    bx, by = point_b
    cx, cy = point_c
    vector_ba = (ax - bx, ay - by)
    vector_bc = (cx - bx, cy - by)
    dot_product = vector_ba[0] * vector_bc[0] + vector_ba[1] * vector_bc[1]
    norm_ba = math.sqrt(vector_ba[0] ** 2 + vector_ba[1] ** 2)
    norm_bc = math.sqrt(vector_bc[0] ** 2 + vector_bc[1] ** 2)
    if norm_ba == 0 or norm_bc == 0:
        raise ValueError("Overlapping keypoints cannot define an angle.")
    cos_angle = dot_product / (norm_ba * norm_bc)
    cos_angle = max(-1.0, min(1.0, cos_angle))
    return math.degrees(math.acos(cos_angle))


def calculate_midpoint(point_left: Point2D, point_right: Point2D) -> Point2D:
    return ((point_left[0] + point_right[0]) / 2, (point_left[1] + point_right[1]) / 2)


def calculate_trunk_inclination(shoulder_mid: Point2D, hip_mid: Point2D) -> float:
    sx, sy = shoulder_mid
    hx, hy = hip_mid
    dx = sx - hx
    dy = sy - hy
    return math.degrees(math.atan2(dy, dx))


def calculate_line_angle(point_a: Point2D, point_b: Point2D) -> float:
    ax, ay = point_a
    bx, by = point_b
    return math.degrees(math.atan2(by - ay, bx - ax))
