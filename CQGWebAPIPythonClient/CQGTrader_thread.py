import websocket
from webapi_1_pb2 import *
import time
from config import *
import threading,queue
 
host_name = 'wss://demoapi.cqg.com:443'
info = 'CapitalCC pass WebApiTest python-client'
list = 'metadata position'
metadata_cond = '1 1 QFAH6'
trade_sub_cond = '1 16873141 1'

metadata_queue = queue.Queue()
position_queue = queue.Queue()	
class CQGTrader:

    def ApiLogin(self,info):#Api登入
      self._connection = websocket.create_connection(info)

    def ApiLogout(self,info=None):#Api登出
      if self._connection:
        self._connection.close()

    def UserLogin(self,info):#用户登入，即时返回登入消息（后续一切功能的前提）
      client_msg = ClientMsg()
      client_msg.logon.user_name = info.split()[0]
      client_msg.logon.password = info.split()[1]
      client_msg.logon.client_id = info.split()[2]
      client_msg.logon.client_version = info.split()[3]
      self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)
      server_msg = ServerMsg()
      opcode,data = self._connection.recv_data()
      server_msg.ParseFromString(data)
      print(str(server_msg))


    def UserLogout(self,info=None):#用户登出
      client_msg = ClientMsg()
      client_msg.logoff.text_message = "BY_REQUEST"
      self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)

    def UserRestoreSession(self,info):#会话保存
        client_msg = ClientMsg()
        client_msg.restore_session.session_token=info
        self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)

    def isApiContected(self):#Api是否连接
        if self._connection != None:
          print("Api Connected\n")
          return True
        else:
          print("Api Disconnected\n")
          return False

    def isUserLogged(self,info):#用户是否登录
        if info == 0:
          print("User Logged\n")
          return True
        else: 
          print("User Unlogged\n")
          return False
     
    def UserChangePassword(self,info):
        client_msg = ClientMsg()
        client_msg.password_change.old_password = info.split()[0]
        client_msg.password_change.new_password = info.split()[1]
        self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)

    def UserTradeSubscription(self,cond):#可实现持仓、委托订阅
        client_msg = ClientMsg()
        trade_subscription = client_msg.trade_subscription.add()
        trade_subscription.id = int(cond.split()[0])
        trade_subscription.subscription_scope.append(2)
        trade_subscription.publication_type = 1
        trade_subscription.account_id = int(cond.split()[1])
        trade_subscription.subscribe = int(cond.split()[2])
        # trade_subscription.skip_orders_snapshot=True
        trade_subscription.last_order_update_utc_time = 1
        self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)

    def UserMarketDataSubscription(self,cond):#实时市场数据订阅
        client_msg = ClientMsg()
        market_data_subscription = client_msg.market_data_subscription.add()
        market_data_subscription.contract_id = int(cond.split()[0])
        market_data_subscription.level=1
        self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)

    def UserMetadataSubscription(self,cond):#元数据订阅
      # while 1:
        client_msg = ClientMsg()
        information_request = client_msg.information_request.add()
        information_request.id = int(cond.split()[0])
        information_request.subscribe = int(cond.split()[1])
        information_request.symbol_resolution_request.symbol = cond.split()[2]
        self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)
       # time.sleep(10)

    def PlaceOrder(self,contract_id,cond):#委托(买卖)
        client_msg = ClientMsg()
        order_request = client_msg.order_request.add()
        order_request.request_id = int(cond.split()[0])
        order_request.new_order.order.account_id = int(cond.split()[1])
        order_request.new_order.order.when_utc_time = int(time.time())
        # print(str(order_request.new_order.order.when_utc_time))
        order_request.new_order.order.contract_id = contract_id
        order_request.new_order.order.cl_order_id = cond.split()[2]
        order_request.new_order.order.order_type = 2
        # order_request.new_order.order.exec_instruction.append(1)
        order_request.new_order.order.duration = 1
        order_request.new_order.order.side = int(cond.split()[3])
        order_request.new_order.order.limit_price = 5960
        order_request.new_order.order.qty = int(cond.split()[4])
        order_request.new_order.order.is_manual = True
        self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)
       
    def CancelOrder(self,cond):#取消委托（撤回）
        client_msg =  ClientMsg()
        order_request = client_msg.order_request.add()
        order_request.request_id = int(cond.split()[0])
        order_request.cancel_order.order_id = cond.split()[1]
        order_request.cancel_order.account_id = int(cond.split()[2])
        order_request.cancel_order.orig_cl_order_id = cond.split()[3]
        order_request.cancel_order.cl_order_id = cond.split()[4]
        order_request.cancel_order.when_utc_time = int(time.time())
        self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)

    def Recv(self,recv_tp):#从队列中取数据
        if recv_tp == 'metadata':
           data = metadata_queue.get()
           print(str(data))
        elif recv_tp == 'position':
           data = position_queue.get()
           print(str(data))

    def distributeData(self,metadata_queue,position_queue):
       # while 1:
           opcode,data  = self._connection.recv_data()
           length = len(data)
           if length > 0:#为了判断data的归属，是否应当先进行反序列化,再放入队列
              server_msg = ServerMsg()
              server_msg.ParseFromString(data)
              if len(str(server_msg.information_report[0].symbol_resolution_report.contract_metadata.contract_id)) > 0:
                 metadata_queue.put(data)
                # time.sleep(2)
              elif len(str(server_msg.position_status[0].open_position[0].id)) > 0:
                 position_queue.put(data)
                 #time.sleep(2)

    def recvTest(self):
       while 1:
         opcode,data = self._connection.recv_data()
         length = len(data)
         if length > 0:
           server_msg = ServerMsg()
           server_msg.ParseFromString(data)
           if len(server_msg.position_status) > 0:
               position_queue.put(data)
               time.sleep(2)
           elif len(server_msg.information_report) > 0:
               metadata_queue.put(data)
               time.sleep(2)
        
    def distributeTest(self,recv_tp):
       while 1:
        if recv_tp == 'position':
         data = position_queue.get()
         server_msg = ServerMsg()
         server_msg.ParseFromString(data)
        elif recv_tp == 'metadata':
         data = metadata_queue.get()
         server_msg = ServerMsg()
         server_msg.ParseFromString(data)
       # print(str(server_msg)) 
        print(len(server_msg.information_report))
        time.sleep(2)
   

user = CQGTrader()
user.ApiLogin(host_name)
user.UserLogin(info)
user.UserMetadataSubscription(metadata_cond)
user.UserTradeSubscription(trade_sub_cond)
user.distributeData(metadata_queue,position_queue)

t1 = threading.Thread(target=user.recvTest)
t2 = threading.Thread(target=user.distributeTest,args=('metadata',))
#t3 = threading.Thread(target=user.distributeTest,args=('metadata',))
t1.start()
t2.start()
#t3.start()
#t1.join()
#t2.join()
"""
t1 = threading.Thread(target=user.distributeData,args=(metadata_queue,position_queue)) 
t2 = threading.Thread(target=user.Recv,args=('metadata',)) 
t3 = threading.Thread(target=user.Recv,args=('position',)) 
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()
"""        
