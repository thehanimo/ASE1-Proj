import copy, json, datetime
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.shortcuts import render

# Create your views here.
@csrf_exempt
@require_POST
def inp(request):
	jsondata = request.body
	data = json.loads(jsondata)
	meta = copy.copy(request.META)
	print(data['locations'][0])
	return JsonResponse({'result': 'ok'})