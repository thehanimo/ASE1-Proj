from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
def result(request):
    order_id= request.POST["oid"]
    user_id= request.POST["yid"]
    dealer_id=request.POST["did"]
    order_address=request.POST["address"]
    order_bottles=request.POST["q1"]
    order_tissues=request.POST["q2"]
    order_amount = request.POST["cost1"]
    

    orderlog = OrderHistory.objects.create(order_id=order_id,user_id=user_id,dealer_id=dealer_id,order_address=order_address
    ,order_bottles=order_bottles,order_tissues=order_tissues,order_amount=order_amount)
     return HttpResponse("created success fully")

def orderhistory(request):
    query_result = OrderHistory.objects.all()
    context = {
            'query_result': query_result
        }
    return render(request, 'watercan/orderhistory.html', context=context)


