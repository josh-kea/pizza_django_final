from channels.generic.websocket import AsyncWebsocketConsumer

import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "Notification_Group"  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
        
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    async def notify(self, event):
        await self.send(text_data=json.dumps(event["text"]))

class OrderStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.group_name = "Order_Status_Group"  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
        
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    # Custom Update Order Status function for employees to update order status on the frontend
    async def update_status(self, event):
        await self.send(text_data=event["text"])
