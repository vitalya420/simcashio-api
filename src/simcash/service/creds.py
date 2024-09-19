import os
from typing import Optional

import grpc
from grpc import ChannelCredentials


def grpc_credentials(folder: Optional[str] = None) -> ChannelCredentials:
    folder = folder or os.path.dirname(os.path.abspath(__file__))
    certs_path = os.path.join(folder, 'certs')

    with open(os.path.join(certs_path, "ca-cert.pem"), 'rb') as f:
        ca_cert = f.read()
    with open(os.path.join(certs_path, "cert.pem"), 'rb') as f:
        cert = f.read()
    with open(os.path.join(certs_path, "key.pem"), 'rb') as f:
        key = f.read()

    credentials = grpc.ssl_channel_credentials(
        root_certificates=ca_cert,
        private_key=key,
        certificate_chain=cert
    )
    return credentials
