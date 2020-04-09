# from django.conf.urls import url
# from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

# application = ProtocolTypeRouter({
# Websocket chat handler
# 'websocket':
# AllowedHostsOriginValidator(
#     AuthMiddlewareStack(
#         URLRouter([
#             # url(r"chat/", TaskConsumer, name='chat'),
#             url(r"messages/(?P<username>[\w.@+-]+)/$",
#                 HomeConsumer,
#                 name='home')
#         ])), ),
# 'channel':
# ChannelNameRouter({'task': TaskConsumer})
# })

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import home.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket':
    AuthMiddlewareStack(URLRouter(home.routing.websocket_urlpatterns)),
})