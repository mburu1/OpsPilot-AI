import json
from channels.generic.websocket import AsyncWebsocketConsumer
from platform.logging.logger import get_logger

logger = get_logger('notifications.websocket')

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # In production, we'd verify the JWT here
        self.group_name = f"user_{self.scope['user'].id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        logger.info(f"User {self.scope['user'].id} connected to notifications")

    async def disconnect(self):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        # Event is sent from a Celery task via channel_layer
        await self.send(text_data=json.dumps({
            "type": "NOTIFICATION",
            "message": event["message"],
            "payload": event["payload"]
        }))
