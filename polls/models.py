"""The model for Polls application."""
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Question models representing each of polls question."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date Published")
    end_date = models.DateTimeField(
        "Date the poll will close.", default=timezone.now)

    def was_published_recently(self):
        """Check if question was published in last 24 hours.

        Returns:
            Boolean telling whether the question was published
            in the last 24 hours
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Check if the current time is greater than or equal to pub_date.

        Returns:
            Boolean telling the publish status of the question.
        """
        return timezone.now() >= self.pub_date
    is_published.boolean = True
    is_published.short_description = 'Published?'

    def can_vote(self):
        """Check if the current time is between the pub_date and end_date inclusively.

        Returns:
           Boolean telling whether question is accepting the vote or not.
        """
        return self.pub_date <= timezone.now() <= self.end_date
    can_vote.boolean = True
    can_vote.short_description = "Accept new vote?"

    def __str__(self):
        """Get the question text.

        Returns:
            str: Question Text
        """
        return self.question_text


class Choice(models.Model):
    """Choice models representing the choice corresponding to each of poll question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        return Vote.objects.filter(choice=self).count()

    def __str__(self):
        """Get the choice text.

        Returns:
            str: Choice Text.
        """
        return self.choice_text


class Vote(models.Model):
    """Vote object that represent the user's vote and choice that they voted."""
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
