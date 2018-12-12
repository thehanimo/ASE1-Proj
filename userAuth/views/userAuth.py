from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView, CreateView
from ..models import User, AgentApplications
from ..forms import PasswordResetForm, NewPasswordForm, AgentSignUpForm
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from userAuth.decorators import anonymous_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from ..tokens import account_activation_token
from django.core.mail import EmailMessage

def AboutUs(request):
	return render(request, 'aboutus.html')

def FAQ(request):
	return render(request, 'faq.html')

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

	return render(request, 'home.html')

def myProfile(request):
	if request.user.is_authenticated:
		if request.user.user_type == 2:
			return redirect('agent:home',aid=request.user.id)
		elif request.user.user_type == 1:
			return redirect('customer:editprofile')
		elif request.user.user_type == 3:
			return redirect('executive:viewprofile')

	return render(request, '500.html')

@method_decorator([anonymous_required], name='dispatch')
class PartnerWithUsView(CreateView):
	model = AgentApplications
	fields = ('fullname', 'email', 'phone', 'zipcode','area')
	template_name = 'registration/ag_signup_form.html'

	def form_valid(self, form):
		existing_queries = len(User.objects.filter(email=form.cleaned_data.get('email'))) + len(AgentApplications.objects.filter(email=form.cleaned_data.get('email')))
		if not existing_queries:
			new_appl = AgentApplications.objects.create(
					fullname = form.cleaned_data.get('fullname'),
					email = form.cleaned_data.get('email'),
					phone = form.cleaned_data.get('phone'),
					zipcode = form.cleaned_data.get('zipcode'),
					area = form.cleaned_data.get('area')
				)
			new_appl.save()
			return render_to_response('registration/newAgentAppl.html')
		return render_to_response('registration/rejectAgentAppl.html')

def password_reset(request):
	form = PasswordResetForm()
	if request.method=='POST':
		form = PasswordResetForm(request.POST)
		if form.is_valid():
			to_email = form.cleaned_data.get('email')
			try:
				user = User.objects.get(email=to_email)
			except User.DoesNotExist:
				user = None
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

def forbidden(request):
	return render(request, '500.html')

