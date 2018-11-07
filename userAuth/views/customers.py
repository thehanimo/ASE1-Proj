from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, FormView

from ..decorators import customer_required, customer_details_required, customer_details_empty
from ..forms import CustomerSignUpForm, CustomerDetailsForm
from ..models import User, Customer

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 1
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customer:home')

@method_decorator([login_required, customer_required, customer_details_empty], name='dispatch')
class NewCustomerDetailsView(FormView):
    template_name = "registration/details.html"
    form_class = CustomerDetailsForm

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

    def get_success_url(self, *args, **kwargs):
        return reverse("customer:home")

@method_decorator([login_required, customer_required], name='dispatch')
class HomeView(ListView):
    template_name = 'userAuth/customers/home.html'
    
    def get_queryset(self):
        return []