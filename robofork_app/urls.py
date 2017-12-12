from django.urls import path
from robofork_app.views import top_view, vehicle_view

urlpatterns = [
    path('', top_view.index, name='top'),
    path('vehicle', vehicle_view.index, name='vehicle_index'),
    path('vehicle/new', vehicle_view.new, name='vehicle_new'),
    path('vehicle/save', vehicle_view.save, name='vehicle_save'),

    # 奥田くんのやつは一旦コメントアウト
    # path('redirect', views.redirect, name='redirect'),
    # path('logout', views.logout, name='logout'),
    # path('manage',views.index, name='manage'),
    # path('usr',views.index, name='usr'),
    # path('plan',views.index, name='plan'),
]
