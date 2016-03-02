Installation
------------

* Install Python 3 (http://www.python.org/)
    Latest Windows installer - http://www.python.org/ftp/python/3.3.4/python-3.3.4.msi

* Modify start.py - set proper host_name, user_name and password

* Run test script:
    python.exe start.py

Package content
---------------

\google          - part of Google Protocol Buffers library
start.py         - sample application
webapi_1.proto   - readable description of protocol messages in ProtoBuf format (with comments)
webapi_1_pb2.py  - protocol wrapper for Python, compiled from .proto
webapi_client.py - helper class for connection to WebAPI server
websocket.py     - WebSocket client library (https://pypi.python.org/pypi/websocket-client/)
protoc.exe       - compiler from .proto files to .py

To generate new version of webapi_1_pb2.py in case webapi_1.proto changes:
    protoc.exe --python_out=. webapi_1.proto
