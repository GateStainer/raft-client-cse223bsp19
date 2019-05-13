import logging
import grpc
import time
import csv
import kvstore_pb2
import kvstore_pb2_grpc
import chaosmonkey_pb2
import chaosmonkey_pb2_grpc

import click


@click.command()
def run():
    address = readAddress("remote-server.csv")
    # start = time.time()
    # for i in range(1):
    #     for a in address:
    #         upload(a, len(address))
    # print(time.time() - start)
    broken_list = [0, 1, 2, 3]
    for i in broken_list:
        try:
            update_server(address[i], i, False)
        except Exception:
            pass

def readAddress(file):
    servers = []
    with open(file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            servers.append(dict(row))
    address = []
    for s in servers:
        address.append(s["address"]+":"+s["port"])
    return address

def upload(address, server_num):
    with grpc.insecure_channel(address) as channel:
        # ChaosMoney matrix creation
        # cmMat = chaosmonkey_pb2.ConnMatrix()
        # for i in range(server_num):
        #     mat_row = cmMat.rows.add()
        #     for j in range(server_num):
        #         mat_row.vals.append(float(0.0))
                # mat_row.vals.add(float(0.25))

        cmstub = chaosmonkey_pb2_grpc.ChaosMonkeyStub(channel)
        # Add more addresses
        # response = cmstub.UploadMatrix(cmMat)
        # print("Client Upload ChaosMonkey Matrix received: " + str(response.ret) + ", @: "+address)

        response = cmstub.UpdateValue(chaosmonkey_pb2.MatValue(row = 1, col = 2, val = 0.99))
        print("Client Update ChaosMonkey Matrix Value received: " + str(response.ret) + "@: "+address)

# Update CM to simulate server crashing or restarting
def update_server(address, server_index, crash):
    value = 0.0
    if crash:
        value = 1.0
    with grpc.insecure_channel(address) as channel:
        cmstub = chaosmonkey_pb2_grpc.ChaosMonkeyStub(channel)
        for row in range(len(address)):
            cmstub.UpdateValue(chaosmonkey_pb2.MatValue(row = row, col = server_index, val = value))
        for col in range(len(address)):
            cmstub.UpdateValue(chaosmonkey_pb2.MatValue(row = server_index, col = col, val = value))


if __name__ == "__main__":
    logging.basicConfig()
    run()
