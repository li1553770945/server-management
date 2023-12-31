"""
URL configuration for server_managerment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from user.views import PasswordChangeView, MyInfoView,CustomTokenObtainPairView,CustomTokenRefreshView
from server.views import ServerUseView, ServerUseListView,ServerCurrentUsersView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('api/my-info/', MyInfoView.as_view(), name='my-info'),
    path('api/server-use/', ServerUseView.as_view(), name='server-use'),
    path('api/server-use-list/', ServerUseListView.as_view(), name='server-use-list'),
    path('api/server-use-users/', ServerCurrentUsersView.as_view(), name='server-use-users'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

