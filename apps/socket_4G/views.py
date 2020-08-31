import queue, socket, time, threading, pickle
from .Raspi_4G import Raspi_run
from .sync_stationinfo import sync_stationinfo

exit_flag = False
timer_cnt = 0



Raspi_run()
sync_stationinfo()
