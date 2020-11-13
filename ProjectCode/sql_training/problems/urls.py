from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login_problem', views.problem_login, name='login_problem'),
    path('1', views.first_problem, name='first'),
    path('2', views.second_problem, name='second'),
    path('3', views.third_problem, name='third'),
    path('4', views.forth_problem, name='forth'),
    path('5', views.fifth_problem, name='fifth'),
    path('6', views.sixth_problem, name='sixth'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)