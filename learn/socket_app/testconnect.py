# coding: utf8
# '本地端，连接 C 端'

from socket import *
import json
from learn.socket_app import asyncFunc, write_stationinfo, write_piginfo

# socket_host = 'localhost'
socket_host = '192.168.0.107'
# socket_port = 10000
socket_port = 9999
BUFSIZE = 4096


# 创建socket  tcp协议
client_socket = socket(AF_INET, SOCK_STREAM)

# 连接服务器
serAddr = (socket_host, socket_port)
client_socket.connect(serAddr)

# 超时时间60秒，在处于监听状态下，超时之后，会报错，被捕捉，关闭连接
# client_socket.settimeout(3)

print('before--')

@asyncFunc
def send_message(msg):
    try:
        client_socket.send(msg)
    except Exception as e:
        print('<<<----- send_message error  ----->>>')
        print(e)



while True:
    try:
        print('yes')
        send_message(json.dumps({
            '_type': 4,
            'machineId': 123456789012,
            'operation': 1,
        }).encode('utf8'))

        raw_receive = client_socket.recv(BUFSIZE)
        if len(raw_receive) > 0:
            recv = json.loads(raw_receive)
            print('--------')
            print(recv)
            print('--------')
            # 接收到种猪信息
            if recv.get('_type') == 1:
                # 种猪信息
                res = write_piginfo(recv)
                res['_type'] = recv.get('_type')
                print('----  res1  -----')
                send_message(json.dumps(res).encode('utf8'))
            elif recv.get('_type') == 2:
                # 测定站工作状态 2
                res = write_stationinfo(recv)
                res['_type'] = recv.get('_type')
                print('----  res2  -----')
                send_message(json.dumps(res).encode('utf8'))
            elif recv.get('_type') == 3:
                # 测定站与 USBCAN 连接状态 3
                pass


    except Exception as e:
        print('<<<-----  err  ------>>>')
        print(e)
        break
