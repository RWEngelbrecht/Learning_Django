from django import forms
from .models import Pizza

class PizzaForm(forms.Form):
  toppings = forms.MultipleChoiceField(
    choices=[('pep', 'Pepperoni'), ('cheese', 'Cheese'), ('pine', 'Pineapple')],
    widget=forms.CheckboxSelectMultiple
    )
  size = forms.ChoiceField(label="Size", choices=[
    ('small', 'Small'),
    ('medium', 'Medium'),
    ('large', 'Large')
    ])

# class PizzaForm(forms.ModelForm):
#   class Meta:
#     model = Pizza
#     fields = ['topping1', 'topping2', 'size']
#     labels = {'topping1': 'Topping 1', 'topping2': 'Topping 2'}