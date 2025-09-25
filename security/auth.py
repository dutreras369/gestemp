import bcrypt
from app.db.mysql_conn import Db

class Auth:
    session_user = None

    @staticmethod
    def hash_password(pwd: str) -> bytes:
        return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

    @staticmethod
    def check_password(pwd: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(pwd.encode(), hashed)
