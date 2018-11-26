from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from orders.models import Order
from userAuth.models import Agent, Customer, Executive, User
from shop.models import Product, Category




class AgentSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 2
        if commit:
            user.save()
        return user

class AgentSignUpFormExtended(forms.ModelForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = Agent
        fields = ('email', 'fullname', 'phone', 'area', 'rating')

class AgentDetailsForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ('fullname', 'phone', 'area', 'rating')

    def save(self, user=None):
        agent_details = super(AgentDetailsForm, self).save(commit=False)
        if user:
            agent_details.user = user
        agent_details.save()
        return agent_details

    def dummy_phone_save(self, user, phone):
        agent = Agent.objects.get(user=user)
        agent.phone = phone 
        agent.save()

class AgentDeleteForm(forms.ModelForm):
    check = forms.BooleanField()
    class Meta:
        model = Agent
        fields = ('check',)

    def save(self, user=None):
        agent = Agent.objects.get(user=user)
        agent.delete()
        user.delete()
        return

class ProductDeleteForm(forms.ModelForm):
    check = forms.BooleanField()
    class Meta:
        model = Product
        fields = ('check',)

    def save(self, in_prd=None):
        prd = Product.objects.get(id=in_prd.id)
        prd.delete()
        return

class CategoryDeleteForm(forms.ModelForm):
    check = forms.BooleanField()
    class Meta:
        model = Category
        fields = ('check',)

    def save(self, in_cat=None):
        cat = Category.objects.get(id=in_cat.id)
        cat.delete()
        return

class OrderCancelForm(forms.ModelForm):
    check = forms.BooleanField()
    class Meta:
        model = Order
        fields = ('check',)

    def save(self, order=None):
        order = Order.objects.get(id=order.id)
        order.order_status = 'W'
        order.save()
        return

class OrderCancelConfirmForm(forms.ModelForm):
    check = forms.BooleanField()
    class Meta:
        model = Order
        fields = ('check',)

    def save(self, order=None):
        order = Order.objects.get(id=order.id)
        order.order_status = 'X'
        order.save()
        return

class OrderAcceptForm(forms.ModelForm):
    check = forms.BooleanField()
    class Meta:
        model = Order
        fields = ('check',)

    def save(self, order=None):
        order = Order.objects.get(id=order.id)
        order.order_status = '2'
        order.save()
        return

class OrderOutForDeliveryForm(forms.ModelForm):
    check = forms.BooleanField()
    class Meta:
        model = Order
        fields = ('check',)

    def save(self, order=None):
        order = Order.objects.get(id=order.id)
        order.order_status = '3'
        order.save()
        return

class OrderDeliveredForm(forms.ModelForm):
    check = forms.BooleanField()
    class Meta:
        model = Order
        fields = ('check',)

    def save(self, order=None):
        order = Order.objects.get(id=order.id)
        order.order_status = '4'
        order.save()
        return

class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 1
        if commit:
            user.save()
        return user

class CategorySignUpForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name','slug')

    def save(self):
        cat = Category.objects.create(slug=self.cleaned_data['slug'], name=self.cleaned_data['name'])
        cat.save()

class ProductSignUpForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category','name','slug','description','price','available','stock','image')

    def save(self):
        prod = Product.objects.create(
            category=self.cleaned_data['category'],
            slug=self.cleaned_data['slug'],
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            price=self.cleaned_data['price'],
            available=self.cleaned_data['available'],
            stock=self.cleaned_data['stock'],
            image=self.cleaned_data['image'],
            )
        a=prod.reduce_stock(0)
        prod.save()

class ExecutiveSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 3
        if commit:
            user.save()
        return user

class CustomerDetailsForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('fullname', 'photo', 'phone', 'street', 'area')

    def save(self, user=None):
        customer_details = super(CustomerDetailsForm, self).save(commit=False)
        if user:
            customer_details.user = user
        customer_details.save()
        return customer_details

class ExecutiveDetailsForm(forms.ModelForm):
    class Meta:
        model = Executive
        fields = ('photo',)

    def save(self, user=None):
        executive_details = super(ExecutiveDetailsForm, self).save(commit=False)
        if user:
            executive_details.user = user
        executive_details.save()
        return executive_details

class ProductDetailsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category','name','slug','description','price','available','stock','image')

    def save(self, user=None):
        product_details = super(ProductDetailsForm, self).save(commit=False)
        product_details.save()
        return product_details

class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class NewPasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('password1', 'password2')

    def save(self, user=None):
        if user:
            user.set_password(self.cleaned_data['password1'])
        user.save()
        return user
