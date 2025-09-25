import os
import bcrypt

pwd = os.getenv("PASSWORD", "admin123")  # toma desde .env o usa el default
h = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
print(h.decode())   # imprime la cadena legible
