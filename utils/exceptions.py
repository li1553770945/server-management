from rest_framework.exceptions import AuthenticationFailed,NotAuthenticated
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        response_data = {
            'code': 4003,  # 自定义错误代码
            'msg': 'token验证失败',  # 自定义错误消息
        }
        response = Response(response_data)
    if isinstance(exc, NotAuthenticated):
        response_data = {
            'code': 4003,  # 自定义错误代码
            'msg': '未提交token信息',  # 自定义错误消息
        }
        response = Response(response_data)
    return response