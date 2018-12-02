from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from .models import Room


@login_required
def room(request, room_name):
	if request.user.user_type == 3:
		Room.objects.get(label=room_name).executive = request.user

	return render(request, 'chat/room.html',{
		'room_name_json': mark_safe(json.dumps(room_name)),
		'username': mark_safe(json.dumps(request.user.username)),
		'user_type': mark_safe(json.dumps(request.user.user_type)),
	})

def success(request):
	return render(request, 'chat/support_success.html')

def error(request):
	return render(request, 'chat/support_error.html')