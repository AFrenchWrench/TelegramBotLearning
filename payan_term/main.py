def calculate_final_grade(exam_score, homework_score, attendance_score):
    if (
        (exam_score < 0 or exam_score > 100)
        or (homework_score < 0 or homework_score > 100)
        or (attendance_score < 0 or attendance_score > 100)
    ):
        return "Invalid input"
    else:
        final_score = (
            (exam_score * 0.6) + (homework_score * 0.3) + (attendance_score * 0.1)
        )
        return round(final_score, 2)
