from apps.food_quantity.models import FoodQuantity
import datetime

def is_none(parm):
    """
    参数parm是不是 None，是就返回 '—'
    :param backfat:
    :return:
    """
    return parm if parm is not None else '—'


def caldate(date1):
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