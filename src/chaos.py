import logging
import grpc
import time

import kvstore_pb2
import kvstore_pb2_grpc
import chaosmonkey_pb2
import chaosmonkey_pb2_grpc

import click


@click.command()
def run():
    address = ['35.160.215.250:7000', '34.208.60.253:7000', '54.218.144.35:7000', '52.13.110.148:7000', \
               '54.188.17.95:7000', '34.222.132.15:7000', '52.33.179.213:7000', '54.212.238.60:7000', \
               '35.167.51.122:7000', '54.187.20.63:7000']
    start = time.time()
    for i in range(100):
        for a in address:
            upload(a)
    print(time.time() - start)


def upload(address):
    with grpc.insecure_channel(address) as channel:
        # ChaosMoney matrix creation
        cmMat = chaosmonkey_pb2.ConnMatrix()
        for i in range(10):
            mat_row = cmMat.rows.add()
            for j in range(10):
                mat_row.vals.append(float(0.25))
                # mat_row.vals.add(float(0.25))

        cmstub = chaosmonkey_pb2_grpc.ChaosMonkeyStub(channel)
        # Add more addresses
        response = cmstub.UploadMatrix(cmMat)
        print("Client Upload ChaosMonkey Matrix received: " + str(response.ret) + ", @: "+address)

        response = cmstub.UpdateValue(chaosmonkey_pb2.MatValue(row = 1, col = 2, val = 0.99))
        print("Client Update ChaosMonkey Matrix Value received: " + str(response.ret) + "@: "+address)

if __name__ == "__main__":
    logging.basicConfig()
    run()
