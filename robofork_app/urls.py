from django.urls import path
from robofork_app.controllers import top

urlpatterns = [
    path('', top.index, name='top'),

    # 奥田くんのやつは一旦コメントアウト
    # path('redirect', views.redirect, name='redirect'),
    # path('logout', views.logout, name='logout'),
    # path('manage',views.index, name='manage'),
    # path('usr',views.index, name='usr'),
    # path('plan',views.index, name='plan'),
]
