from django.urls import path
from . import views

urlpatterns = [
    path('', views.learn, name='learn'),
    path('inband', views.inband, name='inband'),
    path('blind', views.blind, name='blind'),
    path('outband', views.outband, name='outband'),
    path('tools', views.tools, name='tools'),
    path('protection', views.protection, name='protection'),

    path('check', views.check, name='check'),

]