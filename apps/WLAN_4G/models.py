import logging
import struct
import time
# Create your models here.


logger = logging.getLogger(__name__)


class Message(object):

    def __init__(self,
                 is_remote_frame=False,  # 远程帧
                 extended_id=True,  # 扩展帧
                 is_error_frame=False,  # 错误帧
                 arbitration_id=0,
                 dlc=None,  # 数据长度
                 data=None,  # 数据
                 is_fd=False,
                 bitrate_switch=False,  # 波特率选择
                 error_state_indicator=False,
                 channel=None):

        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.id_type = extended_id
        self.is_extended_id = extended_id

        self.is_remote_frame = is_remote_frame
        self.is_error_frame = is_error_frame
        self.arbitration_id = arbitration_id
        self.channel = channel

        self.is_fd = is_fd
        self.bitrate_switch = bitrate_switch
        self.error_state_indicator = error_state_indicator

        if data is None or is_remote_frame:
            self.data = bytearray(8)
        elif isinstance(data, bytearray):
            self.data = data
        else:
            try:
                self.data = bytearray(data)
            except TypeError:
                err = "Couldn't create message from {} ({})".format(data, type(data))
                raise TypeError(err)

        if dlc is None:
            self.dlc = len(self.data)
        else:
            self.dlc = dlc

        if is_fd and self.dlc > 64:
            logger.warning("data link count was %d but it should be less than or equal to 64", self.dlc)
        if not is_fd and self.dlc > 8:
            logger.warning("data link count was %d but it should be less than or equal to 8", self.dlc)

    def __str__(self):
        field_strings = ["Timestamp: {}".format(self.timestamp)]  # 输出格式化的时间
        if self.id_type:
            # Extended arbitrationID
            arbitration_id_string = "ID: {0:08x}".format(self.arbitration_id)
        else:
            arbitration_id_string = "ID: {0:04x}".format(self.arbitration_id)
        field_strings.append(arbitration_id_string.rjust(12, " "))

        flag_string = " ".join([
            "X" if self.id_type else "S",
            "E" if self.is_error_frame else " ",
            "R" if self.is_remote_frame else " ",
            "F" if self.is_fd else " ",
        ])

        field_strings.append(flag_string)

        field_strings.append("DLC: {0:d}".format(self.dlc))
        data_strings = []
        if self.data is not None:
            for index in range(0, min(self.dlc, len(self.data))):
                data_strings.append("{0:02x}".format(self.data[index]))
        if data_strings:  # if not empty
            field_strings.append(" ".join(data_strings).ljust(24, " "))
        else:
            field_strings.append(" " * 24)

        if (self.data is not None) and (self.data.isalnum()):
            try:
                field_strings.append("'{}'".format(self.data.decode('utf-8')))
            except UnicodeError:
                pass

        return "    ".join(field_strings).strip()

    def __len__(self):
        return len(self.data)

    def __bool__(self):
        return True

    def __nonzero__(self):
        return self.__bool__()

    def __repr__(self):
        data = ["{:#02x}".format(byte) for byte in self.data]
        args = ["timestamp={}".format(self.timestamp),
                "is_remote_frame={}".format(self.is_remote_frame),
                "extended_id={}".format(self.id_type),
                "is_error_frame={}".format(self.is_error_frame),
                "arbitration_id={:#x}".format(self.arbitration_id),
                "dlc={}".format(self.dlc),
                "data=[{}]".format(", ".join(data))]
        if self.channel is not None:
            args.append("channel={!r}".format(self.channel))
        if self.is_fd:
            args.append("is_fd=True")
            args.append("bitrate_switch={}".format(self.bitrate_switch))
            args.append("error_state_indicator={}".format(self.error_state_indicator))
        return "can.Message({})".format(", ".join(args))

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.arbitration_id == other.arbitration_id and
                # self.timestamp == other.timestamp and # allow the timestamp to differ
                self.id_type == other.id_type and
                self.dlc == other.dlc and
                self.data == other.data and
                self.is_remote_frame == other.is_remote_frame and
                self.is_error_frame == other.is_error_frame and
                self.is_fd == other.is_fd and
                self.bitrate_switch == other.bitrate_switch)

    def __hash__(self):
        return hash((
            self.arbitration_id,
            # self.timestamp # excluded, like in self.__eq__(self, other)
            self.id_type,
            self.dlc,
            self.data,
            self.is_fd,
            self.bitrate_switch,
            self.is_remote_frame,
            self.is_error_frame
        ))

    def __format__(self, format_spec):
        return self.__str__()

    def msg2byte(self):
        """消息转字节"""
        databyte = bytearray(13)
        databyte[0] = self.is_extended_id << 7 | self.is_remote_frame << 6 | self.dlc
        databyte[4:0:-1] = struct.pack('i', self.arbitration_id)
        databyte[5:13] = self.data
        return databyte

    def byte2msg(self, databyte):
        """字节转消息"""
        # print(list(databyte))
        self.arbitration_id = struct.unpack('i', databyte[4:0:-1])[0]
        self.dlc = databyte[0] & 0x0f
        self.data = databyte[5:5 + self.dlc]
        self.timestamp = time.time()
        if databyte[0] & 0x80 == 0x80:
            self.id_type = True
            self.is_extended_id = True
        else:
            self.id_type = False
            self.is_extended_id = False
        if databyte[0] & 0x40 == 0x40:
            self.is_remote_frame = True
        else:
            self.is_remote_frame = False


class Message_4G(object):

    def __init__(self,
                 msg_length=None,   # 信息长度
                 data=None,         # 信息体，json格式
                 msg_start=None,
                 msg_end=None,
                 station_id=None,
                 station_status=None,
                 func_code=None):

        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 格式化当前时间
        self.msg_start = msg_start
        self.msg_end = msg_end
        self.station_id = station_id
        self.station_status = station_status
        self.func_code = func_code

        if data is None:
            self.data = bytearray(8)
        elif isinstance(data, bytearray):
            self.data = data
        else:
            try:
                self.data = bytearray(data)
            except TypeError:
                err = "Couldn't create message from {} ({})".format(data, type(data))
                raise TypeError(err)

        if msg_length is None:
            self.msg_length = len(self.data)
        else:
            self.msg_length = msg_length



    def msg_to_byte(self):
        """消息转字节"""
        databyte = bytearray(13)
        databyte[0] = self.is_extended_id << 7 | self.is_remote_frame << 6 | self.msg_length
        databyte[4:0:-1] = struct.pack('i', self.arbitration_id)
        databyte[5:13] = self.data
        return databyte

    def byte_to_msg(self, databyte):
        """字节转消息"""
        # print(list(databyte))
        self.msg_start = databyte[0]
        self.station_id = databyte[1:10]
        self.station_status = databyte[10]
        self.func_code = databyte[11:13]
        self.msg_end = databyte[13]

