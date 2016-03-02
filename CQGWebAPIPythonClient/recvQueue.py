import websocket,threading,time
import queue
from config import *
from webapi_1_pb2 import *


class recv(threading.Thread):#把数据放到不同队列里,考虑数据有不同的来源（类型），因此在处理过程中要进行甄别和分派。结果会存在多个queue
    def __init__(self,metadata_queue,position_queue):#是否要初始化多个queue?
       threading.Thread.__init__(self)
       self.metadata_queue = metadata_queue
       self.position_queue = position_queue
    def run(self):#根据data的不同，put到各个队列中
        while 1:
           opcode,data  = self._connection.recv_data()
           length = len(data)
           if length > 0:#为了判断data的归属，是否应当先进行反序列化,再放入队列
              server_msg = ServerMsg()
              server_msg.ParseFromString(data)
              if len(server_msg.information_report[0].symbol_resolution_report.contract_metadata.contract_id) > 0:
                 self.metadata_queue.put(data)
                 time.sleep(2)
              elif len(server_msg.position_status[0].open_position[0].id) > 0:
                 self.position_queue.put(data)
                 time.sleep(2) 
