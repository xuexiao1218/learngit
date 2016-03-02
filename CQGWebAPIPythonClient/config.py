import queue
metadata_queue = queue.Queue()
position_queue = queue.Queue()

def setGlobalMetadata(metadata):
     metadata_queue = metadata
    
def setGlobalPosition(position):
     position_queue = position

def getGlobalMetadata():
     return metadata_queue
         
def getGlobalPosition():
     return position_queue    
