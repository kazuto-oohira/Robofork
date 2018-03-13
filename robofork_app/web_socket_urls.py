from channels.routing import route
# from robofork_app.views.mqtt_test_view import ws_add, ws_message, ws_disconnect
import robofork_app.views.mqtt_test_view as mqtt_test_view

channel_routing = [
    route("websocket.connect", mqtt_test_view.ws_add, path="/mqtt_test_ws"),
    route("websocket.receive", mqtt_test_view.ws_message, path="/mqtt_test_ws"),
    route("websocket.disconnect", mqtt_test_view.ws_disconnect, path="/mqtt_test_ws"),

    route("websocket.connect", mqtt_test_view.ws_add, path="/vehicle_operation_status"),
    route("websocket.receive", mqtt_test_view.ws_message, path="/vehicle_operation_status"),
    route("websocket.disconnect", mqtt_test_view.ws_disconnect, path="/vehicle_operation_status"),
]
