from typing import Dict


def calculate_left_right_difference(left_value: float, right_value: float) -> float:
    return left_value - right_value


def calculate_symmetry_index(left_value: float, right_value: float) -> float:
    denominator = (left_value + right_value) / 2
    if denominator == 0:
        return 0.0
    return abs(left_value - right_value) / denominator * 100


def classify_symmetry(symmetry_index: float) -> str:
    if symmetry_index < 5:
        return "good_symmetry"
    if symmetry_index < 10:
        return "mild_asymmetry"
    if symmetry_index < 20:
        return "moderate_asymmetry"
    return "marked_asymmetry"


def summarize_symmetry(left_value: float, right_value: float) -> Dict[str, object]:
    si = calculate_symmetry_index(left_value, right_value)
    return {
        "left_value": left_value,
        "right_value": right_value,
        "difference": calculate_left_right_difference(left_value, right_value),
        "symmetry_index": si,
        "classification": classify_symmetry(si),
    }
