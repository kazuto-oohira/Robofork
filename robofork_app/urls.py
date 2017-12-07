from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('redirect', views.redirect, name='redirect'),#test
    path('logout', views.logout, name='logout'),
    path('manage',views.redirect, name='manage'),
    path('usr',views.redirect, name='usr'),
    path('plan',views.redirect, name='plan'),
]
