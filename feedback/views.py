from django.shortcuts import render
from .models import Feedback
from django.views.generic import CreateView
from .forms import FeedbackForm

from django.shortcuts import redirect,render
# Create your views here.

class FeedbackView(CreateView):
	model = Feedback
	form_class = FeedbackForm
	template_name = 'feedback/feedback.html'

	def form_valid(self,form):
		form.save()
		return render(self.request, 'feedback/feedback-success.html')