import websocket
from webapi_1_pb2 import *
import time
import threading,queue,sys

metadata_queue = queue.Queue()
position_queue = queue.Queue()
order_queue = queue.Queue()
marketprice_queue = queue.Queue()
metadata_cond = '1 1 QFAH6'
position_cond = '1 16873141 1'

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
       #从服务器到各个队列，从Api登入开始，始终在跑
      t1 = threading.Thread(target=self.ServerToQueue,args=(metadata_queue,position_queue,order_queue,marketprice_queue))
      t1.start()
 
    def UserLogout(self,info=None):#用户登出
      client_msg = ClientMsg()
      client_msg.logoff.text_message = "BY_REQUEST"
      self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_TEXT)
 
    def isApiContected(self):#Api是否连接
      if self._connection != None:
        print("Api Connected\n")
        return True
      else:
        print("Api Disconnected\n")
        return False

    def isUserLogged(self,info):#用户是否登陆
      if info == 0:
        print("User Logged\n")
        return True
      else: 
        print("User Unlogged\n")
        return False

    def Send(self):
        send_tp = input("send metadata or position?\n")
        client_msg = ClientMsg()
        if send_tp == 'metadata':#元数据订阅
          cond = metadata_cond
          information_request = client_msg.information_request.add()
          information_request.id = int(cond.split()[0])
          information_request.subscribe = int(cond.split()[1])
          information_request.symbol_resolution_request.symbol = cond.split()[2]
          print('send_metadata')
        elif send_tp == 'position':#持仓订阅
          cond = position_cond
          trade_subscription = client_msg.trade_subscription.add()
          trade_subscription.id = int(cond.split()[0]) 
          trade_subscription.subscription_scope.append(2)
          trade_subscription.publication_type = 1
          trade_subscription.account_id = int(cond.split()[1])
          trade_subscription.subscribe = int(cond.split()[2])
          trade_subscription.last_order_update_utc_time = 1
          print('send_position')
        elif send_tp == 'order':#委托订阅
          trade_subscription = client_msg.trade_subscription.add()
          trade_subscription.id = int(cond.split()[0])
          trade_subscription.subscription_scope.append(1)
          trade_subscription.publication_type = 1
          trade_subscription.account_id = int(cond.split()[1])
          trade_subscription.subscribe = int(cond.split()[2])
          trade_subscription.last_order_update_utc_time = 1
          print('send_order')
        elif send_tp == 'marketprice':#实时市场数据订阅
          market_data_subscription = client_msg.market_data_subscription.add()
          market_data_subscription.contract_id = int(cond.split()[0])
          market_data_subscription.level = 1
          print('send_marketprice')
        self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY) 

    def Recv(self):#从队列中取数据
        recv_tp = input("receive metadata or position?\n")
        if recv_tp == 'metadata':#元数据
           data = metadata_queue.get()
           print('recv_metadata')
        if recv_tp == 'position':#持仓
           data = position_queue.get()
           print('recv_position') 
        if recv_tp == 'marketprice':#行情
           data = marketprice_queue.get()
           print('recv_marketprice')
        if recv_tp == 'order':#委托
           data = order_queue.get()
           print('recv_order') 
        print(data)

    def ServerToQueue(self,metadata_queue,position_queue,order_queue,marketprice_queue):
        while 1:
           opcode,data  = self._connection.recv_data()
           server_msg = ServerMsg()
           server_msg.ParseFromString(data)
           for position_status in server_msg.position_status:
             position_queue.put(position_status.subscription_id)
             position_queue.put(position_status.is_snapshot)
             position_queue.put(position_status.account_id)
             position_queue.put(position_status.contract_id)
             for open_position in position_status.open_position:
               position_queue.put(open_position)
          # print('position')
           for information_report in server_msg.information_report:
             metadata_queue.put(informaiton_report.id)
             metadata_queue.put(information_report.status_code)
             metadata = informtion_report.symbol_resolution_report.contract_metadata
             metadata_queue.put(metadata)
            # print('metadata')
         
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
    
