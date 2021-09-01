from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    """Poll Index page that displays the latest few questions
    """

    template_name = "polls/index.html"
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Question detail page that displays the question text with a form to vote
    """

    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    """Poll result page that displays the results for a particular question.
    """

    model = Question
    template_name = 'polls/results.html'


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
