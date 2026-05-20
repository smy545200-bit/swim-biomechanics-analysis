import pytest
from core.biomechanics import calculate_joint_angle, calculate_midpoint


def test_calculate_joint_angle_right_angle():
    angle = calculate_joint_angle((1, 0), (0, 0), (0, 1))
    assert angle == pytest.approx(90.0)


def test_calculate_midpoint():
    assert calculate_midpoint((0, 0), (2, 2)) == (1, 1)
