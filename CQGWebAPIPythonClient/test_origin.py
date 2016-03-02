from webapi_1_pb2 import *
import webapi_CQGTrader_test

host_name = 'wss://demoapi.cqg.com:443'
user_name = 'CapitalCC'
password = 'pass'
client_id = 'WebApiTest'
client_version = 'python-client' 
info = 'CapitalCC pass WebApiTest python-client'

user  = webapi_CQGTrader_test.CQGTrader()
user.ApiLogin(host_name)
user.UserLogin(info)

