from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import ServerUseSerializer, ServerUseListSerializer
import utils.para_valid
from .models import ServerModel, ServerUseModel
from datetime import datetime
from django.utils import timezone


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


# Create your views here.
class ServerUseView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        context = dict()
        data = ServerUseSerializer(data=request.data)
        if not data.is_valid():  # 验证有效性
            errors = data.errors
            context['msg'] = utils.para_valid.get_first_error(errors)
            context['code'] = 4001
            return Response(context)

        data = data.validated_data
        server_id = data['server_id']
        public_key = data['public_key']
        end_time = data['end_time']
        query = ServerModel.objects.filter(id=server_id)
        if not query.exists():
            context['code'] = 4004
            context['msg'] = "没有找到对应的服务器"
            return Response(context)

        if end_time < datetime.now():
            context['code'] = 4002
            context['msg'] = "结束时间不能小于当前时间"
            return Response(context)

        ServerUseModel.objects.create(
            user=request.user,
            server_id=server_id,
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
        if server_id is not None:
            try:
                server_id = int(server_id)
            except Exception as err:
                context['code'] = 4001
                context['msg'] = f"参数错误{err}"
                return Response(context)
        else:
            server_name = request.GET.get("server_name")
            if server_name is None:
                server_id = None
            else:
                server_name = request.GET.get("server_name")
                server = ServerModel.objects.filter(name=server_name)
                if not server.exists():
                    context['code'] = 4004
                    context['msg'] = f"未找到对应的服务器"
                    return Response(context)
                server_id = server.first().id


        user_id = None
        if request.user.is_authenticated:
            user_id = request.user.id
        if server_id is not None:
            server_use_list = ServerUseModel.objects.filter(server_id=server_id,
                                                            start_time__lt=timezone.now(),
                                                            end_time__gt=timezone.now())
            context['code'] = 0
            context['data'] = ServerUseListSerializer(server_use_list, many=True).data
            return Response(context)

        if user_id is not None:
            server_use_list = ServerUseModel.objects.filter(user_id=user_id,
                                                            start_time__lt=timezone.now(),
                                                            end_time__gt=timezone.now())
            context['code'] = 0
            context['data'] = ServerUseListSerializer(server_use_list, many=True).data
            return Response(context)
        return Response(context)


class ServerCurrentUsersView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        context = dict()
        server_id = request.GET.get("server_id")
        if server_id is not None:
            try:
                server_id = int(server_id)
            except Exception as err:
                context['code'] = 4001
                context['msg'] = f"参数错误{err}"
                return Response(context)
        else:
            server_name = request.GET.get("server_name")
            server = ServerModel.objects.filter(name=server_name)
            if not server.exists():
                context['code'] = 4004
                context['msg'] = f"未找到对应的服务器"
                return Response(context)
            server_id = server.first().id

        server_use_list = ServerUseModel.objects.filter(server_id=server_id,
                                                        start_time__lt=timezone.now(),
                                                        end_time__gt=timezone.now())
        context['code'] = 0
        context['data'] = [server_use.user.username for server_use in server_use_list]
        return Response(context)

