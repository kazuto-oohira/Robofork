from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('redirect', views.redirect, name='redirect'),
    path('logout', views.logout, name='logout'),
    path('manage',views.index, name='manage'),
    path('usr',views.index, name='usr'),
    path('plan',views.index, name='plan'),
]
