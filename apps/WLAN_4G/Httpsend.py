# coding: utf8
import requests
import json
from ..WLAN_4G import Analysis_4G
baseURL = 'http://localhost:8000/'


def dataPost(json_object):
    """数据上传"""
    try:
        r = requests.post(baseURL+'intakedata/', json=json_object)
        # r = requests.post("http://httpbin.org/post", data=payload)
        ack = json.loads(r.text)
        if not ack['code']:
            print('dataPost', ack)
            print('dataPost err', json_object)
            return False
        else:
            return True
    except:
        print('dataPost failed !')
        return False


def devicePost(json_object):
    """设备新增"""
    try:
        r = requests.post(baseURL+'station/4G/', json=json_object)
        ack = json.loads(r.text)
        if ack['code'] != 'success':
            print('devicePost', ack['code'])
    except:
        print('connect failed !')
        return False


def devicePut(json_object):
    """设备状态修改"""
    try:
        r = requests.put(baseURL+'stationinfo/', json=json_object)
        ack = json.loads(r.text)
        if (ack['success'] != True):
            print('devicePut', ack)
    except:
        print('connect failed !')
        return False


def pigPost(json_object):
    """下位机母猪入栏"""
    try:
        r = requests.post(baseURL+'pigbase/4G/', json=json_object)
        ack = json.loads(r.text)
        if ack['code'] != 'success':
            print('pigPost', ack)
            print('pigPost err', json_object)
            return False
        else:
            return True
    except:
        print('pigPost failed !')
        return False
