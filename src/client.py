import logging
import grpc

import time
import kvstore_pb2
import kvstore_pb2_grpc
import chaosmonkey_pb2
import chaosmonkey_pb2_grpc
from chaos import readAddress

def run():

    addresses = readAddress("remote-server.csv")
    print(addresses)

    start = time.time()
    leaderID = 0
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
                # time.sleep(0.1)
    except Exception as e:
        print(e)
    print(time.time() - start)

    # TODO: Implement PUT and GET
    myKey = "1"*1024
    myValue = "1"*1024
    start = time.time()
    seq_num = 1

    for i in range(100):
        try:
            while True:
                channel = grpc.insecure_channel(addresses[leaderID])
                stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
                # print("Try to put")
                response = stub.Put(kvstore_pb2.PutRequest(key = myKey, value = myValue, clientID = clientID, sequenceNum = seq_num))
                if response.status == kvstore_pb2.NOT_LEADER:
                    leaderID = response.leaderHint
                elif response.status == kvstore_pb2.SESSION_EXPIRED:
                    print("Session Expired")
                elif response.status == kvstore_pb2.OK2CLIENT:
                    print("PUT OK")
                    break
                else:
                    print("PUT Error")
        except Exception as e:
            print(e)
        seq_num += 1


    print(time.time() - start)

    start = time.time()
    try:
        while True:
            channel = grpc.insecure_channel(addresses[leaderID])
            stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
            print("Try to get")
            response = stub.Get(kvstore_pb2.GetRequest(key = myKey))
            if response.status == kvstore_pb2.NOT_LEADER:
                leaderID = response.leaderHint
            elif response.status == kvstore_pb2.SESSION_EXPIRED:
                print("Session Expired")
            elif response.status == kvstore_pb2.OK2CLIENT:
                print(f'GET OK: ')#<{response.value}>')
                break
            else:
                print("GET Error")
    except Exception as e:
        print(e)
    print(time.time() - start)

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
