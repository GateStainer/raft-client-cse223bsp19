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
        # print("Try to put")
        response = stub.Put(kvstore_pb2.PutRequest(key = "1", value = "100"))
        print("Client PUT received: " + str(response.ret))

        response = stub.Get(kvstore_pb2.GetRequest(key = "1"))
        print("Client GET received: " + str(response.value))

    with grpc.insecure_channel('localhost:7000') as channel:
        # ChaosMoney matrix creation
        cmMat = chaosmonkey_pb2.ConnMatrix()
        for i in range(3):
            mat_row = cmMat.rows.add()
            for j in range(3):
                mat_row.vals.append(float(0.25))
                # mat_row.vals.add(float(0.25))

        cmstub = chaosmonkey_pb2_grpc.ChaosMonkeyStub(channel)
        # Add more addresses
        addresses = ["localhost:6000"]
        for address in addresses:
            response = cmstub.UploadMatrix(cmMat)
            print("Client Upload ChaosMonkey Matrix received: " + str(response.ret) + ", @: "+address)

            response = cmstub.UpdateValue(chaosmonkey_pb2.MatValue(row = 1, col = 2, val = 0.99))
            print("Client Update ChaosMonkey Matrix Value received: " + str(response.ret) + "@: "+address)

if __name__ == "__main__":
    logging.basicConfig()
    run()