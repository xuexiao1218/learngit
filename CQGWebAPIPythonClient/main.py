import websocket
from webapi_1_pb2 import *
import time
import threading,queue
from webapi_CQGTrader import *

host_name = 'wss://demoapi.cqg.com:443'
info = 'CapitalCC pass WebApiTest python-client'
metadata_cond = '1 1 QFAH6'
position_cond = '1 16873141 1'

user = CQGTrader()
user.ApiLogin(host_name)
user.UserLogin(info)

#user.Send('position',position_cond)
user.Send('metadata',metadata_cond)
user.Send('position',position_cond)

while 1:
 #user.Recv('position')
 user.Recv('metadata')
 user.Recv('position')
