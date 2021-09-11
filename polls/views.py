from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import json

from .models import Choice, Question


class IndexView(generic.ListView):
    """Poll Index page that displays the latest few questions
    """

    template_name = "polls/index.html"
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")[:5]


def detail(request, question_id):
    """Question detail page that displays the question text with a form to vote
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {
        "question": question,
    }
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    """Poll result page that displays the results for a particular question.
    """

    question = get_object_or_404(Question, pk=question_id)
    # For frontend to display the warning alert if there is no vote.
    total_vote_count = 0
    # Export choice and vote results to json
    # to be displayed piechart in frontend.
    vote_results = []
    for choice in question.choice_set.all():
        vote_results.append([choice.choice_text, choice.votes])
        total_vote_count += choice.votes
    vote_results = json.dumps(vote_results)

    context = {
        'question': question,
        'vote_results': vote_results,
        'total_vote_count': total_vote_count
    }
    return render(request, 'polls/results.html', context)


def vote(request, question_id):
    """Vote listener that accept the vote POST request from form action
     in detail page.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # If the Choice doesn't not exit,
        # Render the detail view with the `error_message`
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))
