from django.http import HttpResponse


def index(request):
    """Poll Index page that displays the latest few questions
    """
    return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, question_id):
    """Question detail page that displays the question text with a form to vote
    """
    return HttpResponse(f"This is the question detail page for question {question_id}")


def vote(request, question_id):
    """Vote page that allow the user to vote on a particular question.
    """
    return HttpResponse(f"This is the vote page for question {question_id}")


def result(request, question_id):
    """Poll result page that displays the results for a particular question.
    """
    return HttpResponse(f"This is the result page for question {question_id}")
