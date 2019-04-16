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

if __name__ == "__main__":
    logging.basicConfig()
    run()
