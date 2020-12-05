from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('1', views.first_problem, name='first'),
    path('2', views.second_problem, name='second'),
    path('3', views.third_problem, name='third'),
    path('4', views.forth_problem, name='forth'),
    path('5', views.fifth_problem, name='fifth'),
    path('6', views.sixth_problem, name='sixth'),
    path('7', views.seventh_problem, name='seventh'),
    path('8', views.eighth_problem, name='eighth'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

