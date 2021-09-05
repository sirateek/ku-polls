import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Question models representing each of polls question.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date Published")

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

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """Choice models representing the choice corresponding
    to each of poll question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text
