from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, register_user, login_user, admin_login, user_reports, user_usage_reports
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
    path('admin-login/', admin_login), 
    path('user-reports/', user_reports, name='user-reports'),
     path("api/token-auth/", obtain_auth_token, name="api_token_auth"),
    path('user-usage-reports/', user_usage_reports, name='user-usage-reports'),  # ✅ NEW
    path('', include(router.urls)),
]
