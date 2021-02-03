from django.urls import path
from . import views

urlpatterns = [
    path('', views.learn, name='learn'),
    path('inband', views.inband, name='inband'),
    path('blind', views.blind, name='blind'),
    path('outband', views.outband, name='outband'),
    path('tools', views.tools, name='tools'),
    path('prevent_sqli', views.prevent_sqli, name='prevent_sqli'),
]