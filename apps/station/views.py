from .models import StationInfo
from apps.pigbase.models import PigBase
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from utils.jwt_token.jwt_auth import JwtAuthorizationAuthentication


# Create your views here.
class StationCheck(APIView):

    authentication_classes = [JwtAuthorizationAuthentication, ]

    def post(self, request):
        try:
            req = request.data
            print(req)
            existStation = StationInfo.objects.filter(build_unit_station=req).first()
            if existStation == None:
                S = StationInfo()
                S.build_unit_station = req
                # S.save()
                return JsonResponse({'code': '饲喂站添加成功'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'code': '饲喂站已存在,请重新输入'}, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'code': '添加失败'}, status=201)

    def get(self, request):
        try:
            stationlist = StationInfo.objects.filter()
            station_options = list()
            all_station = list()
            for s in stationlist:
                s_info = dict()
                s_info['build_unit_station'] = s.build_unit_station
                s_info['status'] = s.get_status_display()
                s_info['temperature'] = s.temperature
                s_info['humidity'] = str(s.humidity * 100) + '%'
                s_info['status_num'] = s.status_num
                all_station.append(s_info)
                station_options.append({
                    'value' : s_info['build_unit_station'],
                    'label' : s_info['build_unit_station']
                })
            # print(station_options)
            total = len(all_station)
            return JsonResponse({'all_station': all_station,
                                 'total': total,
                                 'station_options': station_options,
                                 "code": "SUCCESS"}, status=status.HTTP_200_OK)
            # return JsonResponse({'code': 'SUCCESS'})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 'error'}, status=201)

    def put(self, request):
        pass

    def delete(self, request):
        pass

