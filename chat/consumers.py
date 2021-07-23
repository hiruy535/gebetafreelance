import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chatall.models import Thread, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        self.room_group_name = 'chat_%s' % self.room_name
        me = self.scope['user']
        thread_obj = 'self.room_name'
        if me.username != self.room_name:
            self.thread_obj = await self.get_thread(me ,self.room_name)

            self.room_group_name = f"chat_{self.thread_obj.id}"


        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name

        )

        await self.accept()

    async def disconnect(self, close_code):
        print("disconnect "+ self.room_group_name)
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json is not None:
            message = text_data_json['message']
            username = text_data_json['username']
            timestamp = text_data_json['timestamp']

            print(message,timestamp)
            if message != '':
                #print("send-data",text_data)
                me = self.scope['user']
                #await self.create_chat(me, message, timestamp)

                
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username' : username,
                        'timestamp' : timestamp,
                    }
                )


    @database_sync_to_async
    def get_thread(self, user, other_user):
        return Thread.objects.get_or_new(user,other_user)[0]

    @database_sync_to_async
    def create_chat(self, me, msg, timestamp):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg,timestamp=timestamp)

    # Receive message from room group
    async def chat_message(self, event):
        msg = event.get('message', None)
        if msg is not None:
            message = event['message']
            username = event['username']
            timestamp = event['timestamp'] 


            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                    'type': 'websocket.send',
                    'message': message,
                    'username' : username,
                    'timestamp' : timestamp,
            }))
