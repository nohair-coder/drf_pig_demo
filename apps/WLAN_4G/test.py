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

now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(now_time)
