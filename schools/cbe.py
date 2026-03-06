from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict, cast
import random

from .cbc_utils import (
    LOWER_PRIMARY_LEVEL_POINTS,
    UPPER_PRIMARY_LEVEL_POINTS,
    get_primary_level_and_points,
    get_primary_level_order,
)


class SubjectSpec(TypedDict):
    name: str
    code: str
    short_name: str
    category: str
    optional: bool

JUNIOR_SUBJECT_SPECS: List[SubjectSpec] = [
    # Core learning areas
    {"name": "English", "code": "ENG", "short_name": "Eng", "category": "Languages", "optional": False},
    {"name": "Kiswahili/KSL", "code": "KIS", "short_name": "Kis", "category": "Languages", "optional": False},
    {"name": "Indigenous Language", "code": "IND", "short_name": "Ind", "category": "Languages", "optional": False},
    {"name": "Mathematics", "code": "MATH", "short_name": "Math", "category": "Sciences & Math", "optional": False},
    {"name": "Integrated Science", "code": "ISCI", "short_name": "Int Sci", "category": "Sciences & Math", "optional": False},
    {"name": "Health Education", "code": "HLTH", "short_name": "Health", "category": "Sciences & Math", "optional": False},
    {"name": "Social Studies", "code": "SST", "short_name": "Soc", "category": "Humanities", "optional": False},
    {"name": "Religious Education", "code": "RE", "short_name": "RE", "category": "Humanities", "optional": False},
    {"name": "Pre-Technical", "code": "PRET", "short_name": "PreTech", "category": "Technical", "optional": False},
    {"name": "Business Studies", "code": "BST", "short_name": "Biz", "category": "Technical", "optional": False},
    {"name": "Agriculture", "code": "AGR", "short_name": "Agr", "category": "Technical", "optional": False},
    {"name": "Creative Arts", "code": "CART", "short_name": "Creat", "category": "Creative", "optional": False},
    {"name": "Sports & Physical Education", "code": "SPE", "short_name": "SPE", "category": "Creative", "optional": False},
    {"name": "Life Skills Education", "code": "LIFE", "short_name": "Life", "category": "Life Skills", "optional": False},
    # Optional learning areas (choose 1–2)
    {"name": "Visual Arts", "code": "VART", "short_name": "V Arts", "category": "Optional", "optional": True},
    {"name": "Performing Arts", "code": "PART", "short_name": "P Arts", "category": "Optional", "optional": True},
    {"name": "Home Science", "code": "HSCI", "short_name": "HomeSci", "category": "Optional", "optional": True},
    {"name": "Computer Science", "code": "CS", "short_name": "Comp", "category": "Optional", "optional": True},
    {"name": "Foreign Languages", "code": "FLANG", "short_name": "F Lang", "category": "Optional", "optional": True},
]

LOWER_PRIMARY_SUBJECT_SPECS: List[SubjectSpec] = [
    {"name": "English", "code": "ENG", "short_name": "Eng", "category": "Languages", "optional": False},
    {"name": "Kiswahili/KSL", "code": "KIS", "short_name": "Kis", "category": "Languages", "optional": False},
    {"name": "Mathematical Activities", "code": "MATHA", "short_name": "Math Act", "category": "Mathematics", "optional": False},
    {"name": "Religious Education", "code": "RE", "short_name": "RE", "category": "Humanities", "optional": False},
    {"name": "Environmental Activities", "code": "ENV", "short_name": "Env", "category": "Science & Social", "optional": False},
    {"name": "Creative Activities", "code": "CREACT", "short_name": "Creative", "category": "Creative", "optional": False},
    {"name": "Physical Education", "code": "PE", "short_name": "PE", "category": "Physical", "optional": False},
    {"name": "Indigenous Language", "code": "IND", "short_name": "Ind", "category": "Languages", "optional": False},
]

