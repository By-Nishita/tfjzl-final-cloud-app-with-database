from django.shortcuts import render, get_object_or_404

from .models import Course, Lesson, Question, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)

    return render(
        request,
        "course_details_bootstrap.html",
        {
            "course": course,
            "lessons": lessons,
        },
    )


def exam(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = Question.objects.filter(lesson=lesson)

    return render(
        request,
        "exam.html",
        {
            "lesson": lesson,
            "questions": questions,
        },
    )


def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = Lesson.objects.filter(course=course).first()

    if lesson is None:
        return render(
            request,
            "exam_result.html",
            {
                "lesson": None,
                "score": 0,
                "total": 0,
                "results": [],
            },
        )

    questions = Question.objects.filter(lesson=lesson)

    score = 0
    results = []
    first_submission_id = None

    if request.method == "POST":

        for question in questions:

            choice_id = request.POST.get(
                f"question_{question.id}"
            )

            if choice_id:

                choice = get_object_or_404(
                    Choice,
                    id=choice_id
                )

                is_correct = choice.is_correct

                submission = Submission.objects.create(
                    question=question,
                    selected_choice=choice,
                    is_correct=is_correct,
                )

                if first_submission_id is None:
                    first_submission_id = submission.id

                if is_correct:
                    score += 1

                results.append(
                    {
                        "question": question,
                        "selected_choice": choice,
                        "is_correct": is_correct,
                    }
                )

    request.session["exam_score"] = score
    request.session["exam_total"] = questions.count()

    return render(
        request,
        "exam_result.html",
        {
            "lesson": lesson,
            "score": score,
            "total": questions.count(),
            "results": results,
            "submission_id": first_submission_id,
            "course_id": course.id,
        },
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)

    lesson = Lesson.objects.filter(course=course).first()

    score = request.session.get(
        "exam_score",
        0
    )

    total = request.session.get(
        "exam_total",
        0
    )

    return render(
        request,
        "exam_result.html",
        {
            "lesson": lesson,
            "score": score,
            "total": total,
            "submission_id": submission_id,
            "course_id": course_id,
        },
    )
