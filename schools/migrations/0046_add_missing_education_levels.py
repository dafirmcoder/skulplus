from django.db import migrations


def add_levels(apps, schema_editor):
    EducationLevel = apps.get_model('schools', 'EducationLevel')
    level_names = [
        'Pre School',
        'Kindergarten',
        'Lower Primary',
        'Upper Primary',
        'Lower Secondary',
        'Upper Secondary (IGCSE)',
        'Junior',
        'Senior',
        'A Level',
    ]
    for name in level_names:
        EducationLevel.objects.get_or_create(name=name)


def remove_levels(apps, schema_editor):
    EducationLevel = apps.get_model('schools', 'EducationLevel')
    level_names = [
        'Pre School',
        'Kindergarten',
        'Lower Secondary',
        'Upper Secondary (IGCSE)',
        'A Level',
    ]
    EducationLevel.objects.filter(name__in=level_names).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('schools', '0045_school_cambridge_fields'),
    ]

    operations = [
        migrations.RunPython(add_levels, remove_levels),
    ]
