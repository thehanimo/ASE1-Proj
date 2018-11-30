from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Room
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from userAuth.models import User
from executives.models import Executive

def genRoom(customer, executive):
    id1 = customer.id
    id2 = executive.id
    label = str((id1* id1) +(id2 * id2))
    room,created = Room.objects.get_or_create(
        label=label,
        customer=customer,
        executive=executive
        )
    return room


def index(request):
    if request.method == 'POST':
        customer = request.user
        executive = Executive.objects.all().order_by("-complaints_queue").first().user
        room = genRoom(customer,executive)
        return redirect('chat:room', room_name=room.label)
    return render(request, 'chat/index.html')



class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.objects.order_by('-timestamp').all()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        room = Room.objects.get(label=self.room_name)
        message = Message.objects.create(
            author=author_user,
            content=data['message'],
            room=room,
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            if (self.message_to_json(message) is not None):
                result.append(self.message_to_json(message))

        result1 = result[::-1]
        return result1

    def message_to_json(self, message):
        if (message.room.label == str(self.room_name)):
            return {
                'author': message.author.username,
                'content': message.content,
                'timestamp': str(message.timestamp),
                'roomname': message.room.label,
            }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        author = self.scope["user"]
        author_user = User.objects.filter(username=author)[0]
        room = Room.objects.get(label=self.room_name)
        message = Message.objects.create(
            author=author_user,
            content='Left',
            room=room,
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        self.send_chat_message(content)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))