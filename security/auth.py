from __future__ import annotations
import json, os
import bcrypt
from typing import Callable, List
from app.db.mysql_conn import Db
from app.services.usuario_service import UsuarioService

SESSION_FILE = ".session.json"

class Auth:
    session_user: dict | None = None  # {'username': str, 'rol': 'admin'|'gerente'|'usuario'}

    @staticmethod
    def hash_password(pwd: str) -> str:
        return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def check_password(pwd: str, hashed: str) -> bool:
        h = hashed.encode() if isinstance(hashed, str) else hashed
        return bcrypt.checkpw(pwd.encode(), h)

    @staticmethod
    def login(username: str, pwd: str) -> bool:
        row = UsuarioService.obtener_por_username(username)
        if not row:
            return False
        if not Auth.check_password(pwd, row["password_hash"]):
            return False
        Auth.session_user = {"username": row["username"], "rol": row["rol"]}
        Auth._save_session()
        return True

    @staticmethod
    def logout() -> None:
        Auth.session_user = None
        try:
            if os.path.exists(SESSION_FILE):
                os.remove(SESSION_FILE)
        except Exception:
            pass

    @staticmethod
    def load_session() -> dict | None:
        if Auth.session_user:
            return Auth.session_user
        try:
            if os.path.exists(SESSION_FILE):
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    Auth.session_user = data
                    return data
        except Exception:
            return None
        return None

    @staticmethod
    def _save_session() -> None:
        if Auth.session_user:
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump(Auth.session_user, f)

def require_role(roles: List[str]) -> Callable:
    def decorator(fn: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            user = Auth.load_session()
            if not user or user.get("rol") not in roles:
                raise PermissionError("Acceso denegado: se requiere rol " + "/".join(roles))
            return fn(*args, **kwargs)
        return wrapper
    return decorator
