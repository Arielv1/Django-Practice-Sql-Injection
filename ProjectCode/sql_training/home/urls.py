from django.urls import path
from . import views
from learn import views as learn_views
from django.contrib.auth import views as auth_views
from . import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('problems', views.problems_list, name='problems_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)