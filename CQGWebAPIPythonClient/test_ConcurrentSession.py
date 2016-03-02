from webapi_1_pb2 import *
import webapi_CQGTrader

host_name = 'wss://demoapi.cqg.com:443'
user_name = 'CapitalCC'
password = 'pass'
client_id = 'WebApiTest'
client_version = 'python-client'

user  = webapi_CQGTrader.CQGTrader()
user.ApiLogin(host_name)
user.UserLogin(user_name,password,client_id,client_version,False)

