from django.shortcuts import render
from .forms import PizzaForm

def home(request):
  return render(request, 'pizza/home.html')


def order(request):
  if request.method == 'POST':
    filled_form = PizzaForm(request.POST, request.FILES)
    if filled_form.is_valid():
      note = f'Thanks for ordering! Your {filled_form.cleaned_data["size"]} {filled_form.cleaned_data["topping1"]} and {filled_form.cleaned_data["topping2"]} \'za is probably on its way...'
      new_form = PizzaForm()
      return render(request, 'pizza/order.html', {'pizzaform':new_form, 'note': note})
  else:
    form = PizzaForm()
    return render(request, 'pizza/order.html', {'pizzaform':form})
