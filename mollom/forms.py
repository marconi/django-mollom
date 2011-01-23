from django import forms
from django.contrib.auth.models import User

from mollom.fields import MollomCaptchaField

class MockSignupForm(forms.Form):
    """
    A dummy signup form with basic fields.
    """
    username = forms.CharField()
    email = forms.EmailField(label="Email address")
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label="Password (again)")
    captcha = MollomCaptchaField()
