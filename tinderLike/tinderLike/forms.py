from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    # first_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2")