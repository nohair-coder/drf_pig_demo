from .models import PigBase
from ..food_quantity.models import FoodQuantity
from .logic import write_pigbase, write_backfat, write_foodquantity, delete_pigbase
from ..common.input_check import is_none
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
import json
import datetime


# Create your views here.
class PigBaseCheck(View):
    def post(self, request):
        """
        入栏
        :param request:
        :return:
        """
        try:
            req = json.loads(request.body)
            print(req)
            # print(req['BackFat']=='')
            exist_pigid = PigBase.objects.filter(
                Q(pigid=req['PigId']) & Q(decpigtime=None))

            exist_earid = PigBase.objects.filter(
                Q(stationid=req['Build_Unit_StationId']) & Q(earid=req['EarId']) & Q(decpigtime=None))

            if exist_pigid:
                return JsonResponse({'code': '该母猪号已存在，请检查输入'}, status=201)
            elif exist_earid:
                return JsonResponse({'code': '该栏中耳标号已存在，请选择其它耳标'}, status=201)
            else:
                write_pigbase(req)
                write_backfat(req)
                write_foodquantity(req)
                return JsonResponse({'code': '入栏成功'}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'code': '入栏失败'}, status=201)

    def get(self, request):
        """
        获取pigbase猪只
        :param request:
        :return:
        """
        try:
            req = request.GET['StationId']
            # print(req)
            piglist = PigBase.objects.filter(stationid=req, decpigtime=None)
            stationpig = list()
            for s in piglist:
                s_info = dict()
                s_info['stationid'] = s.stationid.build_unit_station
                s_info['pigid'] = s.pigid
                s_info['earid'] = s.earid
                s_info['pigkind'] = s.pigkind
                s_info['malepignum'] = s.malepignum
                s_info['backfat'] = is_none(FoodQuantity.objects.get(pigid=s.pigid).backfat)
                s_info['gesage'] = s.gesage
                s_info['breedtime'] = s.breedtime
                stationpig.append(s_info)
            # print(stationpig)
            return JsonResponse({'code': '获取pigbase成功', 'stationpig': stationpig}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'code': '获取pigbase失败'}, status=201)

    def put(self, request):
        """
        更换新饲喂站
        :param request:
        :return:
        """
        req = json.loads(request.body)
        print(req)
        req_pigid = req['pigid']
        req_newstation = req['newstation']
        change_pig = PigBase.objects.get(pigid=req_pigid)
        change_pig.stationid = req_newstation
        change_pig.save()
        return JsonResponse({'code': '转栏成功'}, status=200)

    def delete(self, request):
        """
        离栏，并写入日志
        :param request:
        :return:
        """
        now_time = datetime.datetime.now().strftime('%F')
        req = json.loads(request.body)
        req_pigid = req['pigid']
        # print(req_pigid)
        delete_pigbase(req_pigid)
        return JsonResponse({'code': '离栏成功'}, status=200)

    def patch(self, request):
        """
        更换耳标号
        :param request:
        :return:
        """
        req = json.loads(request.body)
        req_pigid = req['pigid']
        req_newearid = req['newearid']
        print(req_pigid)
        print(req_newearid)
        change_pig = PigBase.objects.get(pigid=req_pigid)
        change_pig.earid = req_newearid
        change_pig.save()
        return JsonResponse({'code': '更换成功'}, status=200)


def UploadPig(request):
    """
    上传excel一键入栏
    :param request:
    :return:
    """
    import openpyxl
    if request.method == 'POST':
        try:
            req = request.FILES.getlist('file')[0]
            workbook = openpyxl.load_workbook(req)
            ws = workbook.worksheets[0]
            for row in ws.rows:
                print([item.value for item in row])
            error_list = [123, 324, 123]
            return JsonResponse({'code': '接收文件成功', 'error_list': error_list}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'code': '接收文件失败'}, status=201)
    else:
        print(321)
        return JsonResponse({'code': '不是POST'}, status=201)
