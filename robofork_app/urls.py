from django.urls import path
from django.views.generic import TemplateView

from robofork_app.views import admin_vehicle_view, admin_location_view, admin_user_view, admin_setting_vehicle_type_view, mqtt_test_view, home_view, vehicle_status_view, sp_view
from robofork_app.views.operation_plan_view import OperationPlanIndexView, OperationPlanDetailView
from robofork_app.views import operation_plan_view
from robofork_app.views.api import mqtt, file, location, vehicle_operation_plan, vehicle_operation_status, emergency, vehicle_control


urlpatterns = [
    # ログイン
    path('', TemplateView.as_view(template_name='robofork_app/login.html'), name='login'),

    # NKC管理画面
    path('admin/location', admin_location_view.index, name='admin_location_index'),
    path('admin/location/new', admin_location_view.new, name='admin_location_new'),

    path('admin/user', admin_user_view.index, name='admin_user_index'),

    path('admin/vehicle_status', TemplateView.as_view(template_name='robofork_app/admin_vehicle_status/index.html'), name='admin_vehicle_status_index'),

    path('admin/setting/vehicle_type', admin_setting_vehicle_type_view.index, name='admin_setting_vehicle_type_index'),
    path('admin/setting/vehicle_type/new', admin_setting_vehicle_type_view.new, name='admin_setting_vehicle_type_detail'),

    path('admin/vehicle', admin_vehicle_view.index, name='admin_vehicle_index'),
    path('admin/vehicle/new', admin_vehicle_view.new, name='vehicle_new'),
    path('admin/vehicle/save', admin_vehicle_view.save, name='vehicle_save'),
    path('admin/vehicle/save/<int:vehicle_id>', admin_vehicle_view.save, name='vehicle_save'),
    path('admin/vehicle/<int:vehicle_id>', admin_vehicle_view.detail, name='vehicle_detail'),

    # 各配置場所 管理画面
    path('<int:location_id>/', home_view.index, name='home_index'),
    path('<int:location_id>/vehicle_status/', vehicle_status_view.index, name='vehicle_status_index'),
    path('<int:location_id>/operation_plan/', OperationPlanIndexView.as_view(), name='operation_plan_index'),
    path('<int:location_id>/operation_plan/<int:vehicle_operation_plan_id>', OperationPlanDetailView.as_view(), name='operation_plan_detail'),
    path('<int:location_id>/operation_plan/new', operation_plan_view.detail_new, name='operation_plan_new'),

    # スマフォ画面
    path('sp/<int:location_id>/', sp_view.index),
    path('sp/vehicle/control/<int:vehicle_id>', sp_view.control),
    path('sp/vehicle/status/<int:vehicle_id>', sp_view.status),
    path('sp/vehicle/operation_plan/<int:vehicle_id>', sp_view.operation_plan),

    # API
    path('api/mqtt/send', mqtt.send),
    path('api/vehicle/control/<int:vehicle_id>', vehicle_control.manual_control),
    path('api/vehicle/auto_flag/<int:vehicle_id>', vehicle_control.auto_control_flag),
    path('api/file/<int:file_id>', file.file, name='api_file'),
    path('api/emergency/<int:location_id>/execute', emergency.execute),
    path('api/location/<int:location_id>/map_config', location.map_config),
    path('api/operation_plan/<int:vehicle_operation_plan_id>/save', vehicle_operation_plan.save),
    path('api/operation_plan/<int:vehicle_operation_plan_id>/load', vehicle_operation_plan.load),
    path('api/operation_plan/<int:vehicle_operation_plan_id>/execute', vehicle_operation_plan.execute),
    path('api/vehicle_operation_status/<int:location_id>/load/', vehicle_operation_status.load),

    # MQTT テスト
    path('mqtt_test/<int:vehicle_id>', mqtt_test_view.index),
    path('mqtt_test/<int:vehicle_id>/route_execute', mqtt_test_view.route_execute),
]



