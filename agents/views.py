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


from userAuth.decorators import agent_required, executive_required, agent_or_executive_required
from userAuth.forms import NewPasswordForm
from orders.forms import OrderAcceptForm, OrderCancelConfirmForm, OrderOutForDeliveryForm, OrderDeliveredForm
from userAuth.models import User
from .models import Agent
from orders.models import Order, OrderItem

from executives.models import AgentNotification
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from userAuth.tokens import account_activation_token
from django.core.mail import EmailMessage

@login_required
@agent_required
def HomeView(request):
	inc_orders = len(Order.objects.filter(agent=request.user, order_status='W')) + len(Order.objects.filter(agent=request.user, order_status='1'))
	ass_orders = len(Order.objects.filter(agent=request.user, order_status='2')) + len(Order.objects.filter(agent=request.user, order_status='3'))
	del_orders = len(Order.objects.filter(agent=request.user, order_status='4'))
	can_orders = len(Order.objects.filter(agent=request.user, order_status='X'))
	return render(request, "agents/home.html", {'inc_orders':inc_orders,'ass_orders':ass_orders,'del_orders':del_orders, 'can_orders':can_orders,})



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


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.email_verified = True
		user.is_active = True
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

@method_decorator([login_required, agent_required], name='dispatch')
class OrderView(ListView):
	model = OrderItem
	ordering = ('id', )
	context_object_name = 'items'
	template_name = 'customers/items_list.html'

	def get_queryset(self):
		order = Order.objects.get(id=self.kwargs['oid'])
		cur_user = self.request.user
		if cur_user.id != order.agent.id:
			return []
		queryset = OrderItem.objects.filter(order=order)
		return queryset

@method_decorator([login_required, agent_required], name='dispatch')
class IncomingOrdersView(ListView):
	model = Order
	ordering = ('created', )
	context_object_name = 'orders'
	template_name = 'agents/inc_orders_list.html'

	def get_queryset(self):
		queryset = Order.objects.filter(agent=self.request.user, order_status='W') | Order.objects.filter(agent=self.request.user, order_status='1')
		return queryset

@method_decorator([login_required, agent_required], name='dispatch')
class AssignedOrdersView(ListView):
	model = Order
	ordering = ('created', )
	context_object_name = 'orders'
	template_name = 'agents/ass_orders_list.html'

	def get_queryset(self):
		queryset = Order.objects.filter(agent=self.request.user, order_status='2') | Order.objects.filter(agent=self.request.user, order_status='3')
		return queryset

@method_decorator([login_required, agent_required], name='dispatch')
class CompletedOrdersView(ListView):
	model = Order
	ordering = ('created', )
	context_object_name = 'orders'
	template_name = 'agents/compl_orders_list.html'

	def get_queryset(self):
		queryset = Order.objects.filter(agent=self.request.user, order_status='4')
		return queryset

@method_decorator([login_required, agent_required], name='dispatch')
class CancelledOrdersView(ListView):
	model = Order
	ordering = ('created', )
	context_object_name = 'orders'
	template_name = 'agents/canc_orders_list.html'

	def get_queryset(self):
		queryset = Order.objects.filter(agent=self.request.user, order_status='X')
		return queryset

@login_required
@agent_required
def AcceptOrderView(request, oid):
	try:
		order = Order.objects.get(id=oid)
	except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
		order = None
	if order:
		form = OrderAcceptForm()
		if request.method == 'POST':
			form = OrderAcceptForm(request.POST)
			if request.POST.get('check', False):
				form.save(order)
				return redirect('agent:incomingorders')

		return render(request, 'registration/order_accept.html', {'form':form, 'order':order})
	return redirect('forbidden')

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
@agent_required
def OutForDeliveryOrderView(request, oid):
	try:
		order = Order.objects.get(id=oid)
	except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
		order = None
	if order:
		form = OrderOutForDeliveryForm()
		if request.method == 'POST':
			form = OrderOutForDeliveryForm(request.POST)
			if request.POST.get('check', False):
				form.save(order)
				return redirect('agent:assignedorders')

		return render(request, 'registration/order_confirm.html', {'form':form, 'order':order})
	return redirect('forbidden')


@login_required
@agent_required
def DeliveredOrderView(request, oid):
	try:
		order = Order.objects.get(id=oid)
	except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
		order = None
	if order:
		form = OrderDeliveredForm()
		if request.method == 'POST':
			form = OrderDeliveredForm(request.POST)
			if request.POST.get('check', False):
				form.save(order)
				return redirect('agent:assignedorders')

		return render(request, 'registration/order_confirm.html', {'form':form, 'order':order})
	return redirect('forbidden')

@method_decorator([login_required, agent_required], name='dispatch')
class NotificationsView(ListView):
	model = AgentNotification
	context_object_name = 'notifs'
	template_name = 'agents/notifs.html'

	def get_queryset(self):
		queryset = AgentNotification.objects.filter(agent=self.request.user)
		for notif in queryset:
			notif.notified = True
			notif.save()
		return queryset.order_by('-created')
