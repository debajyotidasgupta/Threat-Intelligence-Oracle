# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import threat_pb2 as threat__pb2


class ThreatStub(object):
    """This is the name of the service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getThreatScore = channel.unary_unary(
                '/threat.Threat/getThreatScore',
                request_serializer=threat__pb2.threatRequest.SerializeToString,
                response_deserializer=threat__pb2.threatResponse.FromString,
                )


class ThreatServicer(object):
    """This is the name of the service.
    """

    def getThreatScore(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ThreatServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getThreatScore': grpc.unary_unary_rpc_method_handler(
                    servicer.getThreatScore,
                    request_deserializer=threat__pb2.threatRequest.FromString,
                    response_serializer=threat__pb2.threatResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'threat.Threat', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Threat(object):
    """This is the name of the service.
    """

    @staticmethod
    def getThreatScore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/threat.Threat/getThreatScore',
            threat__pb2.threatRequest.SerializeToString,
            threat__pb2.threatResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
