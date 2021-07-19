from django.shortcuts import render
from django.http import HttpResponse

from .tasks import send_email_task, sleepy

def index(request):
  send_email_task.delay()
  return HttpResponse('<h1>Task has finished!</h1>')