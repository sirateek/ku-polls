"""Unittesting for Polls app model and view."""
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Question, Vote
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


class QuestionIndexViewTests(TestCase):
    """The test for Question index view."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed onthe index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    """Test for Question Detail view."""

    def test_future_question(self):
        """Test error and redirect of not opened question in detail view.

        Accessing detail view of a question with a pub_date in the future
        will be redirected back to the index page with the error message.
        """
        future_question = create_question(
            question_text="Future Question", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        # This response should contain the redirect code to index page.
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/polls/")
        # The index page should contain message that question is not opened.
        index_response = self.client.get(response.url)
        self.assertContains(
            index_response, text=f"Question no. {future_question.id} is not accepting the vote yet.", status_code=200)

    def test_past_question_not_accepting_the_vote(self):
        """Test error and redirect of can't vote question in detail view.

        An attempt accessing detail view of a question stopped accepting
        the new vote will be redirect back to the index page with the error message.
        """
        past_question = create_question(
            question_text='Past Question.', days=-1, end_in_days=-1)
        url = reverse('polls:detail', args=(past_question.id,))
        # This response should contain the redirect code to index page.
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/polls/")
        # The index page should contain message that question is not opened.
        index_response = self.client.get(response.url)
        self.assertContains(
            index_response,
            text=f"Question no. {past_question.id} is not accepting the vote anymore.",
            status_code=200
        )

    def test_past_question_accepting_the_vote(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(
            question_text='Past Question.', days=-1, end_in_days=1)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultViewTests(TestCase):
    """Test for Question Result View."""
    user_count = 0

    def vote_to_choice(self, choice):
        user = User(username=f"TestUser{self.user_count}")
        user.save()
        self.user_count += 1
        Vote.objects.create(user=user, choice=choice).save()

    def test_total_vote_count_response(self):
        """The result view must display the total response that count every vote in the question."""
        question = create_question(question_text="Some Question", days=0)
        choice_a = question.choice_set.create(choice_text="Test A")
        choice_b = question.choice_set.create(choice_text="Test B")
        self.vote_to_choice(choice_a)
        self.vote_to_choice(choice_b)

        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)
        self.assertEquals(response.context["total_vote_count"], 2)
        self.assertContains(response, "2 votes")

    def test_vote_result_json(self):
        """Test he vote result that contain choice_text and votes on every choices in json format."""
        question = create_question(question_text="Some Question", days=0)
        choice_a = question.choice_set.create(choice_text="Test A")
        choice_b = question.choice_set.create(choice_text="Test B")
        choice_c = question.choice_set.create(choice_text="Test C")
        self.vote_to_choice(choice_a)
        self.vote_to_choice(choice_b)

        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)
        # Convert the vote_results back to python readable data
        vote_results_list = json.loads(response.context["vote_results"])
        self.assertEquals(vote_results_list, [
            ["Test A", 1],
            ["Test B", 1],
            ["Test C", 0]
        ])


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
