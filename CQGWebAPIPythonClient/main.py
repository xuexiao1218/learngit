import websocket
from webapi_1_pb2 import *
import time
import threading,queue
from webapi_CQGTrader import *

host_name = 'wss://demoapi.cqg.com:443'
info = 'CapitalCC pass WebApiTest python-client'

user = CQGTrader()
user.ApiLogin(host_name)
user.UserLogin(info)

#user.Send('position',position_cond)
#user.Send('metadata',metadata_cond)
user.Send()
user.Send()

"""
recv_tp = input('receive metadata or position?\n')
while 1:
 user.Recv(recv_tp)
"""
t2 = threading.Thread(target=user.Recv,args=('metadata',))
t3 = threading.Thread(target=user.Recv,args=('position',))
t2.start()
t3.start()
