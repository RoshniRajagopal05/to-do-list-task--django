from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, register_user, login_user, admin_login, user_reports, user_usage_reports

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
    path('admin-login/', admin_login), 
    path('user-reports/', user_reports, name='user-reports'),
    path('user-usage-reports/', user_usage_reports, name='user-usage-reports'),  # ✅ NEW
    path('', include(router.urls)),
]
