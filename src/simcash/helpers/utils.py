import uuid
from typing import Union, Sequence


def random_client_id():
    return "cccc" + str(uuid.uuid4())[4:]


def normalize_credentials(credentials: Union[str, dict[str, str], Sequence[str]]):
    if isinstance(credentials, str) and ':' in credentials:
        return tuple(credentials.split(':'))
    if isinstance(credentials, dict) and "email" in credentials and "password" in credentials:
        return credentials["email"], credentials["password"]
    if isinstance(credentials, Sequence):
        return tuple(credentials)
