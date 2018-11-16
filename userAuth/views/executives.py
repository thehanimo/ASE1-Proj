from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from ..tokens import account_activation_token
from django.core.mail import EmailMessage

from ..decorators import executive_required
from ..forms import ExecutiveSignUpForm, ExecutiveDetailsForm
from ..models import User, Executive

class ExecutiveSignUpView(CreateView):
	model = User
	form_class = ExecutiveSignUpForm
	template_name = 'registration/signup_form.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 3
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save(commit=False)
		user.is_active = False
		user.save()
		current_site = get_current_site(self.request)
		mail_subject = 'Activate your account.'
		message = render_to_string('registration/exec_acc_active_email.html', {
			'user': user,
			'domain': current_site.domain,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
			'token':account_activation_token.make_token(user),
		})
		to_email = form.cleaned_data.get('email')
		email = EmailMessage(
					mail_subject, message, to=[to_email]
		)
		email.send()
		return render_to_response('registration/newUser.html')

@method_decorator([login_required, executive_required], name='dispatch')
class HomeView(ListView):
	template_name = 'userAuth/executives/home.html'

	def get_queryset(self):
		return []

@method_decorator([login_required, executive_required], name='dispatch')
class ExecutiveDetailsView(UpdateView):
	model = Executive
	template_name = "registration/details.html"
	form_class = ExecutiveDetailsForm

	def get_object(self, *args, **kwargs):
		user = self.request.user
		return user.executive

	def get_success_url(self, *args, **kwargs):
		return reverse("executive:home")

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_verified = True
        user.save()
        return render(request, 'registration/exec_activation_suc.html')
    else:
        return render(request, 'registration/activation_err.html')