# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import kvstore_pb2 as kvstore__pb2


class KeyValueStoreStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Get = channel.unary_unary(
        '/kvstore.KeyValueStore/Get',
        request_serializer=kvstore__pb2.GetRequest.SerializeToString,
        response_deserializer=kvstore__pb2.GetResponse.FromString,
        )
    self.Put = channel.unary_unary(
        '/kvstore.KeyValueStore/Put',
        request_serializer=kvstore__pb2.PutRequest.SerializeToString,
        response_deserializer=kvstore__pb2.PutResponse.FromString,
        )


class KeyValueStoreServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Get(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Put(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_KeyValueStoreServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Get': grpc.unary_unary_rpc_method_handler(
          servicer.Get,
          request_deserializer=kvstore__pb2.GetRequest.FromString,
          response_serializer=kvstore__pb2.GetResponse.SerializeToString,
      ),
      'Put': grpc.unary_unary_rpc_method_handler(
          servicer.Put,
          request_deserializer=kvstore__pb2.PutRequest.FromString,
          response_serializer=kvstore__pb2.PutResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'kvstore.KeyValueStore', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
