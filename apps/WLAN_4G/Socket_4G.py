# coding: utf8
import queue, socket, time, threading, pickle, socketserver
from ..WLAN_4G import Analysis_4G
from .models import Message, Message_4G
from .Httpsend import dataPost, devicePost, devicePut

exit_flag = False
timer_cnt = 0
udp_server = 0


class MySocket(socketserver.BaseRequestHandler):

    def handle(self):
        global udp_server
        try:
            data = self.request[0].decode()
            Addr_4G = self.client_address
            udp_server = self.request[1]
            if (data[0] == '$' and data[12] == '#' and len(data) == 13) or (data[0] == '{' and data[-1] == '}'):
                Analysis_4G.Recv_4G_Queue.put([data, Addr_4G])
            else:
                print('error Recv')
        except Exception as e:
            print(e)
            print(self.request[0].decode(), self.client_address)


def Init_4GSocket():
    """4G Socket 初始化"""
    Send_4G_Thread = threading.Thread(target=Send_4G)
    Send_4G_Thread.start()
    server = socketserver.ThreadingUDPServer(('127.0.0.1', 7788), MySocket)
    server.serve_forever()


def Send_4G():
    """4G发送"""
    print(threading.current_thread().name, 'Send_4G is running...')
    while not exit_flag:
        send_msg = Analysis_4G.Send_4G_Queue.get(block=True)
        data = send_msg[0].encode()
        udp_server.sendto(data, send_msg[1])


def Handle_4G():
    """处理命令"""
    print(threading.current_thread().name + 'running...')
    while not exit_flag:
        msg_addr = Analysis_4G.Recv_4G_Queue.get()
        msg = msg_addr[0]
        Addr_4G = msg_addr[1]
        if msg is not None:
            if msg[0] == '$' and msg[12] == '#' and len(msg) == 13:
                data = Analysis_4G.getFunctionCode(msg)
                func_code = data['func_code']
                if func_code == Analysis_4G.FUN_CODE_DICT['heart_beat']:  # 00 心跳
                    Analysis_4G.network_management(msg, Addr_4G)
                # elif data['func_code'] == Analysis_4G.FUN_CODE_DICT['close_device']:  # 01 关机
                #     pass
                # elif data['func_code'] == Analysis_4G.FUN_CODE_DICT['open_device']:  # 02 开机
                #     pass
                elif func_code == Analysis_4G.FUN_CODE_DICT['data_object_request']:  # 03开始接收数据
                    Analysis_4G.promiseRequest(msg, Addr_4G)
                elif data['func_code'] == Analysis_4G.FUN_CODE_DICT['send_complete']:  # 05 接收数据完成
                    Analysis_4G.closePromiseRequest(msg, Addr_4G)
                elif func_code == Analysis_4G.FUN_CODE_DICT['sync_data_request']:  # 06 请求同步数据
                    pass
                else:
                    print('Node', Analysis_4G.getFunctionCode(msg)['func_code'], ' can not identify !')
            else:
                data_obj = Analysis_4G.dataAnalyse(eval(msg))
                if data_obj != {}:
                    with open('data_object.pickle', 'wb') as f:
                        # Pickle the 'data' dictionary using the highest protocol available.
                        pickle.dump(data_obj, f, pickle.HIGHEST_PROTOCOL)
                else:
                    print('data_obj is null')


def serverSend():
    """上传数据"""
    print(threading.current_thread().name, 'serverSend is running...')
    while not exit_flag:
        try:
            data_obj = Analysis_4G.serverSendQueue.get(timeout=3)
            if not dataPost(data_obj):
                Analysis_4G.serverSendQueue.put(data_obj)
            time.sleep(0.1)
        except:
            pass


def timer():
    """定时任务"""
    global timer_cnt
    if not exit_flag:
        timer_thread = threading.Timer(0.01, timer)
        timer_thread.start()
        timer_cnt += 1
        if timer_cnt > 0xffffffff:
            timer_cnt = 0
        if timer_cnt % 1000 == 1:
            Analysis_4G.nodeMonitor()
        if timer_cnt % 100 == 1:
            Analysis_4G.timeoutHandler()


def Socket_4G_run():
    Analysis_4G.sysInit()
    print("4Gsys init")
    socket_4G_thread = threading.Thread(target=Init_4GSocket)
    socket_4G_thread.start()
    Hand4GThread = threading.Thread(target=Handle_4G)
    Hand4GThread.start()
    serverSendThread = threading.Thread(target=serverSend)
    serverSendThread.start()
    timer()


def setDeviceStatus(cmd):
    """设定测定站状态，[[nodeId,"open_device"],[nodeId,"close_device"]]"""
    try:
        for i in cmd:
            Analysis_4G.deviceStart(int(i[0]), i[1])
        return True
    except Exception as e:
        print(e)
        return False


def getDeviceStatus(nodeId):
    """获得测定站状态,返回["ON","00000"]获取一个"""
    try:
        not_exit_station_statue = {
            'work_status': 'OFF'
        }

        status = Analysis_4G.device_status.get(str(int(nodeId)), not_exit_station_statue)

        if status['work_status'] == 'OFF':
            res = ['OFF', '00000']
        elif status['work_status'] == 'ON':
            res = ['ON', '00000']
        else:
            res = ['ON', status['work_status']]
        return res
    except Exception as e:
        print('获取测定站状态失败 ----------------->>>')
        print(e)
        return False
