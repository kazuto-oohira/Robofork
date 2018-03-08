from django.urls import path
from robofork_app.views import top_view, vehicle_view, mqtt_test_view
from robofork_app.views.login_view import *
from robofork_app.views.operation_plan.operation_plan_detail_view import *
from robofork_app.views.vehicle_control_view import *

urlpatterns = [
    # ログイン
    path('', LoginView.as_view(), name='login'),

    # NKC管理画面
    path('admin/home', TemplateView.as_view(template_name='robofork_app/admin_home/home.html'), name='admin_home'),

    path('top', top_view.index),

    path('vehicle', vehicle_view.index, name='vehicle_index'),
    path('vehicle/new', vehicle_view.new, name='vehicle_new'),
    path('vehicle/save', vehicle_view.save, name='vehicle_save'),
    path('vehicle/save/<int:vehicle_id>', vehicle_view.save, name='vehicle_save'),
    path('vehicle/<int:vehicle_id>', vehicle_view.detail, name='vehicle_detail'),

    path('operation_plan/<int:operation_plan_id>', OperationPlanDetailView.as_view()),

    path('vehicle/control/<int:vehicle_id>', VehicleControlView.as_view(), name='vehicle_control'),

    # MQTT テスト
    path('mqtt_test', mqtt_test_view.index),
    path('mqtt_test/send', mqtt_test_view.send),
    path('mqtt_test/route_execute', mqtt_test_view.route_execute),
]
