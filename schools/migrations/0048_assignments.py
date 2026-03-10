from django.db import migrations, models
import django.db.models.deletion
from django.core.validators import FileExtensionValidator
import schools.models


class Migration(migrations.Migration):
    dependencies = [
        ('schools', '0047_competency_strands'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(choices=[('Term 1', 'Term 1'), ('Term 2', 'Term 2'), ('Term 3', 'Term 3')], max_length=20)),
                ('year', models.IntegerField()),
                ('title', models.CharField(blank=True, default='', max_length=160)),
                ('document', models.FileField(upload_to='assignments/', validators=[FileExtensionValidator(['pdf']), schools.models._validate_pdf_size])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='schools.classroom')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='schools.school')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='schools.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='schools.teacher')),
            ],
            options={
                'ordering': ['-year', '-term', '-created_at'],
                'unique_together': {('school', 'classroom', 'subject', 'term', 'year')},
            },
        ),
    ]
