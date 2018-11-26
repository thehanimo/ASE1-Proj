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
from ..forms import ExecutiveSignUpForm, ExecutiveDetailsForm, AgentDetailsForm, AgentDeleteForm, CategorySignUpForm, ProductSignUpForm, ProductDeleteForm, CategoryDeleteForm, ProductDetailsForm
from ..models import User, Executive, Agent
from orders.models import Order
from shop.models import Product, Category

class ExecutiveSignUpView(CreateView):
	model = User
	form_class = ExecutiveSignUpForm
	template_name = 'registration/exec_signup_form.html'

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

@method_decorator([login_required, executive_required], name='dispatch')
class AgentsView(ListView):
	model = Agent
	ordering = ('fullname', )
	context_object_name = 'agents'
	template_name = 'userAuth/executives/agents_list.html'

	def get_queryset(self):
		queryset = Agent.objects.all()
		return queryset

@method_decorator([login_required, executive_required], name='dispatch')
class AllOrdersView(ListView):
	model = Order
	ordering = ('updated', )
	context_object_name = 'orders'
	template_name = 'userAuth/executives/all_orders.html'

	def get_queryset(self):
		queryset = Order.objects.all()
		return queryset

@method_decorator([login_required, executive_required], name='dispatch')
class CategoriesView(ListView):
	model = Category
	ordering = ('name', )
	context_object_name = 'cats'
	template_name = 'userAuth/executives/cats_list.html'

	def get_queryset(self):
		queryset = Category.objects.all()
		return queryset

@method_decorator([login_required, executive_required], name='dispatch')
class ProductsView(ListView):
	model = Product
	ordering = ('name', )
	context_object_name = 'prds'
	template_name = 'userAuth/executives/prds_list.html'

	def get_queryset(self):
		queryset = Product.objects.all()
		return queryset


@login_required
@executive_required
def AgentEditView(request, id):
	try:
		uid = int(id)
		agent_user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		agent_user = None
	if agent_user:
		form = AgentDetailsForm(initial={
			'fullname': agent_user.agent.fullname,
			'phone': agent_user.agent.phone,
			'area': agent_user.agent.area,
			'rating': agent_user.agent.rating,
			})
		if request.method == 'POST':
			form = AgentDetailsForm(request.POST)
			if request.POST['phone'] == agent_user.agent.phone:
				form.dummy_phone_save(agent_user, '')
			if form.is_valid():
				form.save(agent_user)
				return redirect('/')

		return render(request, 'registration/agent_edit.html', {'form':form})
	return redirect('forbidden')

@login_required
@executive_required
def AgentDeleteView(request, id):
	try:
		uid = int(id)
		agent_user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		agent_user = None
	if agent_user:
		form = AgentDeleteForm()
		if request.method == 'POST':
			form = AgentDeleteForm(request.POST)
			if request.POST.get('check', False):
				form.save(agent_user)
				return redirect('/')

		return render(request, 'registration/agent_edit.html', {'form':form, 'agent':agent_user})
	return redirect('forbidden')

@method_decorator([login_required, executive_required], name='dispatch')
class CategoryCreateView(CreateView):
	model = Category
	form_class = CategorySignUpForm
	template_name = 'registration/create.html'

	def form_valid(self,form):
		form.save()
		return redirect('/')

@method_decorator([login_required, executive_required], name='dispatch')
class ProductCreateView(CreateView):
	model = Product
	form_class = ProductSignUpForm
	template_name = 'registration/create.html'

	def form_valid(self,form):
		form.save()
		return redirect('/')

@login_required
@executive_required
def ProductDeleteView(request, id):
	try:
		pid = int(id)
		prd = Product.objects.get(pk=pid)
	except(TypeError, ValueError, OverflowError, Product.DoesNotExist):
		prd = None
	if prd:
		form = ProductDeleteForm()
		if request.method == 'POST':
			form = ProductDeleteForm(request.POST)
			if request.POST.get('check', False):
				form.save(prd)
				return redirect('/')

		return render(request, 'registration/order_confirm.html', {'form':form})
	return redirect('forbidden')

@login_required
@executive_required
def CategoryDeleteView(request, id):
	try:
		cid = int(id)
		cat = Category.objects.get(pk=cid)
	except(TypeError, ValueError, OverflowError, Category.DoesNotExist):
		cat = None
	if cat:
		form = CategoryDeleteForm()
		if request.method == 'POST':
			form = CategoryDeleteForm(request.POST)
			if request.POST.get('check', False):
				form.save(cat)
				return redirect('/')

		return render(request, 'registration/order_confirm.html', {'form':form})
	return redirect('forbidden')

@method_decorator([login_required, executive_required], name='dispatch')
class ProductDetailsView(UpdateView):
	model = Product
	template_name = "registration/obj_details.html"
	form_class = ProductDetailsForm

	def get_object(self):
		prd = Product.objects.get(id=self.kwargs['pid'])
		return prd

	def get_success_url(self, *args, **kwargs):
		return reverse("executive:product")
