from channels.generic.websocket import WebsocketConsumer
import json
import time

class ChatConsumer(WebsocketConsumer):
    '''websocket请求'''
    # 用户存储当前聊天室用户
    waiters = set()
    # 用于存储历时消息
    messages = []

    def connect(self):
        '''客户端连接'''
        print("客户连接")

        ChatConsumer.waiters.add(self)
        self.accept()
        # ww=WebsocketConsumer.session['username']

    def disconnect(self, close_code):
        '''客户端断开连接'''
        ChatConsumer.waiters.remove(self)

        # Receive message from room group
    def receive(self, text_data):
        print(text_data)
        '''客户端发来数据'''
        # message = event['message']
        #
        # # Send message to WebSocket
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
        msg = json.loads(text_data)
        ctime = time.strftime("%Y-%m-%d %X", time.localtime())
        msg["ctime"]=ctime
        if msg['message']=="查看历史消息":
            for i in ChatConsumer.messages:
                self.send(text_data='''<div style="border: 1px solid #dddddd;margin: 10px;">
    <div>%s | %s</div>
    <div style="margin-left: 20px;">%s</div>
</div>'''%(i['uid'],i['ctime'],i['message']))
        else:
            ChatConsumer.messages.append(msg)
            for client in ChatConsumer.waiters:
                # content = client.render_string('message.html', **msg)
                content='''<div style="border: 1px solid #dddddd;margin: 10px;">
        <div>%s | %s</div>
        <div style="margin-left: 20px;">%s</div>
    </div>'''%(msg['uid'],ctime,msg['message'])

                client.send(text_data=content)

    # def receive(self, text_data):
    #     msg = json.loads(text_data)
    #
    #     ChatConsumer.messages.append(text_data)
    #     for client in ChatConsumer.waiters:
    #         content = client.render_string('message.html', **msg)
    #         print(content)
    #         client.send(text_data=content)
    #     ChatConsumer.messages.clear()

        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        #
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
