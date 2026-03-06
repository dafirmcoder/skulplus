from django.db import migrations


def create_primary_levels(apps, schema_editor):
    EducationLevel = apps.get_model('schools', 'EducationLevel')
    for level in ['Lower Primary', 'Upper Primary']:
        EducationLevel.objects.get_or_create(name=level)


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0035_alter_educationlevel_id_alter_pathway_id'),
    ]

    operations = [
        migrations.RunPython(create_primary_levels),
    ]
