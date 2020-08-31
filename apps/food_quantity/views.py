from .models import FoodQuantity
from apps.pigbase.models import PigBase
from django.http import JsonResponse
from rest_framework.views import APIView
from utils.jwt_token.jwt_auth import JwtAuthorizationAuthentication
import json
from .logic import is_none, caldate, final, algo_backfat


# Create your views here.



class SetIntake(APIView):
    authentication_classes = [JwtAuthorizationAuthentication, ]

    def get(self, request):
        req = request.query_params['StationId']
        try:
            # print(req)
            piglist = PigBase.objects.filter(stationid=req, decpigtime=None)
            stationpig = list()
            for s in piglist:
                s_info = dict()
                s_info['pigid'] = s.pigid
                s_info['earid'] = s.earid
                s_info['pigkind'] = s.pigkind
                onepigbreedtime = s.breedtime
                # print(onepigbreedtime)
                s_info['breeddays'] = caldate(onepigbreedtime)
                onepig = FoodQuantity.objects.get(pigid=s.pigid)
                s_info['backfat'] = is_none(onepig.backfat)
                s_info['index_quantity'] = onepig.index_quantity
                s_info['algo_quantity'] = is_none(onepig.algo_quantity)
                s_info['set_quantity'] = is_none(onepig.set_quantity)
                s_info['final_quantity'] = final(onepig.index_quantity, onepig.algo_quantity, onepig.set_quantity)
                stationpig.append(s_info)
        except Exception as e:
            print(e)
            stationpig = None
        return JsonResponse({'code': '获取intake成功', 'stationpig': stationpig}, status=200)

    def post(self, request):
        req = request.data
        req_pigid = req['pigid']
        req_backfat = req['backfat']  # 字符串
        print(req_pigid)
        print(type(req_backfat))
        change_pig = FoodQuantity.objects.get(pigid=req_pigid)
        change_pig.backfat = req['backfat']
        change_pig.algo_quantity = algo_backfat(float(req['backfat']))
        change_pig.save()
        return JsonResponse({'code': '成功'}, status=200)

    def put(self, request):
        req = request.data
        req_pigid = req['pigid']
        req_set_quantity = req['setnum']
        change_pig = FoodQuantity.objects.get(pigid=req_pigid)
        change_pig.set_quantity = req_set_quantity
        change_pig.save()
        return JsonResponse({'code': '成功'}, status=200)

    def delete(self, request):
        return JsonResponse({'code': '成功'}, status=200)

    def patch(self, request):
        return JsonResponse({'code': '成功'}, status=200)
