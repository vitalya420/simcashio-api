import json
from typing import Union

from simcash.exceptions import UnexpectedResponse
from simcash.service.grpc_client import default_grpc_client


class SimCashService:
    @staticmethod
    def send(key: str, payload: Union[str, dict]):
        payload = payload if isinstance(payload, str) else json.dumps(payload)
        response = default_grpc_client.send(key, payload)
        return response

    @staticmethod
    def register(payload: Union[str, dict]) -> dict[str, dict[str, Union[str, int]]]:
        payload = payload if isinstance(payload, str) else json.dumps(payload)
        res = default_grpc_client.register("register", payload)
        key, payload = res.key, json.loads(res.payload)
        if key != 'register_result' or 'rsp51' not in payload:
            UnexpectedResponse("Got unexpected response from server", key)
        return payload['rsp51']

    @staticmethod
    def register_verify(payload: Union[str, dict]):
        payload = payload if isinstance(payload, str) else json.dumps(payload)
        res = default_grpc_client.register_verify("register_verify", payload)
        key, payload = res.key, json.loads(res.payload)
        if key != 'register_verify_result' or 'rsp68' not in payload:
            UnexpectedResponse("Got unexpected response from server", key)
        return payload['rsp68']

    @staticmethod
    def authorize(email: str, password: str, payload: Union[str, dict]) -> dict[str, dict[str, Union[str, int]]]:
        payload = payload if isinstance(payload, str) else json.dumps(payload)
        res = default_grpc_client.authorize(email, password, payload)
        return res
