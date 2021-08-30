from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    published_date = models.DateTimeField("Date Published")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text
