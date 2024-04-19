# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import payment_system_pb2 as payment__system__pb2


class PaymentServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.paymentLogic = channel.unary_unary(
                '/hello.PaymentService/paymentLogic',
                request_serializer=payment__system__pb2.PaymentRequest.SerializeToString,
                response_deserializer=payment__system__pb2.PaymentResponse.FromString,
                )
        self.prepareToExecute = channel.unary_unary(
                '/hello.PaymentService/prepareToExecute',
                request_serializer=payment__system__pb2.PaymentRequest.SerializeToString,
                response_deserializer=payment__system__pb2.PaymentResponse.FromString,
                )


class PaymentServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def paymentLogic(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def prepareToExecute(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PaymentServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'paymentLogic': grpc.unary_unary_rpc_method_handler(
                    servicer.paymentLogic,
                    request_deserializer=payment__system__pb2.PaymentRequest.FromString,
                    response_serializer=payment__system__pb2.PaymentResponse.SerializeToString,
            ),
            'prepareToExecute': grpc.unary_unary_rpc_method_handler(
                    servicer.prepareToExecute,
                    request_deserializer=payment__system__pb2.PaymentRequest.FromString,
                    response_serializer=payment__system__pb2.PaymentResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'hello.PaymentService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PaymentService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def paymentLogic(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.PaymentService/paymentLogic',
            payment__system__pb2.PaymentRequest.SerializeToString,
            payment__system__pb2.PaymentResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def prepareToExecute(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.PaymentService/prepareToExecute',
            payment__system__pb2.PaymentRequest.SerializeToString,
            payment__system__pb2.PaymentResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
