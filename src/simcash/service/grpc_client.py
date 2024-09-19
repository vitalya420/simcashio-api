import grpc

from simcash.service.creds import grpc_credentials
from simcash.service.smscash_pb2 import MessageRequest, AuthorizeRequest
from simcash.service.smscash_pb2_grpc import SimcashStub

DEFAULT_HOST = "sec2.simcash.io:443"


class SimCashGrpcClient:
    def __init__(self,
                 host: str = DEFAULT_HOST,
                 credentials: grpc.ssl_channel_credentials = grpc_credentials()):
        self.host = host
        self.credentials = credentials
        self.channel = grpc.secure_channel(host, credentials)
        self.stub = SimcashStub(self.channel)

    def send(self, key: str, payload: str):
        req = MessageRequest(key=key, payload=payload)
        response = self.stub.Register(req)
        return response

    def register(self, key: str, payload: str):
        return self.stub.Register(MessageRequest(key=key, payload=payload))

    def register_verify(self, key: str, payload: str):
        return self.stub.Registerverify(MessageRequest(key=key, payload=payload))

    def authorize(self, email: str, password: str, payload: str):
        return self.stub.Authorize(AuthorizeRequest(
            email=email,
            password=password,
            payload=payload
        ))

    def __repr__(self):
        return f"<SimCashGrpcClient(host='{self.host}')>"


default_grpc_client = SimCashGrpcClient(host=DEFAULT_HOST, credentials=grpc_credentials())
