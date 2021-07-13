import pytest

from django.contrib.auth.models import AnonymousUser, User
from mixer.backend.django import mixer
from django.test import RequestFactory, TestCase
from django.urls import reverse

from products.views import product_detail

@pytest.mark.django_db
class TestViews(TestCase):

  # setUpClass will execute before any other tests run
  @classmethod
  def setUpClass(cls):
    super(TestViews, cls).setUpClass()
    mixer.blend('products.Product')
    cls.factory = RequestFactory()

  def test_product_detail_authenticated(self):
    path = reverse('detail', kwargs={'pk': 1})
    request = self.factory.get(path)
    request.user = mixer.blend(User)

    response = product_detail(request, pk=1)
    assert response.status_code == 200

  def test_product_detail_unauthenticated(self):
    path = reverse('detail', kwargs={'pk': 1})
    request = self.factory.get(path)
    request.user = AnonymousUser()

    response = product_detail(request, pk=1)
    assert 'accounts/login' in response.url