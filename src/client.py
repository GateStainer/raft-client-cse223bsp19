import logging
import grpc

import kvstore_pb2
import kvstore_pb2_grpc
import chaosmonkey_pb2
import chaosmonkey_pb2_grpc

import click


@click.command()
@click.option('--address', '-a', type=str, default="localhost:7000")
def run(address):
    with grpc.insecure_channel(address) as channel:
        stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)
        response = stub.Put(kvstore_pb2.PutRequest(key = "1", value = "100"))
        print("Client PUT received: " + str(response.ret))

        response = stub.Get(kvstore_pb2.GetRequest(key = "1"))
        print("Client GET received: " + str(response.value))

        # ChaosMoney matrix
        cmMat = chaosmonkey_pb2.ConnMatrix()
        row1 = cmMat.rows.add()
        row1.vals = "0.25 0.25 0.25"
        row2 = cmMat.rows.add()
        row2.vals = "0.25 0.25 0.25"
        row3 = cmMat.rows.add()
        row3.vals = "0.25 0.25 0.25"

        cmstub = chaosmonkey_pb2_grpc.ChaosMonkeyStub(channel)
        response = cmstub.UploadMatrix(cmMat)
        print("Client Upload ChaosMonkey Matrix received: " + str(response.ret))

        response = cmstub.UpdateValue(chaosmonkey_pb2.MatValue(row = 1, col = 2, val = 0.99))
        print("Client Update ChaosMonkey Matrix Value received: " + str(response.value))

if __name__ == "__main__":
    logging.basicConfig()
    run()