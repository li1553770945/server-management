# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):  # 用于登录的表单合法性验证，防止绕过前端验证
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
