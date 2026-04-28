from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaV3


class SignUpForm(UserCreationForm):
	captcha = ReCaptchaV3()

	class Meta(UserCreationForm.Meta):
		fields = UserCreationForm.Meta.fields


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	captcha = ReCaptchaV3()
	