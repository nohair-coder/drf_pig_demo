# coding: utf8
import requests
import json

baseURL = 'http://localhost:8000/'


def dataPost(json_object):
    """数据上传"""
    try:
        r = requests.post(baseURL+'intakedata/', json=json_object)
        # r = requests.post("http://httpbin.org/post", data=payload)
        ack = json.loads(r.text)
        if (ack['success'] != True):
            print('dataPost', ack)
            print('dataPost err', json_object)
            return False
        else:
            return True
    except:
        print('connect failed !')
        return False


def devicePost(json_object):
    """设备新增"""
    try:
        r = requests.post(baseURL+'stationinfo/', json=json_object)
        ack = json.loads(r.text)
        if (ack['success'] != True):
            print('devicePost', ack)
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
