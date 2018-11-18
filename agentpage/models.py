from django.db import models
from userpage.models import Order

# Create your models here.
class Employee(models.Model):
    agentid=models.CharField(max_length =50, null = False, blank = False,default = "a")
    #agentid=models.ForeignKey(AgentLog, on_delete=models.CASCADE)
    employeeid=models.CharField(primary_key=True,max_length =50)
    employeename=models.CharField(max_length =50, null = False, blank = False)
    employeephone=models.CharField(max_length =20, null = False, blank = False)
    employeeemail=models.CharField(max_length =50, null = False, blank = False)
    employeeaddress=models.CharField(max_length =500, null = False, blank = False)
    employeeaadhar=models.CharField(max_length =50,null = False, blank = False)

    def __str__(self):
        return '{}'.format(self.employeeid)


class DeliveredBy(models.Model):
    employeeid=models.CharField(max_length =50, null = False, blank = False)
    orderid=models.ForeignKey(Order,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    def __str__(self):
        return '{}'.format(self.employeeid)
