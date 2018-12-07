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
from userAuth.tokens import account_activation_token
from django.core.mail import EmailMessage

from userAuth.decorators import executive_required, agent_or_executive_required
from executives.forms import ExecutiveSignUpForm, ExecutiveDetailsForm
from agents.forms import AgentDetailsForm, AgentDeleteForm
from shop.forms import CategorySignUpForm, ProductSignUpForm, ProductDeleteForm, CategoryDeleteForm, ProductDetailsForm
from orders.forms import OrderCancelConfirmForm
from userAuth.models import User, AgentApplications
from executives.models import Executive
from agents.models import Agent
from orders.models import Order, OrderItem, PartyOrders
from shop.models import Product, Category

from chat.models import Room

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
	template_name = 'executives/home.html'

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
	template_name = 'executives/agents_list.html'

	def get_queryset(self):
		queryset = Agent.objects.all()
		return queryset

@method_decorator([login_required, executive_required], name='dispatch')
class AllOrdersView(ListView):
	model = Order
	ordering = ('updated', )
	context_object_name = 'orders'
	template_name = 'executives/all_orders.html'

	def get_queryset(self):
		queryset = Order.objects.all()
		return queryset

@method_decorator([login_required, executive_required], name='dispatch')
class OrderView(ListView):
	model = OrderItem
	ordering = ('id', )
	context_object_name = 'items'
	template_name = 'customers/items_list.html'

	def get_queryset(self):
		order = Order.objects.get(id=self.kwargs['oid'])
		queryset = OrderItem.objects.filter(order=order)
		return queryset

@method_decorator([login_required, executive_required], name='dispatch')
class PartyOrdersView(ListView):
	model = PartyOrders
	ordering = ('id', )
	context_object_name = 'orders'
	template_name = 'executives/partyOrders_list.html'

	def get_queryset(self):
		queryset = PartyOrders.objects.all()
		return queryset

@login_required
@agent_or_executive_required
def CancelOrderView(request, oid):
	try:
		order = Order.objects.get(id=oid)
	except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
		order = None
	if order:
		form = OrderCancelConfirmForm()
		if request.method == 'POST':
			form = OrderCancelConfirmForm(request.POST)
			if request.POST.get('check', False):
				form.save(order)
				return redirect('home')

		return render(request, 'registration/order_cancel.html', {'form':form, 'order':order})
	return redirect('forbidden')

@login_required
@agent_or_executive_required
def PartyOrderCancelView(request, oid):
	try:
		order = PartyOrders.objects.get(id=oid)
	except(TypeError, ValueError, OverflowError, PartyOrders.DoesNotExist):
		order = None
	if order:
		form = OrderCancelConfirmForm()
		if request.method == 'POST':
			form = OrderCancelConfirmForm(request.POST)
			if request.POST.get('check', False):
				order.delete()
				return redirect('executive:all_party_orders')

		return render(request, 'registration/order_cancel.html', {'form':form, 'order':order})
	return redirect('forbidden')

@method_decorator([login_required, executive_required], name='dispatch')
class CategoriesView(ListView):
	model = Category
	ordering = ('name', )
	context_object_name = 'cats'
	template_name = 'executives/cats_list.html'

	def get_queryset(self):
		queryset = Category.objects.all()
		return queryset

@method_decorator([login_required, executive_required], name='dispatch')
class ProductsView(ListView):
	model = Product
	ordering = ('name', )
	context_object_name = 'prds'
	template_name = 'executives/prds_list.html'

	def get_queryset(self):
		queryset = Product.objects.all()
		return queryset

@method_decorator([login_required, executive_required], name='dispatch')
class AgentApplicationsView(ListView):
	model = AgentApplications
	ordering = ('id', )
	context_object_name = 'appls'
	template_name = 'executives/appls_list.html'

	def get_queryset(self):
		queryset = AgentApplications.objects.all()
		return queryset

@login_required
@executive_required
def AcceptAgentApplication(request, aid):
	try:
		agent_appl = AgentApplications.objects.get(pk=aid)
	except:
		agent_appl = None
	if agent_appl:
		newAgent = User.objects.create(
			username='testagent001',
			password=User.objects.make_random_password(),
			email=agent_appl.email,
			user_type=2,
			is_active=False
		)
		newAgent.username = 'agent'+str(1000+newAgent.id)
		newAgent.save()
		newAgentDetails = Agent.objects.create(
			fullname=agent_appl.fullname,
			phone=agent_appl.phone,
			area=agent_appl.area,
			rating=0,
			user=newAgent,
		)
		agent_appl.delete()
		current_site = get_current_site(request)
		mail_subject = 'Welcome aboard, '+newAgentDetails.fullname+'!'
		message = render_to_string('email/agent_appl_accepted.html', {
			'user': newAgent,
			'domain': current_site.domain,
			'uid':urlsafe_base64_encode(force_bytes(newAgent.pk)).decode(),
			'token':account_activation_token.make_token(newAgent),
		})
		to_email = newAgent.email
		email = EmailMessage(
					mail_subject, message, to=[to_email]
		)
		email.send()
		return render(request, 'registration/newAgent.html')
	return render(request, '500.html')

@login_required
@executive_required
def RejectAgentApplication(request, aid):
	try:
		agent_appl = AgentApplications.objects.get(pk=aid)
	except:
		agent_appl = None
	if agent_appl:
		fullname = agent_appl.fullname
		to_email = agent_appl.email
		agent_appl.delete()
		current_site = get_current_site(request)
		mail_subject = "We're sorry, "+fullname+'.'
		message = render_to_string('email/agent_appl_rejected.html', {
			'name': fullname,
		})
		email = EmailMessage(
					mail_subject, message, to=[to_email]
		)
		email.send()
		return render(request, 'registration/rejectAgent.html')
	return render(request, '500.html')



@login_required 
@agent_or_executive_required
def AgentDetailsView(request, aid):
	try:
		agent = User.objects.get(pk=aid)
	except:
		agent = None
	if agent and (agent.id == request.user.id or request.user.user_type == 3):
		details = {}
		for field in Agent._meta.get_fields():
			details[field.name] = getattr(agent.agent, field.name)
		return render(request, "registration/details_view.html", {'details':details})
	return render(request, '500.html')


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

@method_decorator([login_required, executive_required], name='dispatch')
class SupportView(ListView):
	model = Room
	ordering = ('id', )
	context_object_name = 'reqs'
	template_name = 'executives/support_list.html'

	def get_queryset(self):
		queryset = Room.objects.filter(executive=None)
		return queryset

