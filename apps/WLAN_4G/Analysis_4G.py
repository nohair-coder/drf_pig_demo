# coding: utf8
import time, queue, json, threading, pickle
from .Httpsend import devicePut, devicePost, dataPost, pigPost
from .models import Message

FUN_CODE_DICT = {  # 功能码
    'heart_beat': 0,  # 心跳
    'close_device': 1,  # 关机  close_device
    'open_device': 2,  # 开机  open_device
    'data_object_request': 3,  # 请求发送json数据
    'recv_confirm': 4,  # 确认接收到命令
    'send_complete': 5,  # 发送数据完成
    'sync_data_request': 6,  # 请求同步数据
    'sync_data_complete': 7,  # 同步数据完成
}
DEVICE_STATUS_CODE = ['00001', 'OFF', 'ON', '00002', '00003', '00004', '00005', '00006', '00007', '00008']
device_status = {}  # 设备缓存
Send_4G_Queue = queue.Queue(32)
Recv_4G_Queue = queue.Queue(64)
dataRequestQueue = queue.Queue(32)

try:
    with open('data_object.txt', 'r') as f:
        text = f.read()
        # serverSendQueue = json.loads(text)
        serverSendQueue = queue.Queue()
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
except:
    serverSendQueue = queue.Queue()


def getFunctionCode(msg):
    """获取命令参数"""
    msg_start = msg[0]
    station_id = msg[1:9]
    station_status = msg[9]
    func_code = int(msg[10:12])
    msg_end = msg[12]
    code_dict = {
        'msg_start': msg_start,
        'msg_end': msg_end,
        'station_id': station_id,
        'station_status': station_status,
        'func_code': func_code,
    }
    return code_dict


def getWorkStatus(msg):
    """获取普通格式节点"""
    return int(msg[9])


def getNodeID(msg):
    """获取普通格式运行状态"""
    return msg[1:9]


def getJsonNodeID(msg):
    """获取json格式节点"""
    return msg['stationid']


def responseMsg(nodeid):
    id_ack = '$' + nodeid + '2' + '04' + '#'
    return id_ack


def syncTime(msg):
    """同步时间"""
    time_stamp_struct = list(time.localtime())  # 获取本地时间
    time_stamp_struct[0] -= 2000  # 将2019转换成19
    time_stamp_struct[6] = 0  # 星期转成0
    time_stamp_struct[7] = (time_stamp_struct[0] + time_stamp_struct[1] + time_stamp_struct[2] + time_stamp_struct[3] +
                            time_stamp_struct[4] + time_stamp_struct[5] + time_stamp_struct[6] + time_stamp_struct[
                                7]) & 0xff  # 和校验
    time_stamp_struct.pop()
    # Send_4G_Queue.put(
    #     Message(arbitration_id=msg.arbitration_id, data=time_stamp_struct))


def deviceStart(node_id, cmd):
    """上位机命令"""
    pass
    # if cmd == 'open_device':
    #     id_cmd = node_id | FUN_CODE_DICT['open_device'] << FUN_CODE_BIT
    # elif cmd == 'close_device':
    #     id_cmd = node_id | FUN_CODE_DICT['close_device'] << FUN_CODE_BIT
    # elif cmd == 'test_device':
    #     id_cmd = node_id | FUN_CODE_DICT['test_device'] << FUN_CODE_BIT
    # elif cmd == 'train_device':
    #     id_cmd = node_id | FUN_CODE_DICT['train_device'] << FUN_CODE_BIT
    # Send_4G_Queue.put(
    #     Message(arbitration_id=id_cmd, is_remote_frame=True))


def promiseRequest(msg, Addr_4G):
    """处理数据包发送请求"""
    global device_status
    node_id = getNodeID(msg)
    if node_id in device_status:  # 设备已运行然后接收到数据
        if device_status[node_id]['data_Receiving'] != 0:
            dataRequestQueue.put([msg, Addr_4G])  # 接收任务阻塞中，暂存队列
        elif device_status[node_id]['socket_status'] > 0:  # 等待时间不超过2秒，并且4G设备在线
            device_status[node_id]['data_Receiving'] = node_id  # 开始接收
            Send_4G_Queue.put([responseMsg(node_id), Addr_4G])
            device_status[node_id]['dog_count'] = 2
        else:
            print("Can't handle it", node_id)  # 超时不接收


def closePromiseRequest(msg, Addr_4G):
    """处理数据包发送完成请求"""
    global device_status
    node_id = getNodeID(msg)
    if node_id in device_status and device_status[node_id]['frame'] == [] and device_status[node_id][
        'frame_status'] == 0:  # 设备已运行然后接收到数据
        device_status[node_id]['data_Receiving'] = 0
        Send_4G_Queue.put([responseMsg(node_id), Addr_4G])


# {
#     "func": "intake",
#     "stationid": "01010001",
#     "earid": "999999999999",
#     "food_intake": 100,
#     "start_time": "190304050607",
#     "end_time": "190304050607"
# }


