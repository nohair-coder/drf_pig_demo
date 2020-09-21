from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from .models import PigIntake
from apps.pigbase.models import PigBase
from django.db.models import Q
# Create your views here.


class IntakeData(APIView):
    # authentication_classes = [JwtAuthorizationAuthentication, ]

    def get(self, request):
        print(123)
        return JsonResponse({'code': '成功'}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            req = request.data
            req_earid = req['earid']
            req_stationid = req['stationid']
            exist = PigBase.objects.get(earid=req_earid, stationid=req_stationid).pigid
            I = PigIntake()
            I.pigid = PigBase.objects.get(pigid=exist)
            I.food_intake = req['food_intake']
            I.start_time = req['start_time']
            I.end_time = req['end_time']
            I.save()
            return JsonResponse({'code': True}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse({'code': False}, status=status.HTTP_200_OK)

    def put(self, request):
        pass
