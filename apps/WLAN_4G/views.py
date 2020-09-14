import queue, socket, time, threading, pickle
from .Socket_4G import Socket_4G_run
from .sync_stationinfo import sync_stationinfo

exit_flag = False
timer_cnt = 0


Socket_4G_run()
sync_stationinfo()
