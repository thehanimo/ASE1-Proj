from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView
from ..models import User
from ..forms import PasswordResetForm, NewPasswordForm
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from ..tokens import account_activation_token
from django.core.mail import EmailMessage

def home(request):
	if request.user.is_authenticated:
		if request.user.user_type == 2:
			return redirect('agent:home')
		elif request.user.user_type == 1:
			return redirect('customer:home')
		elif request.user.user_type == 3:
			return redirect('executive:home')
		elif request.user.is_superuser == 1:
			return redirect('/admin')

	return render(request, 'userAuth/home.html')


def password_reset(request):
	form = PasswordResetForm()
	if request.method=='POST':
		form = PasswordResetForm(request.POST)
		if form.is_valid():
			to_email = form.cleaned_data.get('email')
			user = User.objects.get(email=to_email)
			print(user.pk)
			if user:
				current_site = get_current_site(request)
				mail_subject = 'Reset your Password.'
				message = render_to_string('registration/pass_reset_email.html', {
					'user': user,
					'domain': current_site.domain,
					'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
					'token':account_activation_token.make_token(user),
				})
				email = EmailMessage(
							mail_subject, message, to=[to_email]
				)
				email.send()
			return render_to_response('registration/newPass.html')
	return render(request, 'registration/password_reset.html', {'form':form})

def new_password(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.email_verified = True
		form = NewPasswordForm()
		if request.method=='POST':
			form = NewPasswordForm(request.POST)
			if form.is_valid():
				form.save(user)
				login(request, user)
				return redirect('/')
		return render(request, 'registration/new_password.html', {'form':form})
	else:
		return render(request, 'registration/activation_err.html')

@login_required(login_url='forbidden')
def change_password(request):
	form = NewPasswordForm()
	if request.method=='POST':
		form = NewPasswordForm(request.POST)
		if form.is_valid():
			user = request.user
			form.save(user)
			login(request, user)
			return redirect('/')
	return render(request, 'registration/new_password.html', {'form':form})

