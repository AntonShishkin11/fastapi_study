from passlib.hash import pbkdf2_sha256

class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pbkdf2_sha256.verify(password, hashed_password)
