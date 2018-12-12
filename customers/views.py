from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, FormView

from userAuth.decorators import anonymous_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from userAuth.tokens import account_activation_token
from django.core.mail import EmailMessage

from userAuth.decorators import customer_required, customer_details_required, customer_details_empty, customer_or_executive_required
from customers.forms import CustomerSignUpForm, CustomerDetailsForm, SubscriptionForm, AgentRateForm
from orders.forms import OrderCancelForm, PartyOrderCreateForm
from orders.models import Subscription, Subscriptions
from userAuth.models import User
from customers.models import Customer

from cart.cart import Cart
from orders.models import Order, OrderItem
from chat.models import Room
from agents.models import Agent
from shop.models import Product, Category
from haikunator import Haikunator
haikunator = Haikunator()

@method_decorator([anonymous_required], name='dispatch')
class CustomerSignUpView(CreateView):
	model = User
	form_class = CustomerSignUpForm
	template_name = 'registration/signup_form.html'

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 1
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save(commit=False)
		user.is_active = False
		user.save()
		current_site = get_current_site(self.request)
		mail_subject = 'Activate your account.'
		message = render_to_string('registration/acc_active_email.html', {
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

@method_decorator([login_required, customer_required, customer_details_empty], name='dispatch')
class NewCustomerDetailsView(FormView):
	template_name = "registration/details.html"
	form_class = CustomerDetailsForm

	def get_context_data(self, **kwargs):
		context=super(NewCustomerDetailsView, self).get_context_data(**kwargs)
		context['cart'] = Cart(self.request)
		return context

	def form_valid(self, form):
		form.save(self.request.user)
		return super(NewCustomerDetailsView, self).form_valid(form)

	def get_success_url(self, *args, **kwargs):
		return reverse("customer:home")

@method_decorator([login_required, customer_required, customer_details_required], name='dispatch')
class CustomerDetailsView(UpdateView):
	model = Customer
	template_name = "registration/details.html"
	form_class = CustomerDetailsForm

	def get_object(self, *args, **kwargs):
		user = self.request.user
		return user.customer

	def get_context_data(self, **kwargs):
		context = super(CustomerDetailsView, self).get_context_data(**kwargs)
		context.update({'user':self.request.user})
		context['cart'] = Cart(self.request)
		return context

	def get_success_url(self, *args, **kwargs):
		return reverse("customer:home")

@login_required
@customer_required
def HomeView(request):
	cart = Cart(request)
	categories = Category.objects.all()
	return render(request, 'customers/home.html',{'cart':cart, 'categories':categories})

def activate(request, uidb64, token):
	cart = Cart(request)
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.email_verified = True
		user.save()
		login(request, user)
		return render(request, 'registration/activation_suc.html',{'cart':cart,})
	else:
		return render(request, 'registration/activation_err.html',{'cart':cart,})

@method_decorator([login_required, customer_required], name='dispatch')
class MyOrdersView(ListView):
	model = Order
	ordering = ('created', )
	context_object_name = 'orders'
	template_name = 'customers/orders_list.html'

	def get_context_data(self, **kwargs):
		context = super(MyOrdersView, self).get_context_data(**kwargs)
		context['cart'] = Cart(self.request)
		return context

	def get_queryset(self):
		queryset = Order.objects.filter(customer=self.request.user)
		return queryset

@method_decorator([login_required, customer_required], name='dispatch')
class OrderView(ListView):
	model = OrderItem
	ordering = ('id', )
	context_object_name = 'items'
	template_name = 'customers/items_list.html'

	def get_context_data(self, **kwargs):
		context = super(OrderView, self).get_context_data(**kwargs)
		context['cart'] = Cart(self.request)
		return context

	def get_queryset(self):
		order = Order.objects.get(id=self.kwargs['oid'])
		cur_user = self.request.user
		if cur_user.id != order.customer.id:
			return []
		queryset = OrderItem.objects.filter(order=order)
		return queryset

@login_required
@customer_required
def CancelOrderView(request, oid):
	cart = Cart(request)
	try:
		order = Order.objects.get(id=oid)
	except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
		order = None
	if order:
		form = OrderCancelForm()
		if request.method == 'POST':
			form = OrderCancelForm(request.POST)
			if request.POST.get('check', False):
				form.save(order)
				return redirect('customer:myorders')

		return render(request, 'registration/order_cancel.html', {'cart':cart,'form':form, 'order':order})
	return redirect('forbidden')

def genRoom():
	label = haikunator.haikunate()
	room,created = Room.objects.get_or_create(
		label=label,
		)
	return room

@login_required
@customer_required
def support(request):
	cart = Cart(request)
	if request.method == 'POST':
		customer = request.user
		room = genRoom()
		room.customer = customer
		room.save()
		return redirect('chat:room', room_name=room.label)
	return render(request, 'customers/support.html',{'cart':cart,})

@login_required
@customer_required
def orderTrack(request):
	cart = Cart(request)
	if request.method == 'POST':
		try:
			order = Order.objects.get(id=request.POST['oid'])
		except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
			order = None
		if order and order.customer == request.user:
			return render(request, 'customers/track.html', {'order':order},{'cart':cart,})
		return redirect('forbidden')
	return render('500.html')

@method_decorator([login_required, customer_required], name='dispatch')
class PartyOrderCreateView(FormView):
	template_name = "orders/partyOrder.html"
	form_class = PartyOrderCreateForm
	
	def get_context_data(self, **kwargs):
		context = super(PartyOrderCreateView, self).get_context_data(**kwargs)
		context['cart'] = Cart(self.request)
		return context

	def form_valid(self, form):
		form.save(self.request.user)
		cart = Cart(self.request)
		return render(self.request,'orders/newPartyOrder.html',{'cart':cart,})

@login_required
@customer_required
@customer_details_required
def SubscriptionsView(request):
	try:
		cat = Category.objects.get(name='Subscriptions')
	except:
		return redirect('shop:product_list')
	return redirect('shop:product_list_by_category',category_slug=cat.slug)
	

@method_decorator([login_required, customer_required], name='dispatch')
class MySubscriptionsView(ListView):
	model = Subscription
	ordering = ('id', )
	context_object_name = 'subs'
	template_name = 'customers/subs_list.html'

	def get_queryset(self):
		queryset = Subscription.objects.filter(customer=self.request.user)
		return queryset

def SubscriptionClaimView(request, id):
	cart = Cart(request)
	sub = Subscription.objects.get(id=id)
	try:
		agent = Agent.objects.get(area=request.user.customer.area)
		if agent.user.is_active == False:
			raise Agent.DoesNotExist
	except Agent.DoesNotExist:
		return render(request, 'orders/order/NoDelivery.html', {'cart':cart,'area':request.user.customer.area})
	order = Order.objects.create(customer=request.user, agent=agent.user, payment_type='3', preferred_time='ASAP')
	cat,created = Category.objects.get_or_create(
		name="Subscriptions",
		slug="subscriptions",
		)
	can,created = Product.objects.get_or_create(
		category=cat,
		name='Subscribed Water Can',
		price=0,
		available=False,
		stock=0,
		)
	OrderItem.objects.create(
		order=order,
		product=can,
		price=0,
		quantity=request.POST.get('number_of_cans'),
	)
	oid = order.id
	sub.number_of_cans -= int(request.POST.get('number_of_cans'))
	sub.save()
	oid = urlsafe_base64_encode(force_bytes(order.id)).decode()
	return HttpResponseRedirect('/orders/placed/'+str(oid))

@login_required
@customer_required
def AgentRateView(request, oid):
	cart = Cart(request)
	try:
		order = Order.objects.get(id=oid)
		agent = order.agent.agent
	except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
		agent = None
	if agent and order.rated == False:
		form = AgentRateForm()
		if request.method == 'POST':
			form = AgentRateForm(request.POST)
			if form.is_valid():
				agent.no_of_ratings += 1
				agent.rating = (agent.rating + float(request.POST.get('rating')))/agent.no_of_ratings
				order.rated = True
				order.save()
				agent.save()
				return redirect('customer:myorders')
		return render(request, 'registration/order_rate.html', {'cart':cart,'form':form, 'order':order})
	return redirect('forbidden')










