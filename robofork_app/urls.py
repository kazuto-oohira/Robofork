from django.urls import path
from robofork_app.views import vehicle_view, mqtt_test_view
from robofork_app.views.login_view import *
from robofork_app.views.vehicle_control_view import *
from robofork_app.views.api import mqtt, file, location, vehicle_operation_plan, vehicle_operation_status


urlpatterns = [
    # ログイン
    path('', LoginView.as_view(), name='login'),

    # NKC管理画面
    path('admin/location/', TemplateView.as_view(template_name='robofork_app/admin_location/index.html'), name='admin_location_index'),
    path('admin/vehicle/', TemplateView.as_view(template_name='robofork_app/admin_vehicle/index.html'), name='admin_vehicle_index'),
    path('admin/vehicle_status/', TemplateView.as_view(template_name='robofork_app/admin_vehicle_status/index.html'), name='admin_vehicle_status_index'),
    path('admin/user/', TemplateView.as_view(template_name='robofork_app/admin_user/index.html'), name='admin_user_index'),
    path('admin/setting/vehicle_type/', TemplateView.as_view(template_name='robofork_app/admin_setting/vehicle_type/index.html'), name='admin_setting_vehicle_type_user_index'),

    # 各配置場所 管理画面
    path('<int:location_id>/', TemplateView.as_view(template_name='robofork_app/home/index.html'), name='home_index'),
    path('<int:location_id>/vehicle_status/', TemplateView.as_view(template_name='robofork_app/vehicle_status/index.html'), name='vehicle_status_index'),
    path('<int:location_id>/operation_plan/', TemplateView.as_view(template_name='robofork_app/operation_plan/index.html'), name='operation_plan_index'),
    path('<int:location_id>/operation_plan/<int:vehicle_operation_plan_id>', TemplateView.as_view(template_name='robofork_app/operation_plan/detail.html'), name='operation_plan_detail'),
    path('<int:location_id>/operation_plan/new', TemplateView.as_view(template_name='robofork_app/operation_plan/detail.html'), name='operation_plan_new'),

    # 車両マニュアル操作
    path('vehicle/control/<int:vehicle_id>', VehicleControlView.as_view(), name='vehicle_control'),

    # API
    path('api/mqtt/send', mqtt.send),
    path('api/file/<int:file_id>', file.file, name='api_file'),
    path('api/location/<int:location_id>/map_config', location.map_config),
    # path('api/operation_plan/<int:vehicle_operation_plan_id>/config', vehicle_operation_plan.config),
    path('api/operation_plan/<int:vehicle_operation_plan_id>/save', vehicle_operation_plan.save),
    path('api/operation_plan/<int:vehicle_operation_plan_id>/load', vehicle_operation_plan.load),
    path('api/operation_plan/<int:vehicle_operation_plan_id>/execute', vehicle_operation_plan.execute),
    path('api/vehicle_operation_status/load', vehicle_operation_status.load),

    # MQTT テスト
    path('mqtt_test', mqtt_test_view.index),
    path('mqtt_test/route_execute', mqtt_test_view.route_execute),

    # 以下はまだテスト
    path('vehicle', vehicle_view.index, name='vehicle_index'),
    path('vehicle/new', vehicle_view.new, name='vehicle_new'),
    path('vehicle/save', vehicle_view.save, name='vehicle_save'),
    path('vehicle/save/<int:vehicle_id>', vehicle_view.save, name='vehicle_save'),
    path('vehicle/<int:vehicle_id>', vehicle_view.detail, name='vehicle_detail'),
]