def dataAnalyse(msg):
    """数据包解析"""
    data_object = {}
    global device_status
    node_id = getJsonNodeID(msg)  # 获得节点ID
    if True:
        # if device_status[node_id]['data_Receiving'] == node_id and device_status[node_id]['data_Receiving'] != 0:
        # 处于接收态 device_status[node_id]['frame'].append(msg)  # 记录数据 device_status[node_id]['frame_status'] += 1  # 帧计数
        device_status[node_id]['dog_count'] = 2  # 超时标志清除
        try:
            func = msg['func']
            if func == 'intake':
                data_object['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                          time.strptime(msg['start_time'],
                                                                        "%Y%m%d%H%M%S"))
                data_object['end_time'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                        time.strptime(msg['end_time'], "%Y%m%d%H%M%S"))
                data_object['stationid'] = node_id  # 8位
                data_object['food_intake'] = msg['food_intake']
                data_object['earid'] = msg['earid']  # 8位
                serverSendQueue.put(data_object)
            elif func == 'addpig':
                data_object['stationid'] = msg['stationid']  # 饲喂站号
                data_object['earid'] = msg['earid']  # 耳标号
                data_object['breedtime'] = msg['mating_date']  # 配种日期
                data_object['gesage'] = msg['parity']  # 胎龄
                data_object['backfat'] = msg['backfat']  # 背膘厚
                pigPost(data_object)
            elif func == 'changestation':
                pass
            elif func == 'asyncdata':
                pass
            elif func == 'changedata':
                pass
            else:
                print(func + 'dataAnalyse error')
                data_object = {}
        except Exception as e:
            print('dataAnalyseError')
            print(e)
            data_object = {}
    if data_object != {}:
        device_status[node_id]['data_Receiving'] = 0
        Send_4G_Queue.put([responseMsg(node_id), device_status[node_id]['addr']])
        with open('data_object.txt', 'w') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            f.write(json.dumps(data_object))
    else:
        print('data_obj is null')


def clearTemp(node_id):
    """解除接收态"""
    device_status[node_id]['frame'] = []
    device_status[node_id]['frame_status'] = 0
    device_status[node_id]['data_Receiving'] = 0
    if dataRequestQueue.empty() == False:
        msg = dataRequestQueue.get()
        promiseRequest(msg[0], msg[1])


def timeoutHandler():
    """接收超时处理"""
    for i in device_status:
        if device_status[i]['data_Receiving'] != 0:  # 正在接收中
            device_status[i]['dog_count'] -= 1
            if device_status[i]['dog_count'] < 0:
                clearTemp(i)


def network_management(msg, Addr_4G):
    """节点状态"""
    global device_status
    node_id = getNodeID(msg)
    if node_id not in device_status:  # 新建一个设备缓存
        device_status[node_id] = {"frame": [],  # 缓存记录数据
                                  'frame_status': 0,  # 缓存帧计数
                                  "socket_status": 0,  # 网络通信状态
                                  "work_status": 0,  # 饲喂站工作状态
                                  "put_status": 0,  # 服务端饲喂站状态
                                  'data_Receiving': 0,  # 饲喂站接收数据状态
                                  'dog_count': 0,   # 超时计数
                                  'addr': 0  # ip地址
                                  }
        jsonobject = {
            'stationid': node_id,
            'comment': '',
            'status': 'off',
            'errorcode': '00000',
        }
        devicePost(jsonobject)  # 上传新建的设备状态
    device_status[node_id]['work_status'] = DEVICE_STATUS_CODE[getWorkStatus(msg)]
    device_status[node_id]['socket_status'] = 2
    device_status[node_id]['addr'] = Addr_4G
    Send_4G_Queue.put(
        [msg, device_status[node_id]['addr']]
    )


def nodeMonitor():
    """节点监控定时函数"""
    # 此函数由定时任务调用
    global device_status
    for i in device_status:
        # print(i,'asdsadsadsad')
        if device_status[i]['socket_status'] > 0:  # 设备在线i
            device_status[i]['socket_status'] -= 1
        elif i != '255':  # 设备断线
            device_status[i]['work_status'] = DEVICE_STATUS_CODE[9]
        if device_status[i]['work_status'] != device_status[i]['put_status']:  # 本地状态和服务器状态不一致
            json_object = {
                'stationid': str(i),
                'comment': '',
                'errorcode': '00000'
            }
            if device_status[i]['work_status'] == 'OFF':
                json_object['status'] = 'off'
            elif device_status[i]['work_status'] == 'ON':
                json_object['status'] = 'on'
            else:
                json_object['status'] = 'on'
                json_object['errorcode'] = device_status[i]['work_status']
            # devicePut(json_object)  # 修改服务器记录
            device_status[i]['put_status'] = device_status[i]['work_status']
    with open('sys_info.txt', 'w') as fou:
        fou.write(json.dumps(device_status))
    print("device_status:", device_status)


def Analysis_sysInit():
    """设备状态初始化"""
    global device_status
    with open('sys_info.txt', 'r') as fin:
        try:
            text = fin.read()
            # print(text)
            device_status = json.loads(text)
        except json.decoder.JSONDecodeError:
            print('sys_info create')
    for i in device_status:
        device_status[i] = {"frame": [], 'frame_status': 0, "can_status": 0, "work_status": 0, "put_status": 0}
