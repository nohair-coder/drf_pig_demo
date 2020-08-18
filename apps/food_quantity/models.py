from django.db import models
from apps.pigbase.models import PigBase
import datetime


# Create your models here.

class FoodQuantity(models.Model):
    now_time = datetime.datetime.now().strftime('%F')
    pigid = models.OneToOneField(PigBase, to_field='pigid', verbose_name='身份码', on_delete=models.CASCADE)
    backfat = models.FloatField(null=True, verbose_name='背膘厚')
    index_quantity = models.FloatField(verbose_name='默认饲喂量', default=1)
    algo_quantity = models.FloatField(verbose_name='计算饲喂量', null=True)
    set_quantity = models.FloatField(verbose_name='设置饲喂量', null=True)
    settime = models.DateField(default=now_time, verbose_name='设置日期')

    class Meta:
        db_table = 'tb_foodquantity'  # 指明数据库表名
        verbose_name = '饲喂量'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称


class Backfat(models.Model):
    now_time = datetime.datetime.now().strftime('%F')
    pigid = models.ForeignKey(PigBase,
                              to_field='pigid',
                              verbose_name='身份码',
                              on_delete=models.CASCADE)
    backfat = models.FloatField(null=True, verbose_name='背膘厚')
    settime = models.DateField(default=now_time, verbose_name='设置日期')

    class Meta:
        db_table = 'tb_backfat'  # 指明数据库表名
        verbose_name = '背膘厚'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称
