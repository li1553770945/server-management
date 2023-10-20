from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash

import utils.para_valid
from .serializer import LoginSerializer, PasswordChangeSerializer
from django.contrib import auth


class LoginView(APIView):
    def post(self, request):
        context = dict()
        data = LoginSerializer(data=request.data)
        if not data.is_valid():  # 验证有效性
            errors = data.errors
            context['msg'] = utils.para_valid.get_first_error(errors)
            context['code'] = 4001
            return Response(context)

        data = data.data
        username = data['username']
        password = data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:  # 用户名或密码错误
            context['msg'] = "用户名或密码错误"
            context['code'] = 4003
            return Response(context)

        auth.login(request, user)
        context['code'] = 0
        return Response(context)


class PasswordChangeView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        context = dict()
        data = PasswordChangeSerializer(data=request.POST)
        if not data.is_valid():  # 验证有效性
            errors = data.errors
            context['msg'] = utils.para_valid.get_first_error(errors)
            context['code'] = 4001
            return Response(context)

        data = data.data
        old_password = data['old_password']
        new_password = data['new_password']
        if not request.user.check_password(old_password):
            context['code'] = 4003
            context['msg'] = "密码错误"
            return Response(context)

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        context['code'] = 0
        return Response(context)





class MyInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        # 在这里根据需要定制要返回的用户信息
        user_data = {
            'id': user.id,
            'username': user.username,
            'name':user.name,
            'email': user.email,
            # 添加其他需要的字段
        }
        return Response(user_data)
