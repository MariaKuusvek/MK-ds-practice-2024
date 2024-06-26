# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import order_queue_pb2 as order__queue__pb2


class QueueServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.enqueue = channel.unary_unary(
                '/hello.QueueService/enqueue',
                request_serializer=order__queue__pb2.QueueRequest.SerializeToString,
                response_deserializer=order__queue__pb2.QueueResponse.FromString,
                )
        self.dequeue = channel.unary_unary(
                '/hello.QueueService/dequeue',
                request_serializer=order__queue__pb2.QueueRequestDequeue.SerializeToString,
                response_deserializer=order__queue__pb2.QueueResponseDequeue.FromString,
                )
        self.queueHasElements = channel.unary_unary(
                '/hello.QueueService/queueHasElements',
                request_serializer=order__queue__pb2.QueueRequestDequeue.SerializeToString,
                response_deserializer=order__queue__pb2.QueueResponse.FromString,
                )


class QueueServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def enqueue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def dequeue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def queueHasElements(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QueueServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'enqueue': grpc.unary_unary_rpc_method_handler(
                    servicer.enqueue,
                    request_deserializer=order__queue__pb2.QueueRequest.FromString,
                    response_serializer=order__queue__pb2.QueueResponse.SerializeToString,
            ),
            'dequeue': grpc.unary_unary_rpc_method_handler(
                    servicer.dequeue,
                    request_deserializer=order__queue__pb2.QueueRequestDequeue.FromString,
                    response_serializer=order__queue__pb2.QueueResponseDequeue.SerializeToString,
            ),
            'queueHasElements': grpc.unary_unary_rpc_method_handler(
                    servicer.queueHasElements,
                    request_deserializer=order__queue__pb2.QueueRequestDequeue.FromString,
                    response_serializer=order__queue__pb2.QueueResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'hello.QueueService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class QueueService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def enqueue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.QueueService/enqueue',
            order__queue__pb2.QueueRequest.SerializeToString,
            order__queue__pb2.QueueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def dequeue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.QueueService/dequeue',
            order__queue__pb2.QueueRequestDequeue.SerializeToString,
            order__queue__pb2.QueueResponseDequeue.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def queueHasElements(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.QueueService/queueHasElements',
            order__queue__pb2.QueueRequestDequeue.SerializeToString,
            order__queue__pb2.QueueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
