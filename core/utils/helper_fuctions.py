import re

regex = re.compile(r'([A-Za-z\d]+[.-_])*[A-Za-z\d]+@[A-Za-z\d-]+(\.[A-Z|a-z]{2,})+')


def verify_email(email: str) -> bool:
    if re.fullmatch(regex, email):
        return True
    return False
