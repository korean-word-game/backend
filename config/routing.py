# mysite/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
import chat.routing
from chat import work_consumers

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
    "channel": ChannelNameRouter({
        "test-worker": work_consumers.PrintConsumer,
    }),
})
