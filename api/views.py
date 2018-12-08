import copy, json, datetime
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.shortcuts import render
from executives.models import AgentNotification
from userAuth.models import User

from orders.models import Order, Tracking
# Create your views here.
@csrf_exempt
@require_POST
def inp(request, oid):
	try:
		order = Order.objects.get(id=oid)
	except(TypeError, ValueError, OverflowError, Order.DoesNotExist):
		return JsonResponse({'result': 'notok'})
	tracking,created = Tracking.objects.get_or_create(
		order=order,
		)
	jsondata = request.body
	data = json.loads(jsondata)
	meta = copy.copy(request.META)
	coords = data['locations'][0]['geometry']['coordinates']
	tracking.longitude = coords[0]
	tracking.latitude = coords[1]
	tracking.save()
	return JsonResponse({'result': 'ok'})

def out(request, oid):
	try:
		order = Order.objects.get(id=oid)
		tracking = Tracking.objects.get(order=order)
		if tracking.enabled == False or tracking.longitude == '' or tracking.latitude == '':
			raise Tracking.DoesNotExist
	except(TypeError, ValueError, OverflowError, Order.DoesNotExist, Tracking.DoesNotExist):
		return JsonResponse({'longitude': '', 'latitude':'', 'enabled':'False'})
	return JsonResponse({'longitude': tracking.longitude, 'latitude':tracking.latitude, 'enabled':'True'})

@csrf_exempt
@require_POST
def poll(request):
	jsondata = request.body
	data = json.loads(jsondata)
	meta = copy.copy(request.META)
	page = data["page"]
	user_id = data['user_id']
	try:
		user=User.objects.get(id=user_id)
	except User.DoesNotExist:
		user=None
	if user.user_type == 2:
		if page == 'home':
			notifs = AgentNotification.objects.filter(notified=False)
			if len(notifs) != 0:
				return JsonResponse({'reload':'true', 'type':'notifs'})
			incOrders = Order.objects.filter(agent=user, order_status='W') | Order.objects.filter(agent=user, order_status='1')
			if len(incOrders) != 0:
				return JsonResponse({'reload':'true', 'type':'incOrders'})
	return JsonResponse({'reload': 'false'})