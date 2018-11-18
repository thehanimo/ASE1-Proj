from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from .models import Notification,Item,Order
import copy
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
