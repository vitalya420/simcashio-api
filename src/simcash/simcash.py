from collections.abc import Sequence
from typing import Optional, Union

from .confirmation import PendingCodeConfirmation
from .const import CODE_ERR, CODE_ERR_9
from .exceptions import UserEmailAlreadyExists, WrongCode, CredentialsNotProvided
from .helpers import payloads
from .helpers.utils import random_client_id, normalize_credentials
from .service.simcash import SimCashService

SIMCASH_VERSION = "3.107"


class SimCash:
    """
    Base class to operate with SimCash API on high level.
    """

    def __init__(self,
                 credentials: Union[str, dict[str, str], Sequence[str], None] = None,
                 client_id: Optional[str] = None,
                 ver: Optional[str] = SIMCASH_VERSION,
                 jwt_token: Optional[str] = None) -> None:
        """
        Example of credentials:
            credentials = "myemail@mail.com:password1"
            credentials = ("myemail@mail.com", "password1")
            credentials = {"email": "myemail@mail.com", "password": "password1"}
        :param credentials:
        :param client_id:
        :param ver:
        :param jwt_token:
        """
        if credentials and jwt_token:
            raise RuntimeError("Provide credentials or JWT token")
        self.credentials: Optional[tuple[str, str]] = normalize_credentials(credentials) if credentials else None
        self.jwt_token: Optional[str] = jwt_token
        self.client_id = client_id or random_client_id()
        self.ver = ver

    def authorize(self):
        if not self.credentials:
            raise CredentialsNotProvided()
        # res = SimCashService.authorize(*self.credentials, )
        # print("Authorization ", res)

    @classmethod
    def register(cls,
                 first_name: str,
                 last_name: str,
                 phone: str,
                 email: str,
                 password: str,
                 referral: Optional[str] = None,
                 ver: str = SIMCASH_VERSION,
                 *,
                 authorize_after_registration: bool = True,
                 ) -> PendingCodeConfirmation:
        """
        Register a new simcash account
        :param first_name: First name
        :param last_name: Last name
        :param phone: Phone in international format
        :param email: Email address (Will be username)
        :param password: Password
        :param referral: Referral code. Optional
        :param ver: Version of application. Optional. Default is 3.107
        :param authorize_after_registration:
        :return: PendingCodeConfirmation or raises Exception
        """
        payload = payloads.register(ver, email, password, f"{first_name} {last_name}", phone, referral)
        register_result = SimCashService.register(payload)
        response_code = register_result['code']
        if response_code == CODE_ERR:
            raise UserEmailAlreadyExists(f'{register_result['msg']}. Email: {email}')

        def _after_submit(code: Union[str, int]):
            instance = cls(credentials=(email, password))
            payload_verify = payloads.register_verify(email, instance.client_id,
                                                      str(code) if isinstance(code, int) else code)
            verify_result = SimCashService.register_verify(payload_verify)
            if verify_result['code'] == CODE_ERR_9:
                raise WrongCode(verify_result['msg'])
            if authorize_after_registration:
                instance.authorize()
            return instance

        return PendingCodeConfirmation(callback=_after_submit)

    @property
    def email(self):
        if self.credentials:
            return self.credentials[0]
        return '<no email>'

    def __repr__(self):
        return f"<SimCash(ver='{self.ver}', client_id='{self.client_id}', email='{self.email}')>"
