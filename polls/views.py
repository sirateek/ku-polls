from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Choice, Question
from django.urls import reverse


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
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # If the Choice doesn't not exit, Render the detail view with the `error_message`
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def result(request, question_id):
    """Poll result page that displays the results for a particular question.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
