class InvalidCode(Exception):
    pass


class UnexpectedResponse(Exception):
    pass


class EmailUsedButNotConfirmed(Exception):
    pass


class UserEmailAlreadyExists(Exception):
    pass


class WrongCode(Exception):
    pass


class SimCashError(Exception):
    pass


class CredentialsNotProvided(Exception):
    pass
