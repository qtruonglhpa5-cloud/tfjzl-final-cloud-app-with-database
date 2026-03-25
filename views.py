from django.shortcuts import render, get_object_or_404
from .models import Course, Lesson, Question, Choice, Submission

def show_exam_result(request, submission_id):
    # Retrieve the submission
    submission = get_object_or_404(Submission, pk=submission_id)
    choices = submission.choices.all()

    # Retrieve the course from the first choice's question -> lesson -> course
    if choices.exists():
        course = choices.first().question.lesson.course
    else:
        # Fallback if no choices selected
        course = None

    total_score = 0
    total_possible = 0
    selected_ids = []

    # Only consider questions in this course
    questions = Question.objects.filter(lesson__course=course)

    for question in questions:
        total_possible += question.grade
        correct_choices = question.choice_set.filter(is_correct=True)
        selected_choices = choices.filter(question=question)
        selected_ids += [c.id for c in selected_choices]

        # Add grade only if selected choices exactly match correct choices
        if set(correct_choices) == set(selected_choices):
            total_score += question.grade

    score_percent = int((total_score / total_possible) * 100) if total_possible > 0 else 0

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'grade': total_score,
        'possible': total_possible,
        'score': score_percent,
    }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
