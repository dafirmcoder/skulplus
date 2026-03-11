from django.db import migrations, models
import django.db.models.deletion


def seed_strands(apps, schema_editor):
    School = apps.get_model('schools', 'School')
    EducationLevel = apps.get_model('schools', 'EducationLevel')
    LearningStrand = apps.get_model('schools', 'LearningStrand')
    SubStrand = apps.get_model('schools', 'SubStrand')

    def get_level(name):
        return EducationLevel.objects.filter(name=name).first()

    cambridge_levels = {'Kindergarten'}
    cbe_levels = {'Pre School'}

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

    for school in School.objects.all():
        if school.school_type == 'CAMBRIDGE':
            level = get_level('Kindergarten')
            if not level:
                continue
            for strand_name, subs in cambridge_strands.items():
                strand, _ = LearningStrand.objects.get_or_create(
                    school=school,
                    education_level=level,
                    name=strand_name
                )
                for sub_name in subs:
                    SubStrand.objects.get_or_create(learning_strand=strand, name=sub_name)
        else:
            level = get_level('Pre School')
            if not level:
                continue
            for strand_name, subs in cbe_strands.items():
                strand, _ = LearningStrand.objects.get_or_create(
                    school=school,
                    education_level=level,
                    name=strand_name
                )
                for sub_name in subs:
                    SubStrand.objects.get_or_create(learning_strand=strand, name=sub_name)


def unseed_strands(apps, schema_editor):
    LearningStrand = apps.get_model('schools', 'LearningStrand')
    SubStrand = apps.get_model('schools', 'SubStrand')
    # Remove only strands created by this seed (matching names)
    strand_names = [
        'Communication & Language',
        'Physical Development',
        'Personal, Social & Emotional Development',
        'Literacy',
        'Mathematics',
        'Understanding the World',
        'Expressive Arts & Design',
        'Language Activities',
        'Mathematics Activities',
        'Environmental Activities',
        'Psychomotor & Creative Activities',
    ]
    strands = LearningStrand.objects.filter(name__in=strand_names)
    SubStrand.objects.filter(learning_strand__in=strands).delete()
    strands.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('schools', '0046_add_missing_education_levels'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningStrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('education_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.educationlevel')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_strands', to='schools.school')),
            ],
            options={
                'ordering': ['education_level__name', 'name'],
                'unique_together': {('school', 'education_level', 'name')},
            },
        ),
        migrations.CreateModel(
            name='SubStrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('learning_strand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_strands', to='schools.learningstrand')),
            ],
            options={
                'ordering': ['name'],
                'unique_together': {('learning_strand', 'name')},
            },
        ),
        migrations.CreateModel(
            name='StudentCompetency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('NOT_YET', 'Not Yet'), ('DEVELOPING', 'Developing'), ('ACHIEVED', 'Achieved'), ('EXCEEDS', 'Exceeds')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competencies', to='schools.exam')),
                ('learning_strand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.learningstrand')),
                ('recorded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competencies', to='schools.student')),
                ('sub_strand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schools.substrand')),
            ],
            options={
                'unique_together': {('student', 'exam', 'sub_strand')},
            },
        ),
        migrations.RunPython(seed_strands, unseed_strands),
    ]
