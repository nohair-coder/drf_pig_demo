# coding: utf8
import queue, socket, time, threading, pickle
from ..socket_4G import Analysis_4G
from .models import Message
from .logic import dataPost, devicePost, devicePut

exit_flag = False
timer_cnt = 0


def Init_4GSocket():
    """4G Socket 初始化"""
    global socket_server, Addr_4G
    port = 9999
    host = '192.168.0.107'
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 开启UDP
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(('8.8.8.8', 80))
    # print('sock   address      ---->', (s.getsockname()[0], port))
    socket_server.bind((host, port))
    # s.close()
    data, Addr_4G = socket_server.recvfrom(1024)
    print('4G connected', Addr_4G)
    Recv_4G_Thread = threading.Thread(target=Recv_4G, args=(socket_server, Addr_4G))
    Send_4G_Thread = threading.Thread(target=Send_4G, args=(socket_server, Addr_4G))
    Recv_4G_Thread.start()
    Send_4G_Thread.start()
    Recv_4G_Thread.join()
    Send_4G_Thread.join()
    socket_server.close()


def Send_4G(socket_server, Addr_4G):
    '4G发送'
    print(threading.current_thread().name, 'CANSend is running...')
    databyte = bytearray()
    while exit_flag != True:
        msg = Analysis_4G.Send_4G_Queue.get(block=True)
        print("Send:", msg, " to ", Addr_4G)
        databyte = msg.msg2byte()
        socket_server.sendto(databyte, Addr_4G)


def Recv_4G(socket_server, Addr_4G):
    '4G接收'
    print(threading.current_thread().name, 'CANRecv is running...')
    while exit_flag != True:
        try:
            data = socket_server.recv(4096)
            Analysis_4G.Recv_4G_Queue.put(data)
            # databyte = socket_server.recv(13 * 50)
            # if len(databyte) % 13 == 0:
            #     for i in range(len(databyte) // 13):
            #         msg = Message()
            #         msg.byte2msg(databyte[i * 13:i * 13 + 13])
            #         if msg.arbitration_id != 0:
            #             print(msg)
            #             Analysis_4G.Recv_4G_Queue.put(msg)
            #         else:
            #             print("Recvive 0 error")
            # else:
            #     print('err Recv')
        except TimeoutError:
            print('can disconnect')


def Handle_4G():
    """CAN处理"""
    print(threading.current_thread().name + 'running...')
    while exit_flag != True:
        msg = Analysis_4G.Recv_4G_Queue.get()
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
    print(123)
    with open('data_object.pickle', 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        serverSendQueue = pickle.load(f)
except:
    serverSendQueue = queue.Queue()

# @asyncFunc
# def CANCommunication():
#     'CAN模块，阻塞型'
#     try:
#         print('before init')
#         CAN_Analysis.sysInit()
#         print("sys init")
#         CANSocketThread=threading.Thread(target=CANSocket)
#         CANSocketThread.start()
#         CANHandThread=threading.Thread(target=CANHand)
#         CANHandThread.start()
#         serverSendThread=threading.Thread(target=serverSend)
#         serverSendThread.start()

#         timer()
#         while(True) :
#             cmd=input ('Press enter to exit...\n')
#             if cmd == 'open' :
#                 CAN_Analysis.deviceStart(9,'open_device')
#             elif cmd == 'close' :
#                 CAN_Analysis.deviceStart(9,'close_device')
#             elif cmd == 'test' :
#                 CAN_Analysis.deviceStart(9,'test_device')
#             elif cmd == 'train' :
#                 CAN_Analysis.deviceStart(9,'train_device')
#             elif cmd == 'exit' :
#                 print('exit system ...')
#                 break
#         CANHandThread.join()
#         CANSocketThread.join()
#         serverSendThread.join()
#         time.sleep(3+1)
#         exit()
#     except:
#         return False
def Raspi_run():
    print('start')
    Analysis_4G.sysInit()
    print("4Gsys init")
    CANSocketThread = threading.Thread(target=Init_4GSocket)
    CANSocketThread.start()
    CANHandThread = threading.Thread(target=Handle_4G)
    CANHandThread.start()
    serverSendThread = threading.Thread(target=serverSend)
    serverSendThread.start()
    timer()



def setDeviceStatus(cmd):
    '设定测定站状态，[[nodeId,"open_device"],[nodeId,"close_device"]]'
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
