from django.db import models
from shop.models import Product
from userAuth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

BILLING_TYPES = [
        ('1','COD'),
        ('2','ONLINE'),
        ('3','SUBSCRIPTION'),
    ]
ORDER_STATUSES = [
        ('0','FAILED'),
        ('X','CANCELLED'),
        ('W','CANCEL REQUESTED'),
        ('1','PLACED'),
        ('2','CONFIRMED'),
        ('3','OUT FOR DELIVERY'),
        ('4','DELIVERED'),
        ('P','PROCESSING'),
    ]

class Order(models.Model):
    customer = models.ForeignKey(User, related_name='order_customer', on_delete=models.CASCADE)
    agent = models.ForeignKey(User, related_name='order_agent', on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    rated = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=1, default='1', choices=BILLING_TYPES)
    order_status = models.CharField(max_length=1, default='1', choices=ORDER_STATUSES)
    preferred_time = models.CharField(max_length=20,blank=True)
    

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

class Tracking(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    enabled = models.BooleanField(default=False)
    longitude = models.CharField(max_length=20, blank=True)
    latitude = models.CharField(max_length=20, blank=True)
    
    def get_coords(self):
        return [float(self.longitude), float(self.latitude)]

class PartyOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_cans = models.IntegerField(blank=False,validators=[MinValueValidator(30), MaxValueValidator(300)])
    comments = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):
    customer = models.ForeignKey(User, related_name='subscription', on_delete=models.CASCADE)
    subscription = models.CharField(max_length=30)
    number_of_cans = models.IntegerField(blank=True)
    subscribed = models.DateTimeField(auto_now_add=True)

    def get_days_remaining(self):
        return (30 - (timezone.now() - self.subscribed).days)

class Subscriptions(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_cans = models.IntegerField()

    def get_all_subs():
        subs = Subscriptions.objects.all()
        names = []
        for sub in subs:
            names.append((str(sub.id),str(sub.name)+' - '+str(sub.description)+' @ ₹'+str(sub.price)))
        return names




