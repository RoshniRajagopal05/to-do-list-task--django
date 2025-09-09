# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Task

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']

# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = '__all__'
#         read_only_fields = ['user']  # ✅ Add this line



from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, UserActionLog

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "created_at", "is_completed"]

class UserReportSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "tasks"]


# ✅ NEW: User Usage Report Serializer
# class UserUsageReportSerializer(serializers.ModelSerializer):
#     added = serializers.SerializerMethodField()
#     deleted = serializers.SerializerMethodField()
#     completed = serializers.SerializerMethodField()
#     edited = serializers.SerializerMethodField()
#     imported = serializers.SerializerMethodField()
#     exported = serializers.SerializerMethodField()
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserActionLog

class UserUsageReportSerializer(serializers.ModelSerializer):
    # ✅ Computed fields using SerializerMethodField
    added = serializers.SerializerMethodField()
    deleted = serializers.SerializerMethodField()
    completed = serializers.SerializerMethodField()
    edited = serializers.SerializerMethodField()
    imported = serializers.SerializerMethodField()
    exported = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "added",
            "deleted",
            "completed",
            "edited",
            "imported",
            "exported",
        ]

    # ✅ These methods are automatically called for SerializerMethodField
    def get_added(self, obj):
        return UserActionLog.objects.filter(user=obj, action="add").count()

    def get_deleted(self, obj):
        return UserActionLog.objects.filter(user=obj, action="delete").count()

    def get_completed(self, obj):
        return UserActionLog.objects.filter(user=obj, action="complete").count()

    def get_edited(self, obj):
        return UserActionLog.objects.filter(user=obj, action="edit").count()

    def get_imported(self, obj):
        return UserActionLog.objects.filter(user=obj, action="import").count()

    def get_exported(self, obj):
        return UserActionLog.objects.filter(user=obj, action="export").count()
