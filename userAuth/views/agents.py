from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import render, redirect, render_to_response


from ..decorators import agent_required, executive_required
from ..forms import AgentSignUpForm, AgentSignUpFormExtended
from ..models import User, Agent

@login_required
@executive_required
def AgentSignUp(request):
	form = AgentSignUpForm()
	form_extended = AgentSignUpFormExtended()
	if request.method == 'POST':
		form = AgentSignUpForm(request.POST)
		form_extended = AgentSignUpFormExtended(request.POST)
		if form.is_valid() and form_extended.is_valid():
			username = request.POST['username']
			password = request.POST['password1']
			email = request.POST['email']
			fullname = request.POST['fullname']
			phone = request.POST['phone']
			area = request.POST['area']
			rating = request.POST['rating']
			user = User.objects.create(username=username, password=password, email=email, user_type=2)
			agent = Agent.objects.create(fullname=fullname, phone=phone, area=area, rating=rating, user=user)
			return redirect('/')

	return render(request, 'registration/agent_signup_form.html', {'form':form, 'form_extended':form_extended})

@method_decorator([login_required, agent_required], name='dispatch')
class HomeView(ListView):
	template_name = 'userAuth/agents/home.html'