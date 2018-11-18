from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

rec_name = ""
u = ""

def genRoom(id1,id2):
    return str((id1* id1) +(id2 * id2))


def index(request):
    k = ""
    if request.method == 'POST':
        global u
        global rec_name
        u = request.user
        rec_name = request.POST['rec-input']
        print(u)
        a = User.objects.get(username=u)
        b = User.objects.get(username=rec_name)
        print(a.id)
        print(b.id)
        sender_id = a.id
        rec_id = b.id

        print(rec_name)
        roomie = genRoom(sender_id,rec_id)
        k = '/chat/' + roomie
        return HttpResponseRedirect(k)
    return render(request, 'chat/index.html')


User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.last_10_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        print(author)

        author_user = User.objects.filter(username=author)[0]
        global rec_name, u
        a = User.objects.get(username=u)
        b = User.objects.get(username=rec_name)
        print(a.id)
        print(b.id)
        sender_id = a.id
        rec_id = b.id
        print(rec_name)
        print(author_user)

        message = Message.objects.create(
            author=author_user,
            content=data['message'],
            roomname=self.room_name,
            rec_name=rec_name
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
        print(result1)

        return result1

    def message_to_json(self, message):
        if (message.roomname == str(self.room_name)):
            return {
                'author': message.author.username,
                'content': message.content,
                'timestamp': str(message.timestamp),
                'roomname': message.roomname,
                'rec_name': message.rec_name

            }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name
        global u, rec_name
        a = User.objects.get(username=u)
        b = User.objects.get(username=rec_name)
        print(a.id)
        print(b.id)
        sender_id = a.id
        rec_id = b.id
        self.room_group_name = genRoom(sender_id,rec_id)
        print(self.room_group_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
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