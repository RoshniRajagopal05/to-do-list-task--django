from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Task, UserActionLog
from .serializers import TaskSerializer, UserReportSerializer, UserUsageReportSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])  # ✅ Only admin can access
def user_reports(request):
    users = User.objects.filter(is_superuser=False)
    serializer = UserReportSerializer(users, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAdminUser])  # ✅ Only admin can access
# def user_usage_reports(request):
#     users = UserActionLog.objects.all()
#     print(users)
#     serializer = UserUsageReportSerializer(users, many=True)
#     print(serializer.data)
#     return Response(serializer.data)

from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .serializers import UserUsageReportSerializer

from django.contrib.auth.models import User
from django.db.models import Count, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAdminUser])  # ✅ Only admin can access
def user_usage_reports(request):
    # ✅ Query User model and annotate counts from UserActionLog
    users = User.objects.annotate(
        added=Count("useractionlog", filter=Q(useractionlog__action="add")),
        deleted=Count("useractionlog", filter=Q(useractionlog__action="delete")),
        completed=Count("useractionlog", filter=Q(useractionlog__action="complete")),
        edited=Count("useractionlog", filter=Q(useractionlog__action="edit")),
        imported=Count("useractionlog", filter=Q(useractionlog__action="import")),
        exported=Count("useractionlog", filter=Q(useractionlog__action="export")),
    )

    serializer = UserUsageReportSerializer(users, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'User already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    token = Token.objects.create(user=user)
    return Response({'token': token.key, 'user_id': user.id, 'username': user.username})


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username})
    return Response({'error': 'Invalid Credentials'}, status=400)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        tasks = Task.objects.filter(user=user).order_by('-due_date')

        status_param = self.request.query_params.get('status')
        search = self.request.query_params.get('search')

        if status_param == 'pending':
            tasks = tasks.filter(is_completed=False)
        elif status_param == 'completed':
            tasks = tasks.filter(is_completed=True)

        if search:
            tasks = tasks.filter(title__icontains=search)

        return tasks
    

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)
        # ✅ Log action
        UserActionLog.objects.create(user=self.request.user, action="add")


@api_view(['POST'])
def admin_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(username,password)

    user = authenticate(username=username, password=password)

    if user and user.is_superuser:   # ✅ only allow superusers
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'is_admin': True
        })
    return Response({'error': 'Invalid admin credentials'}, status=400)
