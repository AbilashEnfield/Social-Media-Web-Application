import Actions.routing
import videocall.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            Actions.routing.websocket_urlpatterns +
            videocall.routing.websocket_urlpatterns
        )
    ),
})
