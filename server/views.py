from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import ServerUseSerializer, ServerUseListSerializer
import utils.para_valid
from .models import ServerModel, ServerUseModel
from datetime import datetime
from django.utils import timezone


# Create your views here.
class ServerUseView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        context = dict()
        data = ServerUseSerializer(data=request.data)
        if not data.is_valid():  # 验证有效性
            errors = data.errors
            context['msg'] = utils.para_valid.get_first_error(errors)
            context['code'] = 4001
            return Response(context)

        data = data.data
        server_id = data['server_id']
        public_key = data['public_key']
        end_time = data['end_time']

        query = ServerModel.objects.filter(id=server_id)
        if not query.exists():
            context['code'] = 4004
            context['msg'] = "没有找到对应的服务器"
            return Response(context)
        server = query.first()

        if end_time < datetime.now():
            context['code'] = 4002
            context['msg'] = "结束时间不能小于当前时间"
            return Response(context)

        ServerUseModel.objects.create(
            user=request.user,
            server=server,
            public_key=public_key,
            start_time=datetime.now(),
            end_time=end_time,
            status="creating"
        )
        context['code'] = 0
        return Response(context)

    def put(self, request):
        pass


class ServerUseListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        context = dict()
        server_id = request.GET.get("server_id")
        user_id = None
        if request.user.is_authenticated:
            user_id = request.user.id
        if server_id is not None:
            server_use_list = ServerUseModel.objects.filter(server_id=server_id,
                                                            start_time__lt=timezone.now(),
                                                            end_time__gt=timezone.now())
            context['code'] = 0
            context['data'] = ServerUseSerializer(server_use_list, many=True).data
            return Response(context)

        if user_id is not None:
            server_use_list = ServerUseModel.objects.filter(user_id=user_id,
                                                            start_time__lt=timezone.now(),
                                                            end_time__gt=timezone.now())
            context['code'] = 0
            context['data'] = ServerUseSerializer(server_use_list, many=True).data
            return Response(context)

        context['code'] = 4003
        context['msg'] = "未登录"
        return Response(context)
