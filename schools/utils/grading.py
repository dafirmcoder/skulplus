def get_level_and_points_for_score(student, subject, score, out_of, term):
    """
    Unified CBC grading logic for both Lower and Upper Primary.
    Adjust this logic to match your real grading engine from get_suggested_comments.
    """
    percent = (score / out_of) * 100 if out_of else 0
    class_name = getattr(getattr(student, 'current_class', None), 'name', None) or getattr(getattr(student, 'classroom', None), 'name', None)
    # Example: Lower Primary
    if class_name in ["Grade 1", "Grade 2", "Grade 3"]:
        if percent >= 80:
            return "Exceeding Expectation", 4
        elif percent >= 60:
            return "Meeting Expectation", 3
        elif percent >= 40:
            return "Approaching Expectation", 2
        else:
            return "Below Expectation", 1
    # Example: Upper Primary
    else:
        if percent >= 75:
            return "Exceeding Expectation", 4
        elif percent >= 50:
            return "Meeting Expectation", 3
        elif percent >= 30:
            return "Approaching Expectation", 2
        else:
            return "Below Expectation", 1
