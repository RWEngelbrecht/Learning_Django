import datetime as dt
from django.db import models
from django.utils import timezone as tz

class Question(models.Model):
    def __str__(self) -> str:
        return self.question_text

    def was_published_recently(self):
        now = tz.now()
        return now >= self.pub_date >= now - dt.timedelta(days=1)

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    def __str__(self) -> str:
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


