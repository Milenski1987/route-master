from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from accounts.forms import RouteMasterLoginForm
from accounts.views import UserRegisterView, UserProfileView, UserSettingsView, AdminDashboardAPIView

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', include([
        path('', UserProfileView.as_view(), name='profile'),
        path('settings/',UserSettingsView.as_view() ,name='settings')
    ])),
    path('login/', LoginView.as_view(template_name='account/login.html', authentication_form=RouteMasterLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/users/', AdminDashboardAPIView.as_view(), name='users-api')
]

