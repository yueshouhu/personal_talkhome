

from django.conf.urls import re_path
# from django.conf.urls import url
from chat import consumers

websocket_urlpatterns = [
    re_path(r'^chat$', consumers.ChatConsumer),

]