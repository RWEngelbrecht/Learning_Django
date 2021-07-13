from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Product

@login_required
def product_detail(req, pk):
  product = get_object_or_404(Product, pk=pk)
  return render(req, 'products/product_detail.html', {'product': product})
