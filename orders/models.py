from django.db import models
from shop.models import Product
from userAuth.models import User

BILLING_TYPES = [
        ('1','COD'),
        ('2','ONLINE'),
    ]
ORDER_STATUSES = [
        ('0','FAILED'),
        ('X','CANCELLED'),
        ('W','CANCEL REQUESTED'),
        ('1','PLACED'),
        ('2','CONFIRMED'),
        ('3','OUT FOR DELIVERY'),
        ('4','DELIVERED')
    ]
class Order(models.Model):
    customer = models.ForeignKey(User, related_name='order_customer', on_delete=models.CASCADE)
    agent = models.ForeignKey(User, related_name='order_agent', on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=1, default='1', choices=BILLING_TYPES)
    order_status = models.CharField(max_length=1, default='1', choices=ORDER_STATUSES)
    

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

