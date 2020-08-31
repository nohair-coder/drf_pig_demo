# coding: utf8
import queue, socket, time, threading, pickle
from ..socket_4G import Analysis_4G
from .models import Message, Message_4G
from .logic import dataPost, devicePost, devicePut

exit_flag = False
timer_cnt = 0


def Init_4GSocket():
    """4G Socket 初始化"""
    global socket_server, Addr_4G
    port = 9999
    host = '192.168.0.107'
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 开启UDP
    socket_server.bind((host, port))
    while True:
        data, Addr_4G = socket_server.recvfrom(4096)
        print('4G connected', Addr_4G)
        # print(socket_server.recvfrom(1024))
        Recv_4G_Thread = threading.Thread(target=Recv_4G, args=(socket_server, Addr_4G))
        # Send_4G_Thread = threading.Thread(target=Send_4G, args=(socket_server, Addr_4G))
        Recv_4G_Thread.start()
        # Send_4G_Thread.start()
        # Send_4G_Thread.join()

    socket_server.close()


def Send_4G(socket_server, Addr_4G):
    """4G发送"""
    print(threading.current_thread().name, 'Send_4G is running...')
    while exit_flag != True:
        msg = Analysis_4G.Send_4G_Queue.get(block=True)
        print("Send:", msg, " to ", Addr_4G)
        data = msg.msg2byte()
        socket_server.sendto(data, Addr_4G)


def Recv_4G(socket_server, Addr_4G):
    '4G接收'
    print(threading.current_thread().name, 'Recv_4G is running...')
    # data形如'$01020003100#'
    while exit_flag != True:
        try:
            databyte = socket_server.recv(1024)
            if len(databyte) == 13:
                msg = Message_4G()
                msg.byte_to_msg(databyte)
                if msg.msg_start == '$' and msg.msg_end == '#':
                    if msg.func_code == '05':
                        print('发送数据完成')
                        break
                    else:
                        print('正在接收数据')
                        Analysis_4G.Recv_4G_Queue.put(msg)
                else:
                    print("Recvive 0 error")
            elif type(databyte) == dict:
                print('接收到数据')
                pass
            else:
                print('err Recv')
        except TimeoutError:
            print('can disconnect')


def Handle_4G():
    """CAN处理"""
    print(threading.current_thread().name + 'running...')
    while exit_flag != True:
        msg = Analysis_4G.Recv_4G_Queue.get()
        # print(msg)
        if msg != None:
            print(msg)
            # if msg.is_remote_frame == True:  # 如果是远程帧
            #     func_code = Analysis_4G.getFunctionCode(msg)  # 获取功能码
            #     if (msg.arbitration_id == 0x0ff):
            #         pass
            #     elif func_code == Analysis_4G.FUN_CODE_DICT['time_stamp_request']:
            #         Analysis_4G.syncTime(msg)
            #     elif func_code == Analysis_4G.FUN_CODE_DICT['heart_beat']:
            #         Analysis_4G.network_management(msg)
            #         # print('heart_beat',msg)
            #     elif func_code == Analysis_4G.FUN_CODE_DICT['data_object_request']:
            #         Analysis_4G.promiseRequest(msg)
            #         # print('data_object_request',msg)
            #     else:
            #         print('Node', Analysis_4G.getFunctionCode(msg), ' can not identify !')
            # else:
            #     data_obj = Analysis_4G.dataAnalyse(msg)
            #     if data_obj != None and data_obj != {}:
            #         serverSendQueue.put(data_obj)
            #         with open('data_object.pickle', 'wb') as f:
            #             pickle.dump(data_obj, f, pickle.HIGHEST_PROTOCOL)


def serverSend():
    '上传数据'
    print(threading.current_thread().name, 'serverSend is running...')
    while exit_flag != True:
        data_obj = {}
        try:
            data_obj = serverSendQueue.get(timeout=3)
            if dataPost(data_obj) != True:
                serverSendQueue.put(data_obj)
            time.sleep(0.1)
        except:
            pass


def timer():
    '定时任务'
    global timer_cnt
    if exit_flag != True:
        timerThread = threading.Timer(0.01, timer)
        timerThread.start()
        timer_cnt += 1
        if timer_cnt > 0xffffffff:
            timer_cnt = 0
        if (timer_cnt % 1000 == 1):
            Analysis_4G.nodeMonitor()
        if (timer_cnt % 5 == 1):
            Analysis_4G.timeoutHandler()


try:
    with open('data_object.pickle', 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        serverSendQueue = pickle.load(f)
except:
    serverSendQueue = queue.Queue()


def Raspi_run():
    Analysis_4G.sysInit()
    print("4Gsys init")
    Socket4GThread = threading.Thread(target=Init_4GSocket)
    Socket4GThread.start()
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
