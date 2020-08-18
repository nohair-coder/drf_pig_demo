from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from apps.pigbase.models import PigBase
from apps.station.models import StationInfo
from utils.jwt_token.jwt_auth import JwtAuthorizationAuthentication
# Create your views here.


class SystemCheck(APIView):
    authentication_classes = [JwtAuthorizationAuthentication, ]

    def get(self, request):
        pig_num = PigBase.objects.filter().count()
        station_num = StationInfo.objects.filter().count()
        data = {
            'pig_num': pig_num,
            'station_num': station_num
        }
        # print(pig_num)
        # print(station_num)
        return JsonResponse(
            {'code': '获取成功',
             'data': data
             },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        pass

    def put(self, request):
        pass
