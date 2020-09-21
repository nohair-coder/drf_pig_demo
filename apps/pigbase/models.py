from django.db import models
from apps.station.models import StationInfo


# Create your models here.
class PigBase(models.Model):
    stationid = models.ForeignKey(StationInfo,
                                  to_field='build_unit_station',
                                  on_delete=models.CASCADE,
                                  verbose_name='饲喂站号')
    pigid = models.CharField(max_length=16, unique=True, verbose_name='身份码')
    earid = models.CharField(max_length=16, verbose_name='耳标号')
    pigkind = models.CharField(max_length=20, verbose_name='品种', null=True)
    malepignum = models.CharField(max_length=20, verbose_name='与配公猪号')
    gesage = models.FloatField(default=0, verbose_name='胎龄')
    # vaccine = models.CharField(max_length=64, verbose_name='疫苗情况')
    addpigtime = models.DateField(auto_now_add=True, verbose_name='入栏日期')
    breedtime = models.CharField(max_length=16, verbose_name='配种日期')
    decpigtime = models.DateField(max_length=10, null=True, verbose_name='出栏日期')

    class Meta:
        db_table = 'tb_pigbase'  # 指明数据库表名
        verbose_name = '动物基础表'  # 在admin站点中显示的名称
        # verbose_name_plural = verbose_name  # 显示的复数名称

    # def __str__(self):
    #     """定义每个数据对象的显示信息"""
    #     return self.stationid
