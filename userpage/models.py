from django.db import models

# Create your models here.
class Notification(models.Model):
    userid=models.CharField(max_length =50, null = False, blank = False,default = "1")
    #userid=models.ForeignKey(UserLog, on_delete=models.CASCADE)
    notifiedfrom=models.CharField(max_length =50, null = False, blank = False)
    message=models.CharField(max_length =500, null = False, blank = False)
    seen=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True,editable=False)

    class Meta:
        get_latest_by = 'date'

class Item(models.Model):
    itemid=models.PositiveIntegerField(default=0,primary_key=True)
    itemname=models.CharField(max_length =50, null = False, blank = False)
    itemcost=models.PositiveIntegerField(default=0,null= False ,blank = False)


class Order(models.Model):
    orderid=models.AutoField(primary_key=True)
    userid=models.CharField(max_length =50, null = False, blank = False,default = "1")
    agentid=models.CharField(max_length =50, null = False, blank = False,default = "a")
    #userid=models.ForeignKey(UserLog, on_delete=models.CASCADE)
    #agentid=models.ForeignKey(AgentLog, on_delete=models.CASCADE)
    billingaddress=models.CharField(max_length =200, null = False, blank = False)
    billingdate=models.DateTimeField(auto_now_add=True,editable=False)
    billingamount=models.PositiveIntegerField(default=0)
    billingtype=models.CharField(max_length =50, null = False, blank = False)
    orderplaced=models.BooleanField(default=False)
    orderstatus=models.CharField(max_length =50, null = False, blank = False)

    def __str__(self):
        return '{}'.format(self.orderid)


class OrderItem(models.Model):
    orderid=models.ForeignKey(Order, on_delete=models.CASCADE)
    itemname=models.CharField(max_length =50, null = False, blank = False)
    quantity=models.PositiveIntegerField(default=0)
