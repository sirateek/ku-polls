"""Unittesting for voting in Polls app."""

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from polls.models import Question, Vote, Choice
import datetime
import json


def create_question(question_text, days, end_in_days=0):
    """Create a question with specific days.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    end_date = timezone.now() + datetime.timedelta(days=end_in_days)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=end_date)


def create_choice(question, choice_text):
    """Create the choice for the inputted question

    Args:
        question (Question): Question Model
        choice_text (str): String for the choice_text

    Returns:
        Choice: Choice Object
    """
    choice = Choice.objects.create(question=question, choice_text=choice_text)
    choice.save()
    return choice


def create_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    user.save()
    return user


class TestVoting(TestCase):

    def setUp(self):
        self.question = create_question("Example", days=1)
        self.choice_a = create_choice(self.question, "Test")
        self.choice_b = create_choice(self.question, "Test2")
        self.vote_target_url = reverse("polls:vote", args=(self.question.id,))
        self.user = create_user("test_user", "1234")

    def vote(self, choice):
        vote_data = {
            "choice": choice.id
        }
        return self.client.post(self.vote_target_url, data=vote_data)

    def test_vote_with_logged_in(self):
        self.client.login(username="test_user", password="1234")
        response = self.vote(self.choice_a)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(
            "polls:results", args=(self.question.id,)))
        self.assertEqual(self.choice_a.votes, 1)
        self.assertEqual(self.choice_b.votes, 0)

    def test_voting_without_login(self):
        response = self.vote(self.choice_a)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, f"/accounts/login/?next=/polls/{self.question.id}/vote/")

    def test_change_vote(self):
        """User must be able to vote for only 1 choice.
        """
        self.client.login(username="test_user", password="1234")
        self.vote(self.choice_a)
        self.assertEqual(self.choice_a.votes, 1)
        self.assertEqual(self.choice_b.votes, 0)
        self.vote(self.choice_b)
        self.assertEqual(self.choice_a.votes, 0)
        self.assertEqual(self.choice_b.votes, 1)
