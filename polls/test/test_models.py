"""Unittesting for Polls app model."""

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from polls.models import Question, Vote
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


class QuestionModelTests(TestCase):
    """Test for Question model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        future_question = create_question("Dummy question", 30)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        old_question = create_question("Dummy question", -1)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        recent_question = create_question("Dummy question", -0.99)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_just_published_question(self):
        """is_published() returns True when the current time is equal to pub_date."""
        just_published_question = create_question("Just Published question", 0)
        self.assertIs(just_published_question.is_published(), True)

    def test_is_published_with_old_question(self):
        """is_published() returns True when the current time is greater than the pub_date."""
        published_question = create_question("Published question", -1)
        self.assertIs(published_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """is_published() returns False when the current time is less than the pub_date."""
        future_question = create_question("Unpublushed question", 1)
        self.assertIs(future_question.is_published(), False)

    def test_can_vote_with_during_poll_period_question(self):
        """can_vote() returns True when the current datetime is between pub_date and end_date."""
        during_poll_period_question = create_question(
            "I'm still accepting the vote", -1, 1)
        self.assertIs(during_poll_period_question.can_vote(), True)

    def test_can_vote_with_old_question(self):
        """can_vote() returns False when the current datetime is after the poll period."""
        old_question = create_question(
            "I'm stoped accepting the new vote", -2, -1)
        self.assertIs(old_question.can_vote(), False)

    def test_can_vote_with_future_question(self):
        """can_vote() returns False when the current datetime is behind the poll period."""
        future_question = create_question("I'm still not opened yet", 1, 2)
        self.assertIs(future_question.can_vote(), False)
