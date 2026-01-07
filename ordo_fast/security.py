from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(normal_password: str, hashed_password: str):
    return pwd_context.verify(normal_password, hashed_password)
