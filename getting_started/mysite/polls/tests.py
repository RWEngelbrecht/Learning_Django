import datetime as dt

from django.test import TestCase
from django.utils import timezone as tz
from django.urls import reverse

from .models import Question, Choice

def create_question(question_text, days=0) -> Question:
  """
  Creates and returns Question with given question_text and
  publish at given number of days offset to now
  question_text: str
  days: n >= 0 or n < 0
  """
  time = tz.now() + dt.timedelta(days=days)
  return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(choice_text, question) -> Choice:
  return Choice.objects.create(question=question, choice_text=choice_text)

class QuestionModelTests(TestCase):

  def test_was_published_recently_with_future_question(self) -> bool:
    time = tz.now() + dt.timedelta(days=30)
    future_question = Question(pub_date=time)
    self.assertIs(future_question.was_published_recently(), False)

  def test_was_published_recently_with_old_question(self) -> bool:
    time = tz.now() - dt.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(), False)

  def test_was_published_recently_with_recent_question(self) -> bool:
    time = tz.now() - dt.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
  def test_no_questions(self):
    """
    If no Questions exist, displays appropriate message
    """
    res = self.client.get(reverse('polls:index'))
    self.assertEqual(res.status_code, 200)
    self.assertContains(res, 'No polls available.')
    self.assertQuerysetEqual(res.context['latest_question_list'], [])

  def test_past_questions(self):
    """
    Displays questions from the past
    """
    q = create_question("Does the past exist?", -30)
    create_choice("Who knows", q)
    res = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(res.context['latest_question_list'], [q])

  def test_future_questions(self):
    """
    Does not display questions with pub_date set in the future
    """
    create_question("Does the future exits?", 30)
    res = self.client.get(reverse('polls:index'))
    self.assertContains(res, 'No polls available.')

  def test_future_and_past_questions(self):
    """
    Displays correct questions if both future and past
    Questions exist in DB
    """
    q1 = create_question("Does the future exits?", 30)
    q2 = create_question("Does the past exist?", -30)
    create_choice("Who knows", q1)
    create_choice("Who knows", q2)
    res = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(res.context['latest_question_list'], [q2])

  def test_multiple_past_questions(self):
    q1 = create_question("Does the past exist?", -30)
    q2 = create_question("Or is time not linear?", -2)
    create_choice("Who knows", q1)
    create_choice("Who knows", q2)
    res = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(res.context['latest_question_list'], [q2,q1])

  def test_question_with_choices(self):
    q = create_question("Is this a test?")
    create_choice("Yes", q)
    res = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(res.context['latest_question_list'], [q])

  def test_question_without_choices(self):
    q = create_question("Is this a test?")
    res = self.client.get(reverse('polls:index'))
    self.assertQuerysetEqual(res.context['latest_question_list'], [])

class QuestionDetailViewTests(TestCase):
  def test_future_question(self):
    q = create_question("Is this question sent by Skynet?", 16425)
    res = self.client.get(reverse('polls:detail', args=(q.id,)))
    self.assertEqual(res.status_code, 404)

  def test_past_quesion(self):
    q = create_question("Did Sarah Connor decide enough is enough?", -16425)
    res = self.client.get(reverse('polls:detail', args=(q.id,)))
    self.assertContains(res ,q.question_text)

class QuestionResultsViewTests(TestCase):
  def test_future_question(self):
    q = create_question("Is this question sent by Skynet?", 16425)
    res = self.client.get(reverse('polls:results', args=(q.id,)))
    self.assertEqual(res.status_code, 404)

  def test_past_quesion(self):
    q = create_question("Did Sarah Connor decide enough is enough?", -16425)
    res = self.client.get(reverse('polls:results', args=(q.id,)))
    self.assertContains(res ,q.question_text)