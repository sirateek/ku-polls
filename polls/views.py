from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Question


def index(request):
    """Poll Index page that displays the latest few questions
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    """Question detail page that displays the question text with a form to vote
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def vote(request, question_id):
    """Vote page that allow the user to vote on a particular question.
    """
    return HttpResponse(f"This is the vote page for question {question_id}")


def result(request, question_id):
    """Poll result page that displays the results for a particular question.
    """
    return HttpResponse(f"This is the result page for question {question_id}")
