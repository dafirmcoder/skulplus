from django.db import migrations, models


def seed_cbc_primary_comments(apps, schema_editor):
    CompetencyComment = apps.get_model('schools', 'CompetencyComment')
    Subject = apps.get_model('schools', 'Subject')

    lower_levels = ["EE", "ME", "AE", "BE"]
    upper_levels = ["EE1", "EE2", "ME1", "ME2", "AE1", "AE2", "BE1", "BE2"]

    general_templates = {
        "Lower Primary": {
            "EE": [
                "Consistently exceeds expectations and demonstrates strong understanding.",
                "Shows outstanding mastery and applies skills confidently.",
                "Excellent performance with clear understanding and creativity.",
                "Demonstrates exceptional competence and independence.",
                "Highly skilled and consistently delivers quality work.",
                "Outstanding progress and surpasses expected standards.",
                "Shows excellent grasp and applies learning in new contexts.",
            ],
            "ME": [
                "Meets expectations and shows steady understanding.",
                "Demonstrates good competence with minor support.",
                "Shows consistent progress and meets required standards.",
                "Competent performance with occasional guidance.",
                "Applies skills appropriately and meets expectations.",
                "Good effort and understanding across tasks.",
                "Shows solid performance at the expected level.",
            ],
            "AE": [
                "Approaching expectations; needs more practice.",
                "Shows developing understanding with support needed.",
                "Progressing but requires reinforcement of key skills.",
                "Needs additional guidance to meet expectations.",
                "Demonstrates partial understanding; more practice required.",
                "Improving steadily; continue targeted support.",
                "Shows potential but needs more consistency.",
            ],
            "BE": [
                "Below expectations; requires significant support.",
                "Needs focused assistance to grasp key skills.",
                "Requires more time and practice to improve.",
                "Limited understanding; intensive support recommended.",
                "Struggles with core skills; needs close guidance.",
                "Below expected level; extra practice is essential.",
                "Requires consistent support to build basic competence.",
            ],
        },
        "Upper Primary": {
            "EE1": [
                "Exceptional performance; consistently exceeds expectations.",
                "Outstanding mastery and application of skills.",
                "Excellent understanding with confident application.",
                "Shows exceptional competence and independence.",
                "Highly proficient with exemplary work quality.",
                "Consistently outstanding across tasks.",
                "Demonstrates superior understanding and creativity.",
            ],
            "EE2": [
                "Very strong performance; exceeds expectations.",
                "Shows high competence and reliable application.",
                "Excellent effort with strong understanding.",
                "Performs above expected standard consistently.",
                "Demonstrates advanced understanding.",
                "Shows strong mastery with minor refinement needed.",
                "Very good performance and application.",
            ],
            "ME1": [
                "Meets expectations with good competence.",
                "Shows reliable understanding and application.",
                "Good performance with occasional support.",
                "Consistently meets the expected standard.",
                "Competent and progressing well.",
                "Applies skills appropriately and effectively.",
                "Good effort and understanding across tasks.",
            ],
            "ME2": [
                "Generally meets expectations; needs minor support.",
                "Shows adequate understanding with some guidance.",
                "Competent but requires consolidation.",
                "Progressing steadily toward expectations.",
                "Meets many expectations with support.",
                "Shows developing competence.",
                "Fair performance with room for improvement.",
            ],
            "AE1": [
                "Approaching expectations; needs more practice.",
                "Shows developing understanding.",
                "Requires guidance to meet expectations.",
                "Progressing but needs reinforcement.",
                "Improving but not yet consistent.",
                "Partial understanding; more practice required.",
                "Needs additional support to improve.",
            ],
            "AE2": [
                "Below expectations; requires more support.",
                "Limited understanding; needs reinforcement.",
                "Requires focused practice to improve.",
                "Needs consistent guidance.",
                "Shows basic understanding only.",
                "Progress is slow; needs support.",
                "Requires targeted intervention.",
            ],
            "BE1": [
                "Significantly below expectations.",
                "Struggles with key skills; needs support.",
                "Requires intensive guidance to improve.",
                "Needs substantial practice and support.",
                "Limited achievement; requires close monitoring.",
                "Below expected level; extra help needed.",
                "Needs consistent intervention to progress.",
            ],
            "BE2": [
                "Very low performance; urgent support needed.",
                "Requires immediate intervention and guidance.",
                "Severely limited understanding.",
                "Needs intensive support to build basics.",
                "Struggles significantly with core skills.",
                "Urgent remediation required.",
                "Requires close supervision and support.",
            ],
        },
    }

    subject_templates = {
        "math": [
            "Demonstrates strong number sense and accurate calculations.",
            "Applies mathematical concepts correctly in problem-solving.",
            "Shows good understanding of operations and patterns.",
            "Needs more practice with mathematical procedures.",
            "Solves problems effectively and checks work.",
            "Shows developing reasoning in mathematics.",
            "Requires support to improve accuracy and speed.",
        ],
        "english": [
            "Reads fluently and expresses ideas clearly.",
            "Uses appropriate vocabulary and grammar in writing.",
            "Shows strong comprehension of texts.",
            "Needs more practice with spelling and sentence structure.",
            "Communicates ideas confidently in speaking.",
            "Shows improvement in reading and writing skills.",
            "Requires support to improve comprehension.",
        ],
        "science": [
            "Demonstrates good understanding of scientific concepts.",
            "Applies inquiry skills and observes accurately.",
            "Shows curiosity and engages well in experiments.",
            "Needs more practice with scientific explanations.",
            "Understands cause and effect in science topics.",
            "Shows progress in scientific reasoning.",
            "Requires support to grasp key concepts.",
        ],
        "social": [
            "Shows good understanding of society and environment.",
            "Explains social concepts clearly and accurately.",
            "Demonstrates awareness of community roles.",
            "Needs more practice with social studies content.",
            "Participates well in discussions about society.",
            "Shows developing understanding of civic issues.",
            "Requires support to improve content knowledge.",
        ],
    }

    def ensure_variants(level_name, performance_level, subject_id, comments):
        existing = CompetencyComment.objects.filter(
            education_level=level_name,
            performance_level=performance_level,
            subject_id=subject_id,
        ).count()
        missing = max(0, 7 - existing)
        if missing <= 0:
            return
        for idx in range(missing):
            CompetencyComment.objects.create(
                education_level=level_name,
                performance_level=performance_level,
                subject_id=subject_id,
                comment_text=comments[idx % len(comments)],
            )

    for level_name, levels in (("Lower Primary", lower_levels), ("Upper Primary", upper_levels)):
        for perf in levels:
            ensure_variants(level_name, perf, None, general_templates[level_name][perf])

    subject_name_map = {
        "math": ["mathematics"],
        "english": ["english"],
        "science": ["science", "integrated science", "environmental", "science & technology"],
        "social": ["social studies"],
    }

    subjects = list(Subject.objects.all().select_related('education_level'))
    for subject in subjects:
        level_name = subject.education_level.name if subject.education_level else None
        if level_name not in ("Lower Primary", "Upper Primary"):
            continue
        name = (subject.name or "").lower()
        subject_key = None
        for key, patterns in subject_name_map.items():
            if any(p in name for p in patterns):
                subject_key = key
                break
        if not subject_key:
            continue
        levels = lower_levels if level_name == "Lower Primary" else upper_levels
        for perf in levels:
            ensure_variants(level_name, perf, subject.id, subject_templates[subject_key])


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0037_alter_subject_unique_constraints'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentmark',
            name='level',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='studentmark',
            name='points',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RunPython(seed_cbc_primary_comments, migrations.RunPython.noop),
    ]