UPPER_PRIMARY_SUBJECT_SPECS: List[SubjectSpec] = [
    {"name": "English", "code": "ENG", "short_name": "Eng", "category": "Languages", "optional": False},
    {"name": "Kiswahili/KSL", "code": "KIS", "short_name": "Kis", "category": "Languages", "optional": False},
    {"name": "Mathematics", "code": "MATH", "short_name": "Math", "category": "Mathematics", "optional": False},
    {"name": "Science & Technology", "code": "SCI", "short_name": "Sci", "category": "Sciences", "optional": False},
    {"name": "Agriculture", "code": "AGR", "short_name": "Agr", "category": "Technical", "optional": False},
    {"name": "Home Science", "code": "HSCI", "short_name": "HomeSci", "category": "Technical", "optional": False},
    {"name": "Social Studies", "code": "SST", "short_name": "SST", "category": "Humanities", "optional": False},
    {"name": "Religious Education", "code": "RE", "short_name": "RE", "category": "Humanities", "optional": False},
    {"name": "Creative Arts", "code": "CART", "short_name": "Creative", "category": "Creative", "optional": False},
    {"name": "Foreign Languages", "code": "FLANG", "short_name": "F Lang", "category": "Optional", "optional": True},
]


def _normalize_subject_name(name: Optional[str]) -> str:
    if not name:
        return ""
    cleaned = (
        name.lower()
        .replace("&", "and")
        .replace("/", " ")
        .replace("-", " ")
        .replace("_", " ")
    )
    cleaned = " ".join(cleaned.split())
    return cleaned


_JUNIOR_NAME_MAP = {_normalize_subject_name(s["name"]): s for s in JUNIOR_SUBJECT_SPECS}
JUNIOR_SUBJECT_NAMES = set(_JUNIOR_NAME_MAP.keys())

_PRIMARY_NAME_MAP = {
    _normalize_subject_name(s["name"]): s
    for s in (LOWER_PRIMARY_SUBJECT_SPECS + UPPER_PRIMARY_SUBJECT_SPECS)
}
PRIMARY_SUBJECT_NAMES = set(_PRIMARY_NAME_MAP.keys())


def is_junior_subject_name(name: str) -> bool:
    return _normalize_subject_name(name) in JUNIOR_SUBJECT_NAMES


def is_primary_subject_name(name: str) -> bool:
    return _normalize_subject_name(name) in PRIMARY_SUBJECT_NAMES


JUNIOR_LEVEL_BANDS = [
    (90, 100, "EE1", 8),
    (75, 89, "EE2", 7),
    (58, 74, "ME1", 6),
    (41, 57, "ME2", 5),
    (31, 40, "AE1", 4),
    (21, 30, "AE2", 3),
    (11, 20, "BE1", 2),
    (1, 10, "BE2", 1),
]

JUNIOR_LEVEL_POINTS: Dict[str, int] = {level: points for _, _, level, points in JUNIOR_LEVEL_BANDS}
JUNIOR_LEVEL_ORDER = [level for _, _, level, _ in JUNIOR_LEVEL_BANDS]

PRIMARY_LEVEL_POINTS: Dict[str, int] = {
    **LOWER_PRIMARY_LEVEL_POINTS,
    **UPPER_PRIMARY_LEVEL_POINTS,
}


def get_junior_level(score: Optional[float]) -> str:
    if score is None:
        return ""
    try:
        value = float(score)
    except (TypeError, ValueError):
        return ""
    if value <= 0:
        return ""
    for min_score, max_score, level, _ in JUNIOR_LEVEL_BANDS:
        if min_score <= value <= max_score:
            return level
    if value > 100:
        return "EE1"
    return ""


def get_junior_points(level: Optional[str]) -> int:
    if not level:
        return 0
    return JUNIOR_LEVEL_POINTS.get(level, 0)


def get_primary_level(score: Optional[float], education_level_name: Optional[str] = None) -> str:
    level, _ = get_primary_level_and_points(score, education_level_name)
    return level


def get_primary_points(level: Optional[str]) -> int:
    if not level:
        return 0
    return PRIMARY_LEVEL_POINTS.get(level, 0)


def get_junior_level_from_points(points: Optional[float]) -> str:
    if points is None:
        return ""
    try:
        value = float(points)
    except (TypeError, ValueError):
        return ""
    if value <= 0:
        return ""
    nearest = int(round(value))
    for level, pts in JUNIOR_LEVEL_POINTS.items():
        if pts == nearest:
            return level
    return ""


