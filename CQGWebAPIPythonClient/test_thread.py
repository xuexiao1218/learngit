from webapi_1_pb2 import *
from webapi_CQGTrader_thread import *
from recvQueue import *
from config import *
import threading
import queue

host_name = 'wss://demoapi.cqg.com:443'
info =  'CapitalCC pass WebApiTest python-client'
list = 'metadata position'
metadata_cond = '1 1 QFAH6'
trade_sub_cond = '1 16873141 1'

user = CQGTrader()
user.ApiLogin(host_name)
user.UserLogin(info)
user.UserMetadataSubscription(metadata_cond)#元数据订阅	
user.UserTradeSubscription(trade_sub_cond)#持仓订阅
threads = []#从各个队列中读数据的线程集合
files = range(len(list.split()))#队列数目
for i in files:
    get_and_print = threading.Thread(target = CQGTrader.Recv, args = (list.split()[i-1]),)#创建读数据线程
    threads.append(get_and_print)
read_and_put  = recv(metadata_queue,position_queue)#把数据压到各个队列的线程
read_and_put.start()
for i in files:
    threads[i].start()
read_and_put.join()
for i in files:
    threads[i].join()
  
