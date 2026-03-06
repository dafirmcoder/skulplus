from __future__ import annotations

from typing import Dict, List, Optional, Tuple

LowerPrimaryBand = Tuple[int, int, str, int]
UpperPrimaryBand = Tuple[int, int, str, int]

LOWER_PRIMARY_LEVEL_BANDS: List[LowerPrimaryBand] = [
    (75, 100, "EE", 4),
    (50, 74, "ME", 3),
    (25, 49, "AE", 2),
    (0, 24, "BE", 1),
]

UPPER_PRIMARY_LEVEL_BANDS: List[UpperPrimaryBand] = [
    (90, 100, "EE1", 8),
    (75, 89, "EE2", 7),
    (58, 74, "ME1", 6),
    (41, 57, "ME2", 5),
    (31, 40, "AE1", 4),
    (21, 30, "AE2", 3),
    (11, 20, "BE1", 2),
    (1, 10, "BE2", 1),
]

LOWER_PRIMARY_LEVEL_POINTS: Dict[str, int] = {
    level: points for _, _, level, points in LOWER_PRIMARY_LEVEL_BANDS
}
UPPER_PRIMARY_LEVEL_POINTS: Dict[str, int] = {
    level: points for _, _, level, points in UPPER_PRIMARY_LEVEL_BANDS
}

LOWER_PRIMARY_LEVEL_ORDER = [level for _, _, level, _ in LOWER_PRIMARY_LEVEL_BANDS]
UPPER_PRIMARY_LEVEL_ORDER = [level for _, _, level, _ in UPPER_PRIMARY_LEVEL_BANDS]


def _bands_for_level(education_level_name: Optional[str]) -> List[Tuple[int, int, str, int]]:
    if education_level_name == "Upper Primary":
        return UPPER_PRIMARY_LEVEL_BANDS
    return LOWER_PRIMARY_LEVEL_BANDS


def get_primary_level_and_points(
    score: Optional[float],
    education_level_name: Optional[str],
) -> tuple[str, int]:
    if score is None:
        return "", 0
    try:
        value = float(score)
    except (TypeError, ValueError):
        return "", 0
    if value <= 0:
        return "", 0

    bands = _bands_for_level(education_level_name)
    for min_score, max_score, level, points in bands:
        if min_score <= value <= max_score:
            return level, points

    if value > 100:
        if education_level_name == "Upper Primary":
            return "EE1", 8
        return "EE", 4

    return "", 0


def get_primary_level_order(education_level_name: Optional[str]) -> List[str]:
    if education_level_name == "Upper Primary":
        return list(UPPER_PRIMARY_LEVEL_ORDER)
    return list(LOWER_PRIMARY_LEVEL_ORDER)
