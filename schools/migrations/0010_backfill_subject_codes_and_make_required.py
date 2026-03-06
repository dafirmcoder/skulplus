from django.db import migrations, models


def generate_code(name):
    # simple code generator: take uppercase initials and a numeric hash
    if not name:
        return 'SUBJ'
    parts = name.split()
    initials = ''.join(p[0].upper() for p in parts if p)
    return (initials + '_' + str(abs(hash(name)) % 1000))[:20]


def forwards(apps, schema_editor):
    Subject = apps.get_model('schools', 'Subject')
    for subj in Subject.objects.filter(code__isnull=True) | Subject.objects.filter(code=''):
        subj.code = generate_code(subj.name)
        subj.save()


def backwards(apps, schema_editor):
    # no-op (we won't revert generated codes)
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0009_subject_code_subject_short_name_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
        migrations.AlterField(
            model_name='subject',
            name='code',
            field=models.CharField(max_length=20),
        ),
    ]
