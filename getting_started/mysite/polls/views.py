from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import F, Q
from django.views import generic
from django.utils import timezone as tz

from .models import Question, Choice

class IndexView(generic.ListView):
  # ListView generic view uses template called
  # <appName>/<modelName>_detail.html unless specified
  # otherwise with template_name attribute
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    # Did an inner join; can't use distinct() because DISTINCT ON doesn't work with sqlite
    questions = []
    [questions.append(question) for question in
      Question.objects
        .filter(pub_date__lte=tz.now(), choice__question=F('id'))
        .order_by('-pub_date')[:5]
      if question not in questions]
    return questions


class DetailView(generic.DetailView):
  model = Question
  # DetailView generic view uses template called
  # <appName>/<modelName>_detail.html unless specified
  # otherwise with template_name attribute
  template_name = 'polls/detail.html'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=tz.now())


class ResultsView(generic.DetailView):
  model = Question
  template_name = 'polls/results.html'

  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=tz.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
      selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
      return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "Please select a choice..."
      })
    else:
      selected_choice.votes = F('votes') + 1
      selected_choice.save()
      return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
