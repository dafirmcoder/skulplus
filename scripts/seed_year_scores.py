"""Seed subject scores for existing students across a full school year.

Usage example:
    python scripts/seed_year_scores.py --school "My School" --year 2025

Optional flags:
    --out-of 100 --mean 62 --std 12 --min 30 --max 95 --overwrite --publish
"""
import os
import sys
import argparse
import random
from datetime import date

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django  # noqa: E402

django.setup()

from django.db import transaction  # noqa: E402

from schools.models import (  # noqa: E402
    School,
    ClassRoom,
    Subject,
    Exam,
    MarkSheet,
    Student,
    StudentMark,
    SubjectAllocation,
)


def clamp(value, low, high):
    return max(low, min(value, high))


def parse_args():
    parser = argparse.ArgumentParser(description="Seed subject scores for an existing school/year.")
    parser.add_argument("--school", required=True, help="School name (exact match).")
    parser.add_argument("--year", type=int, required=True, help="Academic year to seed.")
    parser.add_argument("--class", dest="class_name", default=None, help="Optional class name filter.")
    parser.add_argument("--out-of", type=int, default=100, help="Marks out of (default 100).")
    parser.add_argument("--mean", type=float, default=60.0, help="Mean percentage (default 60).")
    parser.add_argument("--std", type=float, default=12.0, help="Std dev percentage (default 12).")
    parser.add_argument("--min", dest="min_pct", type=float, default=30.0, help="Minimum percentage (default 30).")
    parser.add_argument("--max", dest="max_pct", type=float, default=95.0, help="Maximum percentage (default 95).")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing scores.")
    parser.add_argument("--publish", action="store_true", help="Set created mark sheets to published.")
    parser.add_argument("--use-allocations", action="store_true", help="Restrict to subject allocations when available.")
    return parser.parse_args()


def select_students(school, classroom, subject, use_allocations):
    qs = Student.objects.filter(school=school, classroom=classroom)
    if not use_allocations:
        return qs

    allocated_ids = SubjectAllocation.objects.filter(
        subject=subject,
        student__school=school,
        student__classroom=classroom,
    ).values_list('student_id', flat=True)

    if allocated_ids.exists():
        return qs.filter(id__in=allocated_ids)
    return qs


def generate_score(out_of, mean_pct, std_pct, min_pct, max_pct):
    pct = random.gauss(mean_pct, std_pct)
    pct = clamp(pct, min_pct, max_pct)
    return round((out_of * pct) / 100.0, 1)


@transaction.atomic
def main():
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    school = School.objects.filter(name=args.school).first()
    if not school:
        print(f"School not found: {args.school}")
        return

    exams = Exam.objects.filter(school=school, year=args.year).order_by('term', 'title')
    if not exams.exists():
        print(f"No exams found for {school.name} in {args.year}. Create exams first.")
        return

    classrooms = ClassRoom.objects.filter(school=school).order_by('name')
    if args.class_name:
        classrooms = classrooms.filter(name=args.class_name)

    subjects = Subject.objects.filter(school=school).order_by('name')

    total_created = 0
    total_updated = 0
    total_skipped = 0
    marksheets_created = 0

    for exam in exams:
        for classroom in classrooms:
            for subject in subjects:
                marksheet, created = MarkSheet.objects.get_or_create(
                    exam=exam,
                    school_class=classroom,
                    subject=subject,
                    defaults={
                        'term': exam.term,
                        'out_of': args.out_of,
                        'status': 'published' if args.publish else 'draft',
                        'created_by': None,
                    },
                )
                if created:
                    marksheets_created += 1
                elif args.publish and marksheet.status != 'published':
                    marksheet.status = 'published'
                    marksheet.save(update_fields=['status'])

                students = select_students(school, classroom, subject, args.use_allocations)
                for student in students:
                    score = generate_score(args.out_of, args.mean, args.std, args.min_pct, args.max_pct)
                    mark_obj, created_mark = StudentMark.objects.get_or_create(
                        marksheet=marksheet,
                        student=student,
                        defaults={'score': score},
                    )
                    if created_mark:
                        total_created += 1
                    else:
                        if args.overwrite:
                            mark_obj.score = score
                            mark_obj.save(update_fields=['score'])
                            total_updated += 1
                        else:
                            total_skipped += 1

    print("--- Seed Year Scores Complete ---")
    print(f"School: {school.name}")
    print(f"Year: {args.year}")
    print(f"Exams processed: {exams.count()}")
    print(f"Classes processed: {classrooms.count()}")
    print(f"Subjects processed: {subjects.count()}")
    print(f"MarkSheets created: {marksheets_created}")
    print(f"Marks created: {total_created}")
    print(f"Marks updated: {total_updated}")
    print(f"Marks skipped (existing): {total_skipped}")


if __name__ == "__main__":
    main()
