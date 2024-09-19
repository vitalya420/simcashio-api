from simcash.exceptions import UserEmailAlreadyExists
from simcash import SimCash
from simcash import PendingCodeConfirmation


def main():
    # Registration with high level api
    try:
        confirmation = SimCash.register(
            first_name="John",
            last_name="Doe",
            phone="+1123123123",
            email="wesileg886@marchub.com",
            password="fuah",
            referral="!@#$4",
            authorize_after_registration=True
        )
        if isinstance(confirmation, PendingCodeConfirmation):
            code = input("Code >>> ")
            scash = confirmation.submit(code)
            print(scash)
    except UserEmailAlreadyExists:
        print("Email already exists")


if __name__ == '__main__':
    main()
