from django.db import migrations, models
import django.db.models.deletion


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
    ]
