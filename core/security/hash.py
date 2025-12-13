import bcrypt


class Hash:
    @staticmethod
    def bcrypt(password: str) -> str:

        salt = bcrypt.gensalt(rounds=10)
        pwd_bytes = password.encode()

        hash_password = bcrypt.hashpw(pwd_bytes, salt)
        return hash_password.decode()

    @staticmethod
    def verify(password: str, hash_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hash_password.encode())
