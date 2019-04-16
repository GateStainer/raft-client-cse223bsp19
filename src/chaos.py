import logging
import grpc

import kvstore_pb2
import kvstore_pb2_grpc
import chaosmonkey_pb2
import chaosmonkey_pb2_grpc

import click


@click.command()
def run():
    address = ['localhost:7000', 'localhost:7001', 'localhost:7002']
    for a in address:
        upload(a)


def upload(address):
    with grpc.insecure_channel(address) as channel:
        # ChaosMoney matrix creation
        cmMat = chaosmonkey_pb2.ConnMatrix()
        for i in range(3):
            mat_row = cmMat.rows.add()
            for j in range(3):
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
