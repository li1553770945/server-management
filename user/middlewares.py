# custom_authentication_middleware.py
from django.http import JsonResponse
import re


class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.anonymous_url_pattern = r"^(/admin|/api/login).*$"

    def __call__(self, request):
        print(request.path)
        if not re.match(self.anonymous_url_pattern, request.path):
            if not request.user.is_authenticated:
                response_data = {'code': 4003, 'msg': "请登录后使用"}
                return JsonResponse(response_data, status=403)

        response = self.get_response(request)
        return response
