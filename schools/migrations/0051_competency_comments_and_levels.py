from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0050_school_calendar_event_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcompetency',
            name='comment_manual',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentcompetency',
            name='comment_text',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='studentcompetency',
            name='level',
            field=models.CharField(choices=[('CBC_EMERGING', 'Emerging'), ('CBC_DEVELOPING', 'Developing'), ('CBC_APPROACHING', 'Approaching Expectation'), ('CBC_MEETING', 'Meeting Expectation'), ('CBC_EXCEEDING', 'Exceeding Expectation'), ('CAM_BEGINNING', 'Beginning'), ('CAM_DEVELOPING', 'Developing'), ('CAM_SECURE', 'Secure'), ('CAM_ADVANCED', 'Advanced'), ('CAM_MASTERY', 'Mastery')], max_length=20),
        ),
        migrations.CreateModel(
            name='StudentCompetencySummary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_comment', models.TextField(blank=True, default='')),
                ('comment_manual', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competency_summaries', to='schools.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competency_summaries', to='schools.student')),
            ],
            options={
                'unique_together': {('student', 'exam')},
            },
        ),
    ]
