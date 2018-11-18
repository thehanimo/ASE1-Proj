from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .models import Notification,Item,Order,OrderItem
import copy
# Create your views here.
def onload_everypage(request):
    request.session['userid'] = '1'  ## TEMP
    unseen_notifications_count=Notification.objects.filter(seen=False).filter(userid=request.session['userid']).count()
    return unseen_notifications_count
    #return {'unseen_notifications_count':unseen_notifications_count,}

def userpage(request):
    onload=onload_everypage(request)
    request.session['agentid'] = 'a'  ## TEMP
    try:
        Items_list=Item.objects.all()
        Items_dict={'Items_list':Items_list,'unseen_notifications_count':onload,}
        return render(request,'userpage/user.html',context=Items_dict)

    except KeyError:
        return HttpResponse('OOPS !\nsSomething went wrong in server .....')
    except Exception:
        return HttpResponse('Some Thing Went Wrong !\nPlease Consult Admin....')


def checkout(request):
    onload_dict=onload_everypage(request)
    #t_list=copy.deepcopy(Items_list)
    try:
        Items_required=[0,]
        Items_list=Item.objects.all()
        Items_required.append(int(request.POST['cans']))
        Items_required.append(int(request.POST['bottles']))
        Items_required.append(int(request.POST['tissues']))
        request.session['no_cans']=int(request.POST['cans'])
        request.session['no_bottles']=int(request.POST['bottles'])
        request.session['no_tissues']=int(request.POST['tissues'])
        total=0
        c=1
        t_list=[0,]
        for i in Items_list:
            total=total+(i.itemcost * int(Items_required[c]))
            t_list.append(i.itemcost * int(Items_required[c]))
            c=c+1
        if total==0:
            Items_list=Item.objects.all()
            Items_dict={'Items_list':Items_list,}
            return userpage(request)
        else:
            request.session['total'] = total
            print(Items_required,t_list,total)
            return render(request,'userpage/checkout.html', context={'Items_list':Items_list,'Items_required':Items_required,'t_list':t_list,'total':total})
    except KeyError:
        return HttpResponse('Please Select Quantity First !')
#    except Exception:
#        return HttpResponse('Some Thing Went Wrong !\nPlease Consult Admin....')



def orderplaced(request):
        onload_dict=onload_everypage(request)
#    try:
        billingaddress= request.POST['firstname'] + ',' + request.POST['email'] + ',' + request.POST['pno'] + ',' + request.POST['address'] + ',' + request.POST['city'] + ',' + request.POST['state']  + ',' + request.POST['pin']
        billingamount= request.session['total']
        billingtype= "COD"
        orderplaced= True
        orderstatus= "Order Placed"

        subject = 'Thank For Using Our Service !'
        message = 'It means a world to us \nYour order is been placed and will be delivered as soon as possible\nAny aurgs ? contact us through email'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['email'],]
        #send_mail( subject, message, email_from, recipient_list )

        notifiedfrom='Admin'
        Notification_message="Thanks for using our service !\nYour order is been placed and will be delivered as soon as possible...."
        Notification.objects.create(notifiedfrom=notifiedfrom,message=Notification_message,userid=request.session['userid'])

        request.session.modified = True
        del request.session['total']

        order = Order.objects.create(billingaddress=billingaddress,billingamount=billingamount,billingtype=billingtype,orderplaced=orderplaced,orderstatus=orderstatus)
        if int(request.session['no_cans']):
            OrderItem.objects.create(orderid=order,itemname="can",quantity=int(request.session['no_cans']))
        if int(request.session['no_bottles']):
            OrderItem.objects.create(orderid=order,itemname="bottle",quantity=int(request.session['no_bottles']))
        if int(request.session['no_tissues']):
            OrderItem.objects.create(orderid=order,itemname="tissue",quantity=int(request.session['no_tissues']))
        return render(request,'userpage/orderplaced.html', context={'order':order,})

    #except KeyError:
    #    return HttpResponse('Please dont skip the checkout verification !')
    #except Exception:
    #    return HttpResponse('Some Thing Went Wrong !\nPlease Consult Admin....')

def yourorders(request):
    return HttpResponse("To Be finished")


def notifications(request):
    onload_dict=onload_everypage(request)
    Notifications_list_unseen=Notification.objects.filter(seen=False).filter(userid=request.session['userid'])
    Notifications_list_seen=Notification.objects.filter(seen=True).filter(userid=request.session['userid'])
    Notifications_list_unseen_copy=copy.deepcopy(reversed(Notifications_list_unseen))
    Notifications_list_seen_copy=copy.deepcopy(reversed(Notifications_list_seen))
    Notifications_list_unseen.update(seen=True)
    return render(request,'userpage/notifications.html',context={'Notifications_list_unseen':Notifications_list_unseen_copy,'Notifications_list_seen':Notifications_list_seen_copy,})
