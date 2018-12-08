from django import forms
from .models import Feedback
from captcha.fields import CaptchaField

class FeedbackForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = Feedback
        fields = ('message',)