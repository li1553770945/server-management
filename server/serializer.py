from rest_framework import serializers


class ServerUseSerializer(serializers.Serializer):  # 用于登录的表单合法性验证，防止绕过前端验证
    end_time = serializers.DateTimeField(required=True)
    server_id = serializers.IntegerField(required=True)
    public_key = serializers.CharField(max_length=500, required=True)


class UserNameField(serializers.Field):
    def to_representation(self, obj):
        return obj.user.first_name


class ServerUseListSerializer(serializers.Serializer):

    user_name = UserNameField(source='*')  # 使用自定义字段

    class Meta:
        model = ServerUseSerializer
        fields = ['server_id', 'user_name','start_time','end_time']  # 包括其他所需的字段

