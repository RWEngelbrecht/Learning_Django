from celery import shared_task
from time import sleep
from django.core.mail import send_mail

@shared_task
def sleepy(duration):
  sleep(duration)
  return None

@shared_task
def send_email_task():
  send_mail('celery task worked!',
  'this is proof that this thing worked',
  "no-reply@mydomain.com",
  recipient_list=['lileka9378@godpeed.com']
  )
  return None