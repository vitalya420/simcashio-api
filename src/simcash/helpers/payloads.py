from typing import Optional


def register(ver: str, email: str, password: str, name: str,
             phone: str, ref: Optional[str] = None) -> dict[str, dict[str, str]]:
    retval = {"cmd51": {"ver": ver, "email": email, "pw": password, "name": name, "tel": phone}}
    if ref:
        retval["cmd51"]["ref"] = ref
    return retval


def register_verify(email: str, client_id: str, code: str) -> dict[str, dict[str, str]]:
    return {"cmd68": {"email": email, "client_id": client_id, "code": code}}


def authorize(email: str, password: str):
    pass