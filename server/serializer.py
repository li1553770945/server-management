from datetime import datetime
from .models import ServerUseModel
from rest_framework import serializers


class ServerUseSerializer(serializers.Serializer):  # 用于登录的表单合法性验证，防止绕过前端验证
    end_time = serializers.DateTimeField(required=True)
    server_id = serializers.IntegerField(required=True)
    public_key = serializers.CharField(max_length=500, required=True)





class ServerUseListSerializer(serializers.ModelSerializer):
    server_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    class Meta:
        model = ServerUseModel
        fields = ['server_name', 'username', 'start_time', 'end_time','public_key']  # 包括其他所需的字段

    def get_server_name(self, obj):
        # 在此方法中返回 server 的名称
        return obj.server.name

    def get_username(self,obj):
        return obj.user.username
