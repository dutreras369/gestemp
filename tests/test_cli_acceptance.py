import subprocess

def run_cli(cmd):
    return subprocess.run(["python","main.py"]+cmd.split(),
                          capture_output=True, text=True)

def test_ping_db():
    out = run_cli("ping-db")
    assert "Conexión OK" in out.stdout

def test_auth_and_whoami():
    # login (usar seed admin/admin123)
    out = run_cli("auth login --username admin --password admin123")
    assert "Login correcto" in out.stdout or "✅" in out.stdout
    out2 = run_cli("auth whoami")
    assert "admin" in out2.stdout
