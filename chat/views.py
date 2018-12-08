from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from .models import Room


@login_required
def room(request, room_name):
	try:
		room = Room.objects.get(label=room_name)
	except Room.DoesNotExist:
		return redirect('forbidden')
	if request.user.user_type == 3:
		if room.executive == None:
			room.executive = request.user
			room.save()
		else:
			return redirect('forbidden')
	elif request.user.user_type == 1:
		if room.customer != request.user:
			return redirect('forbidden')
	else:
		return redirect('forbidden')
	return render(request, 'chat/room.html',{
		'room_name_json': mark_safe(json.dumps(room_name)),
		'username': mark_safe(json.dumps(request.user.username)),
		'user_type': mark_safe(json.dumps(request.user.user_type)),
	})

def success(request):
	return render(request, 'chat/support_success.html')

def error(request):
	return render(request, 'chat/support_error.html')