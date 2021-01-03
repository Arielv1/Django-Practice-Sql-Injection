from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views as user_views
from django.conf import settings
from django.conf.urls.static import static
# from .views import FilteredSqlProblemListView

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('edit_profile/', user_views.edit_profile, name='edit_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('change_password', user_views.change_password, name='change_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)