def ensure_junior_learning_areas(school) -> None:
    if not school or getattr(school, "system_type", None) != "CBE":
        return

    from .models import Subject, EducationLevel

    level_obj, _ = EducationLevel.objects.get_or_create(name="Junior")
    level_obj = cast(Any, level_obj)

    for spec in JUNIOR_SUBJECT_SPECS:
        name = spec["name"]
        subject = Subject.objects.filter(
            school=school,
            code__iexact=spec["code"],
            education_level=level_obj,
        ).first()
        if not subject:
            subject = Subject.objects.filter(
                school=school,
                name__iexact=name,
                education_level=level_obj,
            ).first()
        if not subject:
            subject = Subject.objects.create(
                school=school,
                name=name,
                code=spec["code"],
                short_name=spec["short_name"],
                education_level=level_obj,
            )
            continue

        subject_obj = cast(Any, subject)
        changed = False
        if not subject_obj.education_level or getattr(subject_obj, "education_level_id", None) != getattr(level_obj, "id", None):
            subject_obj.education_level = level_obj
            changed = True
        if not subject_obj.name:
            subject_obj.name = name
            changed = True
        if not subject_obj.code:
            subject_obj.code = spec["code"]
            changed = True
        if not subject_obj.short_name:
            subject_obj.short_name = spec["short_name"]
            changed = True
        if getattr(subject_obj, "pathway_id", None):
            subject_obj.pathway = None
            changed = True
        if changed:
            subject_obj.save()


def _ensure_subjects_for_level(school, level_name: str, specs: List[SubjectSpec]) -> None:
    if not school or getattr(school, "system_type", None) != "CBE":
        return

    from .models import Subject, EducationLevel

    level_obj, _ = EducationLevel.objects.get_or_create(name=level_name)
    level_obj = cast(Any, level_obj)

    for spec in specs:
        name = spec["name"]
        subject = Subject.objects.filter(
            school=school,
            code__iexact=spec["code"],
            education_level=level_obj,
        ).first()
        if not subject:
            subject = Subject.objects.filter(
                school=school,
                name__iexact=name,
                education_level=level_obj,
            ).first()
        if not subject:
            subject = Subject.objects.create(
                school=school,
                name=name,
                code=spec["code"],
                short_name=spec["short_name"],
                education_level=level_obj,
            )
            continue

        subject_obj = cast(Any, subject)
        changed = False
        if not subject_obj.education_level or getattr(subject_obj, "education_level_id", None) != getattr(level_obj, "id", None):
            subject_obj.education_level = level_obj
            changed = True
        if not subject_obj.name:
            subject_obj.name = name
            changed = True
        if not subject_obj.code:
            subject_obj.code = spec["code"]
            changed = True
        if not subject_obj.short_name:
            subject_obj.short_name = spec["short_name"]
            changed = True
        if getattr(subject_obj, "pathway_id", None):
            subject_obj.pathway = None
            changed = True
        if changed:
            subject_obj.save()


def ensure_lower_primary_subjects(school) -> None:
    _ensure_subjects_for_level(school, "Lower Primary", LOWER_PRIMARY_SUBJECT_SPECS)


def ensure_upper_primary_subjects(school) -> None:
    _ensure_subjects_for_level(school, "Upper Primary", UPPER_PRIMARY_SUBJECT_SPECS)


def ensure_primary_learning_areas(school) -> None:
    ensure_lower_primary_subjects(school)
    ensure_upper_primary_subjects(school)


def ensure_cbe_learning_areas(school) -> None:
    if not school or getattr(school, "system_type", None) != "CBE":
        return
    category = getattr(school, "school_category", None)
    if category in ("PRIMARY", "COMPREHENSIVE", None):
        ensure_lower_primary_subjects(school)
        ensure_upper_primary_subjects(school)
    if category in ("JUNIOR", "COMPREHENSIVE", None):
        ensure_junior_learning_areas(school)


def get_performance_level(level: Optional[str], percentage: Optional[float]) -> str:
    if not level or percentage is None:
        return ""
    if level in ("Primary", "Lower Primary", "Upper Primary"):
        return get_primary_level(percentage, level) or ""
    if level == "Junior":
        return get_junior_level(percentage) or ""
    return ""


