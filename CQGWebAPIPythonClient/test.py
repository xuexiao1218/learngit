from webapi_1_pb2 import * 
import webapi_CQGTrader


host_name = 'wss://demoapi.cqg.com:443'
user_name = 'CapitalCC'
password = 'pass'
client_id = 'WebApiTest'
client_version = 'python-client'
info = "CapitalCC pass WebApiTest python-client 1"
metadata_cond = "1 1 QFAH6"
trade_sub_cond = "1 16873141 1"
market_data_sub_cond = "1"
place_order_cond =  "1 16873141 3 1 1"
cancel_order_cond =  "1 515700612 16873141 3 4"


user  = webapi_CQGTrader.CQGTrader()
user.ApiLogin(host_name)
#user.UserLogin(info)
#user.UserLogin(user_name,'123456',client_id,client_version)
#user.UserLogin(user_name,password,client_id,'')
loginfo = user.UserLogin(info).logon_result.result_code
server_msg1 =  user.Recv('metadata',metadata_cond)
contract_id = server_msg1.information_report[0].symbol_resolution_report.contract_metadata.contract_id
#user.PlaceOrder(contract_id,place_order_cond)
user.CancelOrder(cancel_order_cond)
#user.UserTradeSubscription(trade_sub_cond)
#user.UserMarketDataSubscription(market_data_sub_cond)
#user.Recv('trade_subscription',trade_sub_cond)
#user.isUserLogged(loginfo)
#user.UserLogout()
#user.isUserLogged(loginfo)
#user.ApiLogout()
