from django.core.management.base import BaseCommand
from schools.models import Teacher


class Command(BaseCommand):
    help = 'Sync teacher usernames to match their email addresses'

    def handle(self, *args, **options):
        updated_count = 0
        teachers = Teacher.objects.all()
        
        for teacher in teachers:
            if teacher.user.email and teacher.user.username != teacher.user.email.lower():
                old_username = teacher.user.username
                teacher.user.username = teacher.user.email.lower()
                teacher.user.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Updated {old_username} → {teacher.user.username}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTotal updated: {updated_count} teachers')
        )