def get_comment_variants(level: str, subject, performance_level: str, limit: int = 7) -> List[str]:
    if not level or not performance_level:
        return []
    from .models import CompetencyComment

    qs = CompetencyComment.objects.filter(
        education_level=level,
        performance_level=performance_level,
    )
    if subject:
        subject_qs = qs.filter(subject=subject)
        if subject_qs.exists():
            qs = subject_qs
        else:
            qs = qs.filter(subject__isnull=True)
    else:
        qs = qs.filter(subject__isnull=True)

    comments = list(qs.values_list('comment_text', flat=True))
    if not comments:
        return []
    random.shuffle(comments)
    return comments[:limit] if limit else comments


def get_random_comment(level: str, subject, performance_level: str, student=None, term: Optional[str] = None) -> str:
    comments = get_comment_variants(level, subject, performance_level, limit=0)
    if not comments:
        return ""

    if student and subject and term:
        from .models import StudentMark
        previous = (
            StudentMark.objects.filter(
                student=student,
                marksheet__subject=subject,
            )
            .exclude(comment_text='')
            .exclude(marksheet__term=term)
            .order_by('-marksheet__exam__year', '-marksheet__created_at')
            .values_list('comment_text', flat=True)
            .first()
        )
        if previous and len(comments) > 1:
            comments = [c for c in comments if c != previous] or comments

    return random.choice(comments)


def recommend_junior_pathway(subject_points_by_name: Dict[str, int]) -> str:
    if not subject_points_by_name:
        return "GENERAL"

    def points_for(names: List[str]) -> List[int]:
        values = []
        for n in names:
            norm = _normalize_subject_name(n)
            for subject_name, pts in subject_points_by_name.items():
                if _normalize_subject_name(subject_name) == norm:
                    values.append(pts)
                    break
        return values

    stem_points = points_for(["Mathematics", "Integrated Science", "Computer Science"])
    arts_points = points_for(["Creative Arts", "Sports & Physical Education", "Visual Arts", "Performing Arts"])
    social_points = points_for([
        "Social Studies",
        "Religious Education",
        "Business Studies",
        "English",
        "Kiswahili/KSL",
        "Indigenous Language",
        "Foreign Languages",
    ])

    def avg(values: List[int]) -> Optional[float]:
        if not values:
            return None
        return sum(values) / len(values)

    threshold = JUNIOR_LEVEL_POINTS.get("ME1", 6)
    stem_avg = avg(stem_points)
    if stem_avg is not None and stem_avg >= threshold:
        return "STEM"

    arts_avg = avg(arts_points)
    if arts_avg is not None and arts_avg >= threshold:
        return "ARTS"

    social_avg = avg(social_points)
    if social_avg is not None and social_avg >= threshold:
        return "SOCIAL"

    return "GENERAL"


def recommend_primary_interest(subject_points_by_name: Dict[str, int]) -> str:
    if not subject_points_by_name:
        return "GENERAL"

    def points_for(names: List[str]) -> List[int]:
        values = []
        for n in names:
            norm = _normalize_subject_name(n)
            for subject_name, pts in subject_points_by_name.items():
                if _normalize_subject_name(subject_name) == norm:
                    values.append(pts)
                    break
        return values

    threshold = PRIMARY_LEVEL_POINTS.get("ME", 3)

    stem_points = points_for([
        "Mathematics",
        "Environmental Activities / Science & Technology",
    ])
    arts_points = points_for([
        "Creative Arts",
        "Physical & Health Education",
    ])
    social_points = points_for([
        "English",
        "Kiswahili",
        "Social Studies",
    ])

    def avg(values: List[int]) -> Optional[float]:
        if not values:
            return None
        return sum(values) / len(values)

    stem_avg = avg(stem_points)
    if stem_avg is not None and stem_avg >= threshold:
        return "STEM INTEREST"

    arts_avg = avg(arts_points)
    if arts_avg is not None and arts_avg >= threshold:
        return "ARTS INTEREST"

    social_avg = avg(social_points)
    if social_avg is not None and social_avg >= threshold:
        return "SOCIAL SCIENCES INTEREST"

    return "GENERAL"
