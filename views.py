from django.shortcuts import render, get_object_or_404
from .models import Course, Lesson, Question, Choice, Submission


def submit(request, exam_id):
    if request.method == 'POST':
        submission = Submission.objects.create(user=request.user)

        selected_choices = request.POST.getlist('choices')

        for choice_id in selected_choices:
            choice = Choice.objects.get(id=choice_id)
            submission.choices.add(choice)

        return show_exam_result(request, submission.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    choices = submission.choices.all()

    total_score = 0
    total_possible = 0

    questions = Question.objects.all()

    for question in questions:
        total_possible += question.grade
        correct_choices = question.choice_set.filter(is_correct=True)

        selected_choices = choices.filter(question=question)

        if set(correct_choices) == set(selected_choices):
            total_score += question.grade

    score_percent = int((total_score / total_possible) * 100) if total_possible > 0 else 0

    context = {
        'score': score_percent,
        'total': total_possible,
        'choices': choices
    }

    return render(request, 'onlinecourse/exam_result.html', context)