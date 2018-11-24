from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from channels.sessions import SessionMiddlewareStack
from django.conf.urls import url
from chat.consumers import *

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            URLRouter(
                [
                    url(r"^chat/(?P<email>[\w.@+-]+)/$", ChatConsumer)
                ]
            )
        )
    )
})
