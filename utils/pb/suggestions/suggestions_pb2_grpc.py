# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import suggestions_pb2 as suggestions__pb2


class SuggestionsServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.startBookSuggestionsMicroService = channel.unary_unary(
                '/hello.SuggestionsService/startBookSuggestionsMicroService',
                request_serializer=suggestions__pb2.SuggestionsThreadRequest.SerializeToString,
                response_deserializer=suggestions__pb2.SuggestionsResponse.FromString,
                )
        self.bookSuggestionsEventF = channel.unary_unary(
                '/hello.SuggestionsService/bookSuggestionsEventF',
                request_serializer=suggestions__pb2.SuggestionsRequest.SerializeToString,
                response_deserializer=suggestions__pb2.SuggestionsResponse.FromString,
                )
        self.deleteData = channel.unary_unary(
                '/hello.SuggestionsService/deleteData',
                request_serializer=suggestions__pb2.SuggestionsDeleteRequest.SerializeToString,
                response_deserializer=suggestions__pb2.SuggestionsDeleteResponse.FromString,
                )


class SuggestionsServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def startBookSuggestionsMicroService(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def bookSuggestionsEventF(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SuggestionsServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'startBookSuggestionsMicroService': grpc.unary_unary_rpc_method_handler(
                    servicer.startBookSuggestionsMicroService,
                    request_deserializer=suggestions__pb2.SuggestionsThreadRequest.FromString,
                    response_serializer=suggestions__pb2.SuggestionsResponse.SerializeToString,
            ),
            'bookSuggestionsEventF': grpc.unary_unary_rpc_method_handler(
                    servicer.bookSuggestionsEventF,
                    request_deserializer=suggestions__pb2.SuggestionsRequest.FromString,
                    response_serializer=suggestions__pb2.SuggestionsResponse.SerializeToString,
            ),
            'deleteData': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteData,
                    request_deserializer=suggestions__pb2.SuggestionsDeleteRequest.FromString,
                    response_serializer=suggestions__pb2.SuggestionsDeleteResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'hello.SuggestionsService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SuggestionsService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def startBookSuggestionsMicroService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.SuggestionsService/startBookSuggestionsMicroService',
            suggestions__pb2.SuggestionsThreadRequest.SerializeToString,
            suggestions__pb2.SuggestionsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def bookSuggestionsEventF(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.SuggestionsService/bookSuggestionsEventF',
            suggestions__pb2.SuggestionsRequest.SerializeToString,
            suggestions__pb2.SuggestionsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hello.SuggestionsService/deleteData',
            suggestions__pb2.SuggestionsDeleteRequest.SerializeToString,
            suggestions__pb2.SuggestionsDeleteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
