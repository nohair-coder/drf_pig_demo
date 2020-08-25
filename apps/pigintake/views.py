from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from utils.jwt_token.jwt_auth import JwtAuthorizationAuthentication
# Create your views here.


class IntakeData(APIView):
    # authentication_classes = [JwtAuthorizationAuthentication, ]

    def get(self, request):
        print(123)
        return JsonResponse({'code': '成功'}, status=status.HTTP_200_OK)

    def post(self, request):
        pass

    def put(self, request):
        pass
