from webapi_1_pb2 import *
import webapi_client

host_name = 'wss://demoapi.cqg.com:443'
user_name = 'msinghalwapi'
password = 'pass'


def logon(user_name, password, client_id='WebApiTest', client_version='python-client'):
    client_msg = ClientMsg()
    client_msg.logon.user_name = user_name
    client_msg.logon.password = password
    client_msg.logon.client_id = client_id
    client_msg.logon.client_version = client_version
    client.send_client_message(client_msg)

    server_msg = client.receive_server_message()
    if server_msg.logon_result.result_code == 0:
        return server_msg.logon_result.base_time
    else:
        raise Exception("Can't login: " + server_msg.logon_result.text_message)


def resolve_symbol(symbol_name, msg_id=1, subscribe=None):
    client_msg = ClientMsg()
    information_request = client_msg.information_request.add()
    information_request.id = msg_id
    if subscribe is not None:
        information_request.subscribe = subscribe
    information_request.symbol_resolution_request.symbol = symbol_name
    client.send_client_message(client_msg)

    server_msg = client.receive_server_message()
    return server_msg.information_report[0].symbol_resolution_report.contract_metadata


client = webapi_client.WebApiClient(need_to_log=True)
client.connect(host_name)

logon(user_name, password)
contract_metadata = resolve_symbol('EP',1,1)
print(contract_metadata.contract_symbol, contract_metadata.description)

#client.disconnect()
