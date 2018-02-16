from django.urls import path
from robofork_app.views import top_view, vehicle_view, mqtt_test_view
from robofork_app.views.operation_plan.operation_plan_detail_view import *
from robofork_app.views.vehicle_control_view import *

urlpatterns = [
    path('', top_view.index, name='top'),
    path('vehicle', vehicle_view.index, name='vehicle_index'),
    path('vehicle/new', vehicle_view.new, name='vehicle_new'),
    path('vehicle/save', vehicle_view.save, name='vehicle_save'),
    path('vehicle/save/<int:vehicle_id>', vehicle_view.save, name='vehicle_save'),
    path('vehicle/<int:vehicle_id>', vehicle_view.detail, name='vehicle_detail'),

    path('operation_plan', OperationPlanDetailView.as_view(), name='operation_show'),

    path('vehicle/control/<int:vehicle_id>', VehicleControlView.as_view(), name='vehicle_control'),

    # MQTT テスト
    path('mqtt_test', mqtt_test_view.index),
    path('mqtt_test/send', mqtt_test_view.send),

    # 奥田くんのやつは一旦コメントアウト
    # path('redirect', views.redirect, name='redirect'),
    # path('logout', views.logout, name='logout'),
    # path('manage',views.index, name='manage'),
    # path('usr',views.index, name='usr'),
    # path('plan',views.index, name='plan'),
]
