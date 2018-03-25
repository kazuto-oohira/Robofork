from channels.routing import route
import robofork_app.views.mqtt_test_view as mqtt_test_view
from robofork_app.views.api import vehicle_operation_status
channel_routing = [
    route("websocket.connect", mqtt_test_view.ws_add, path="/mqtt_test_ws"),
    route("websocket.receive", mqtt_test_view.ws_message, path="/mqtt_test_ws"),
    route("websocket.disconnect", mqtt_test_view.ws_disconnect, path="/mqtt_test_ws"),

    route("websocket.connect", vehicle_operation_status.ws_add, path="/vehicle_operation_status/<int:location_id>"),
    route("websocket.connect", vehicle_operation_status.ws_add, path="/vehicle_operation_status"),  # 不要になったら消す
    route("websocket.receive", vehicle_operation_status.ws_message, path="/vehicle_operation_status/<int:location_id"),
    route("websocket.receive", vehicle_operation_status.ws_message, path="/vehicle_operation_status"),  # 不要になったら消す
    route("websocket.disconnect", vehicle_operation_status.ws_disconnect, path="/vehicle_operation_status/<int:location_id"),
    route("websocket.disconnect", vehicle_operation_status.ws_disconnect, path="/vehicle_operation_status"),    # 不要になったら消す
]

