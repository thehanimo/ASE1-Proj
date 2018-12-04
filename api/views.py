import copy, json, datetime
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.shortcuts import render

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
	except(TypeError, ValueError, OverflowError, Order.DoesNotExist, Tracking.DoesNotExist):
		return JsonResponse({'longitude': '', 'latitude':'', 'enabled':'False'})
	return JsonResponse({'longitude': tracking.longitude, 'latitude':tracking.latitude, 'enabled':'True'})