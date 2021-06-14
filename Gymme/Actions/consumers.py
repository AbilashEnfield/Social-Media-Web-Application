import json
import base64
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from .models import chatContent, chatroom
from Accounts.models import People, Trainer
from django.core.files.base import ContentFile


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.roomCode = self.scope['url_route']['kwargs']['roomCode']
        self.room_group_code = 'chatroom_%s' % self.roomCode

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_code,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_code,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        msgtype = text_data_json['type']
        username = text_data_json['username']
        id = text_data_json['id']
        if msgtype == 'image' or msgtype == 'video' or msgtype == 'audio':
            print('here')
            format, filestr = message.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(filestr), name=msgtype + '.' + ext)
            roomNo = chatroom.objects.get(roomcode=self.roomCode)
            chatter = User.objects.get(id=id)
            chatData = chatContent.objects.create(chatRoom=roomNo, chatter=chatter, msg_type=msgtype, upload_file=data)
            print('hi')
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_code,
                {
                    'type': 'chatroom_message',
                    'msgtype': msgtype,
                    'message': message,
                    'username': username

                }
            )
        else:
            roomNo = chatroom.objects.get(roomcode=self.roomCode)
            chatter = User.objects.get(id=id)
            chatData = chatContent.objects.create(chatRoom=roomNo, chatter=chatter, chatContentText=message)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_code,
                {
                    'type': 'chatroom_message',
                    'msgtype': msgtype,
                    'message': message,
                    'username': username

                }
            )

    def chatroom_message(self, event):
        print('chat')
        message = event['message']
        msgtype = event['msgtype']
        username = event['username']

        async_to_sync(
            self.send(text_data=json.dumps({
                'message': message,
                'username': username,
                'msgtype': msgtype

            }))
        )
    print('end')
