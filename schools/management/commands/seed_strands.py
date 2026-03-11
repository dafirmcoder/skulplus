from django.core.management.base import BaseCommand

from schools.models import School, EducationLevel, LearningStrand, SubStrand


class Command(BaseCommand):
    help = "Seed default strands and sub-strands for CBE (Pre School) and Cambridge (Kindergarten)."

    def handle(self, *args, **options):
        cambridge_strands = {
            'Communication & Language': ['Listening & Attention', 'Speaking', 'Understanding'],
            'Physical Development': ['Gross Motor', 'Fine Motor', 'Health & Self-Care'],
            'Personal, Social & Emotional Development': ['Self-Regulation', 'Managing Self', 'Building Relationships'],
            'Literacy': ['Comprehension', 'Word Reading', 'Writing'],
            'Mathematics': ['Number', 'Numerical Patterns'],
            'Understanding the World': ['People, Culture & Communities', 'The Natural World', 'Technology'],
            'Expressive Arts & Design': ['Creating with Materials', 'Being Imaginative & Expressive'],
        }
        cbe_strands = {
            'Language Activities': ['Listening & Speaking', 'Reading Readiness', 'Writing Readiness'],
            'Mathematics Activities': ['Number Sense', 'Patterns', 'Shapes & Space'],
            'Environmental Activities': ['Social Environment', 'Natural Environment', 'Health Practices'],
            'Psychomotor & Creative Activities': ['Creative Arts', 'Music & Movement', 'Physical Activities'],
        }

        level_kg = EducationLevel.objects.filter(name='Kindergarten').first()
        level_ps = EducationLevel.objects.filter(name='Pre School').first()

        if not level_kg or not level_ps:
            self.stdout.write(self.style.ERROR('Missing EducationLevel: Kindergarten or Pre School.'))
            return

        created_strands = 0
        created_subs = 0

        for school in School.objects.all():
            if school.school_type == 'CAMBRIDGE':
                level = level_kg
                strands = cambridge_strands
            else:
                level = level_ps
                strands = cbe_strands

            for strand_name, subs in strands.items():
                strand, s_created = LearningStrand.objects.get_or_create(
                    school=school,
                    education_level=level,
                    name=strand_name,
                )
                if s_created:
                    created_strands += 1
                for sub_name in subs:
                    sub, sub_created = SubStrand.objects.get_or_create(
                        learning_strand=strand,
                        name=sub_name,
                    )
                    if sub_created:
                        created_subs += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete. Strands created: {created_strands}, Sub-strands created: {created_subs}.'
        ))
