from core.symmetry import calculate_symmetry_index, classify_symmetry


def test_symmetry_index():
    si = calculate_symmetry_index(42, 36)
    assert round(si, 2) == 15.38


def test_classify_symmetry():
    assert classify_symmetry(3) == "good_symmetry"
    assert classify_symmetry(8) == "mild_asymmetry"
    assert classify_symmetry(15) == "moderate_asymmetry"
    assert classify_symmetry(25) == "marked_asymmetry"
