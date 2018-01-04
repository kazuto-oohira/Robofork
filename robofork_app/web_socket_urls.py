from channels.routing import route
from robofork_app.views.mqtt_test_view import ws_add, ws_message, ws_disconnect


channel_routing = [
    route("websocket.connect", ws_add, path="/mqtt_test_ws"),
    route("websocket.receive", ws_message, path="/mqtt_test_ws"),
    route("websocket.disconnect", ws_disconnect, path="/mqtt_test_ws"),
]
