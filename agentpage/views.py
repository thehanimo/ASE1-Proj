from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponse
from userpage.models import Item,Order,Notification,OrderItem
from .models import Employee,DeliveredBy
import copy,random

# Create your views here.

def onload_everypage(request):
    request.session['agentid']='a'
    return Order.objects.filter(orderstatus="Order Placed").filter(agentid=request.session['agentid']).count()


def addemployee(request):
    todo_count=onload_everypage(request)
    if request.POST:
        employeename=request.POST['employeename']
        employeephone=request.POST['phone']
        employeeaddress=request.POST['address']
        employeeemail=request.POST['email']
        employeeaadhar=request.POST['aadhar']
        employee_aadhar_list=Employee.objects.filter(agentid=request.session['agentid']).values('employeeaadhar',)
        employee_id_list=Employee.objects.filter(agentid=request.session['agentid']).values('employeeid',)
        employee_id_list=list(employee_id_list)
        employee_aadhar_list=list(employee_aadhar_list)
        employee_id_list_temp=list()
        for e in employee_id_list:
            employee_id_list_temp.append(e['employeeid'])
        employee_aadhar_list_temp=list()
        for e in employee_aadhar_list:
            employee_aadhar_list_temp.append(e['employeeaadhar'])
        if(employeeaadhar not in employee_aadhar_list_temp):
            while(1):
                employeeid=employeename
                for i in range(0,20):
                    employeeid = employeeid + str(random.randint(0,9))

                if(employeeid not in employee_id_list_temp):
                    e=Employee.objects.create(employeeid=employeeid,employeename=employeename,employeephone=employeephone,agentid=request.session['agentid'],employeeemail=employeeemail,employeeaddress=employeeaddress,employeeaadhar=employeeaadhar)
                    break
    return render(request,'agentpage/addemployee.html', context={'todo_count':todo_count,})

def agentpage(request):
    todo_count=onload_everypage(request)
    request.session['agentid'] = 'a'
    return render(request,'agentpage/agentpage.html', context={'todo_count':todo_count,})


def todo(request):
    todo_count=onload_everypage(request)
    employee_list=Employee.objects.filter(agentid=request.session['agentid'])
    order_todo_list=Order.objects.filter(orderstatus="Order Placed").filter(agentid=request.session['agentid'])
    order_todo_list_copy=copy.deepcopy(order_todo_list)
    if "Assign Work" in request.POST:
        if not DeliveredBy.objects.filter(orderid=request.POST['orderid']):
            o=Order.objects.filter(orderid=request.POST["orderid"])
            for obj in o:
                DeliveredBy.objects.create(orderid=obj,employeeid=request.POST["Assign Work"])
            Order.objects.filter(orderid=request.POST["orderid"]).update(orderstatus="out to deliver")
            ordderitems=OrderItem.objects.filter(orderid=request.POST["orderid"])
            s=""
            for oi in ordderitems:
                s= s + str(oi.itemname) + '(' + str(oi.quantity) +')' +' ,'
            for o in Order.objects.filter(orderid=request.POST["orderid"]):
                Notification.objects.create(userid=o.userid,notifiedfrom="AGENT-"+ request.session['agentid'],message="Your Order - ORDERID:"+str(o.orderid) + " : " + s + "- is out to delivery")
            todo_count=onload_everypage(request)
            print('worked assigned')
        else:
            print('alderady assigned')

        todo_count=onload_everypage(request)
    return render(request,'agentpage/todo.html', context={'order_todo_list':order_todo_list_copy,'todo_count':todo_count,'employee_list':employee_list})


def delivering(request):
    todo_count=onload_everypage(request)
    if "Deliver Later" in request.POST:
        Order.objects.filter(orderid=request.POST["Deliver Later"]).update(orderstatus="Order Placed")
        DeliveredBy.objects.filter(orderid=request.POST['Deliver Later']).delete()
        ordderitems=OrderItem.objects.filter(orderid=request.POST["Deliver Later"])
        s=""
        for oi in ordderitems:
            s= s + str(oi.itemname) + '(' + str(oi.quantity) +')' +' ,'

        for o in Order.objects.filter(orderid=request.POST['Deliver Later']):
            Notification.objects.create(userid=o.userid,notifiedfrom="AGENT-"+ request.session['agentid'], message="Your Order - ORDERID:"+str(o.orderid) + "-"+ s +" can't be delivered for now.\nSorry for the delay.\nWe will makesure that our service will come to you soon .. ")

    order_delivering_list=Order.objects.filter(orderstatus="out to deliver").filter(agentid=request.session['agentid'])
    order_delivering_list_copy=copy.deepcopy(order_delivering_list)
    return render(request,'agentpage/delivering.html', context={'order_delivering_list':order_delivering_list_copy,'todo_count':todo_count,})


def delivered(request):
    todo_count=onload_everypage(request)
    order_delivered_list=Order.objects.filter(orderstatus="delivered").filter(agentid=request.session['agentid'])
    order_delivered_list_copy=copy.deepcopy(order_delivered_list)
    return render(request,'agentpage/delivered.html', context={'order_delivered_list':order_delivered_list_copy,'todo_count':todo_count,})



def employee(request):
    todo_count=onload_everypage(request)
    return render(request,'agentpage/employee.html', context={})


def employeework(request):
    todo_count=onload_everypage(request)
    if 'employeeid' in request.POST:
        work = DeliveredBy.objects.filter(employeeid=request.POST['employeeid']).filter(status=False)
        request.session['employeeid']=request.POST['employeeid']
        return render(request,'agentpage/employeework.html', context={'todo_count':todo_count,'work':work,})
    elif 'order delivered' in request.POST:
        DeliveredBy.objects.filter(orderid=request.POST['order delivered']).update(status=True)
        Order.objects.filter(orderid=request.POST['order delivered']).update(orderstatus="delivered")
        for o in Order.objects.filter(orderid=request.POST['order delivered']):
            Notification.objects.create(userid=o.userid,notifiedfrom="Admin - ",message="Your Order - ORDERID:"+str(o.orderid) + "- is been delivered successfully......\nThanks for using our services ! \nAny isuues ? Please contact us.")

        work = DeliveredBy.objects.filter(employeeid=request.session['employeeid']).filter(status=False)
        return render(request,'agentpage/employeework.html', context={'todo_count':todo_count,'work':work,})

    else:
        return employee(request)
