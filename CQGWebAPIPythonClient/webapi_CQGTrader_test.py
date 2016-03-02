import websocket
from webapi_1_pb2 import *

class CQGTrader:
    def ApiLogin(self,info):
      self._connection = websocket.create_connection(info)

    def ApiLogout(self,info=None):
      if self._connection:
        self._connection.close()

    def UserLogin(self,info):
      client_msg = ClientMsg()
      client_msg.logon.user_name = info.split()[0]
      client_msg.logon.password = info.split()[1]
      client_msg.logon.client_id = info.split()[2]
      client_msg.logon.client_version = info.split()[3]
      #client_msg.logon.drop_concurrent_session = info.split(' ')[4]
      self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)
     # print("Client message sent:\n" + str(client_msg))
      
      server_msg = ServerMsg()
      opcode,data = self._connection.recv_data()
      if opcode == websocket.ABNF.OPCODE_TEXT:
         raise Exception("Received unexpected text message from WebAPI server")
      elif opcode == websocket.ABNF.OPCODE_CLOSE:
         raise websocket.WebSocketConnectionClosedException(
                "Can't receive message - WebAPI server closed connection")

      server_msg.ParseFromString(data)
      if server_msg.logon_result.result_code == 0:
         print("SUCCESS")
      if server_msg.logon_result.result_code == 101:
         print("FAILURE")
      if server_msg.logon_result.result_code == 104:
         print("PASSWORD_EXPIRED")
      if server_msg.logon_result.result_code == 105:
         print("CONCURRENT_SESSION")

 
      print("Server message received:\n" + str(server_msg.logon_result))
      return server_msg
     # print(server_msg.logon_result.result_code)
 
    def UserLogout(self,info=None):
      client_msg = ClientMsg()
      client_msg.logoff.text_message = "BY_REQUEST"
      self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_TEXT)
      server_msg = ServerMsg()
      opcode,data = self._connection.recv_data()
     # server_msg.ParseFromString(data)
      if opcode == websocket.ABNF.OPCODE_CLOSE:
         #raise websocket.WebSocketConnectionClosedException(
              #  "Can't receive message - WebAPI server closed connection")
     # if server_msg.logged_off.LogoffReason == 1:
         print("BY_REQUEST")
         
      """
      opcode,data = self._connection.recv_data()
      if opcode == websocket.ABNF.OPCODE_TEXT:
         raise Exception("Received unexpected text message from WebAPI server")
         raise websocket.WebSocketConnectionClosedException(
                "Can't receive message - WebAPI server closed connection")
      server_msg.ParseFromString(data)
      if server_msg.logged_off.LogoffReason == 1:
         print("BY_REQUEST")
      return server_msg
      """

      """
    def send_client_message(self, client_msg):
        self._connection.send(client_msg.SerializeToString(), websocket.ABNF.OPCODE_BINARY)
        if self._need_to_log:
            print("Client message sent:\n" + str(client_msg))

    def receive_server_message(self):
        server_msg = ServerMsg()
        opcode, data = self._connection.recv_data()
        if opcode == websocket.ABNF.OPCODE_TEXT:
            raise Exception("Received unexpected text message from WebAPI server")
        elif opcode == websocket.ABNF.OPCODE_CLOSE:
            raise websocket.WebSocketConnectionClosedException(
                "Can't receive message - WebAPI server closed connection")
             
        server_msg.ParseFromString(data)

        if self._need_to_log:
            print("Server message received:\n" + str(server_msg))
        return server_msg
        """

    def UserRestoreSession(self,info):
      client_msg = ClientMsg()
      client_msg.restore_session.session_token=info
      self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)
      server_msg = ServerMsg()
      opcode,data = self._connection.recv_data()
      server_msg.ParseFromString(data)
      print("Server message received:\n" + str(server_msg))

    def isApiContected(self):
      if self._connection != None:
        print("Api Connected\n")
        return True
      else:
        print("Api Disconnected\n")
        return False

    def isUserLogged(self,info):
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
      server_msg = ServerMsg()
      opcode,data = self._connection.recv_data()
      server_msg.ParseFromString(data)
      print("Server message received:\n" + str(server_msg))

    def UserTradeSubscription(self,cond):
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
        while (1):
         server_msg = ServerMsg()
         opcode,data = self._connection.recv_data()
         server_msg.ParseFromString(data)
         if server_msg.position_status is not None:
          print(str(server_msg))
        #return server_msg

    def UserMarketDataSubscription(self,cond):
        client_msg = ClientMsg()
        market_data_subscription = client_msg.market_data_subscription.add()
        market_data_subscription.contract_id = int(cond.split()[0])
        market_data_subscription.level=1
        self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)
        while (1):
         server_msg = ServerMsg()
         opcode,data = self._connection.recv_data()
         server_msg.ParseFromString(data)
         print(str(server_msg.real_time_market_data))
       # return server_msg

    def Recv(self,recv_tp,cond):
      if recv_tp == 'metadata':
        client_msg = ClientMsg()
        information_request = client_msg.information_request.add()
        information_request.id = int(cond.split()[0])
        information_request.subscribe = int(cond.split()[1])
        information_request.symbol_resolution_request.symbol = cond.split()[2]
        self._connection.send(client_msg.SerializeToString(),websocket.ABNF.OPCODE_BINARY)
        while (1):
         server_msg = ServerMsg()
         opcode,data = self._connection.recv_data()
         server_msg.ParseFromString(data)
         print("Contract Metadata:\n"+str(server_msg.information_report[0].symbol_resolution_report.contract_metadata))
         #print("Contract Metadata:\n"+str(server_msg.information_report[0]))

       # return server_msg

    def PlaceOrder(self,cond):
      pass
    def CancelOrder(self,cond):
      pass
 
