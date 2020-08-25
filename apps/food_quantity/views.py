from .models import FoodQuantity
from apps.pigbase.models import PigBase
from django.http import JsonResponse
from rest_framework.views import APIView
from utils.jwt_token.jwt_auth import JwtAuthorizationAuthentication
import json
import datetime
from .logic import is_none


# Create your views here.


def Caldate(date1):
    '''
    计算两日期相隔天数
    :param date1: 妊娠日期
    :return:
    '''
    now_time = datetime.datetime.now().strftime('%F')
    # date1, date2均为string类型
    # %Y-%m-%d为日期格式，其中的-可以用其他代替或者不写，但是要统一，同理后面的时分秒也一样；可以只计算日期，不计算时间。
    # date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    # date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
    date1 = datetime.datetime.strptime(date1[0:10], "%Y-%m-%d")
    date2 = datetime.datetime.strptime(now_time, "%Y-%m-%d")
    return (date2 - date1).days + 1


def final(index, algo, set):
    if set is None:
        if algo is None:
            return index
        else:
            return algo
    else:
        return set


def algo_backfat(backfat):
    algo_intake = backfat * 2
    return algo_intake


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
                s_info['breeddays'] = Caldate(onepigbreedtime)
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
