# import pickle
#
# data = {
#     'a': [1, 2.0, 3, 4 + 6j],
#     'b': ("character string", b"byte string"),
#     'c': {None, True, False}
# }
# # print(data)
# with open('data_object.pickle', 'wb') as f:
#     pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
# try:
#     with open('data_object.pickle', 'rb') as f:
#
#         data = pickle.load(f)
# except:
#     data = {}
# print(data)
# a = '12312'
# b = {}
# print(type(a) == str)
# print(type(b) == dict)

import time
import requests
import json
baseURL = 'http://localhost:8000/'


msg = {
    "func": "intake",
    "stationid": "01020003",
    "earid": "999999999999",
    "food_intake": 100,
    "start_time": "190304050607",
    "end_time": "190304050607"
}

print(time.strftime("%Y-%m-%d %H:%M:%S",
                    time.strptime(msg['start_time'],
                                  "%Y%m%d%H%M%S")))

