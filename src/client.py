import logging
import grpc

import time
import kvstore_pb2
import kvstore_pb2_grpc
import chaosmonkey_pb2
import chaosmonkey_pb2_grpc

def run():

    addresses = ['35.160.215.250:7000', '34.208.60.253:7000', '54.218.144.35:7000', '52.13.110.148:7000', \
                 '54.188.17.95:7000', '34.222.132.15:7000', '52.33.179.213:7000', '54.212.238.60:7000', \
                 '35.167.51.122:7000', '54.187.20.63:7000']
    leaderID = 0
    clientID = -1
    try:
        while True:
            if leaderID == -1:
                leaderID = 0
            channel = grpc.insecure_channel(addresses[leaderID])
            stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
            print(f'Send RegisterClient RPC to server <{leaderID}>')
            response = stub.registerClient(kvstore_pb2.RegisterRequest())
            if response.status == kvstore_pb2.OK2CLIENT:
                clientID = response.clientID
                print(f"Register client as <{clientID}>")
                break
            else:
                leaderID = response.leaderHint
                time.sleep(0.1)
    except Exception as e:
        print(e)


    # TODO: Implement PUT and GET
    start = time.time()
    seq_num = 1

    for i in range(100):
        try:
            while True:
                channel = grpc.insecure_channel(addresses[leaderID])
                stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
                # print("Try to put")
                response = stub.Put(kvstore_pb2.PutRequest(key = "1", value = "100", clientID = clientID, sequenceNum = seq_num))
                if response.status == kvstore_pb2.NOT_LEADER:
                    leaderID = response.leaderHint
                elif response.status == kvstore_pb2.SESSION_EXPIRED:
                    print("Session Expired")
                elif response.status == kvstore_pb2.OK2CLIENT:
                    # print("PUT OK")
                    break
                else:
                    print("PUT Error")
        except Exception as e:
            print(e)
        seq_num += 1


    print(time.time() - start)

    # try:
    #     while True:
    #         channel = grpc.insecure_channel(addresses[leaderID])
    #         stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
    #         print("Try to get")
    #         response = stub.Get(kvstore_pb2.GetRequest(key = "1"))
    #         if response.status == kvstore_pb2.NOT_LEADER:
    #             leaderID = response.leaderHint
    #         elif response.status == kvstore_pb2.SESSION_EXPIRED:
    #             print("Session Expired")
    #         elif response.status == kvstore_pb2.OK2CLIENT:
    #             print(f'GET OK: <{response.value}>')
    #             break
    #         else:
    #             print("GET Error")
    # except Exception as e:
    #     print(e)

    #
    # with grpc.insecure_channel(address) as channel:
    #     stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
    #     # print("Try to put")
    #     response = stub.Put(kvstore_pb2.PutRequest(key = "1", value = "100"))
    #     print("Client PUT received: " + str(response.ret))
    #
    #
    #     response = stub.Get(kvstore_pb2.GetRequest(key = "1"))
    #     print("Client GET received: " + str(response.value))

if __name__ == "__main__":
    logging.basicConfig()
    run()
