from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question
import datetime
import json


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(
            question_text="Future Question", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(
            question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultViewTests(TestCase):
    def test_total_vote_count_response(self):
        """The result view must display the total response
        that count every vote in the question.
        """
        question = create_question(question_text="Some Question", days=0)
        question.choice_set.create(choice_text="Test A", votes=5)
        question.choice_set.create(choice_text="Test B", votes=3)

        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)
        self.assertEquals(response.context["total_vote_count"], 8)
        self.assertContains(response, "8 votes")

    def test_vote_result_json(self):
        """The vote result that contain choice_text and votes on every choices
        in json format that must be sent to Google Chart API
        to render the pie chart.
        """
        question = create_question(question_text="Some Question", days=0)
        question.choice_set.create(choice_text="Test A", votes=2)
        question.choice_set.create(choice_text="Test B", votes=1)
        question.choice_set.create(choice_text="Test C", votes=0)

        url = reverse('polls:results', args=(question.id,))
        response = self.client.get(url)
        # Convert the vote_results back to python readable data
        vote_results_list = json.loads(response.context["vote_results"])
        self.assertEquals(vote_results_list, [
            ["Test A", 2],
            ["Test B", 1],
            ["Test C", 0]
        ])


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_just_published_question(self):
        """
        is_published() returns True when the pub_date is less than
        or equal to the current time.
        """
        published_question = create_question("Published question", 0)
        self.assertTrue(published_question.is_published())

    def test_is_published_with_future_question(self):
        """
        is_published() returns False when the pub_date is gether than
        the current time.
        """
        future_question = create_question("Unpublushed question", 1)
        self.assertFalse(future_question.is_published())
