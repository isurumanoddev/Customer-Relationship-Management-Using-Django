from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from accounts.models import Order, Customer
from django import forms

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ["user"]


class CreateUserForm(UserCreationForm):
    # phone_number = forms.CharField(label="phone_number", max_length=10)
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]





