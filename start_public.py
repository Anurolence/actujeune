"""Script to start Actujeune server and expose it freely via Cloudflare Quick Tunnel."""
import subprocess
import time
import re
import urllib.request
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

VENV_PYTHON = os.path.join(BASE_DIR, ".venv", "bin", "python")
CLOUDFLARED = os.path.join(BASE_DIR, "cloudflared")

print("🇨🇲 1/3 Démarrage du serveur Actujeune...")
server_proc = subprocess.Popen(
    [VENV_PYTHON, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# Wait for server to start
server_ready = False
for _ in range(25):
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000") as res:
            if res.status == 200:
                server_ready = True
                break
    except Exception:
        time.sleep(0.4)

if not server_ready:
    print("❌ Erreur: Le serveur local n'a pas répondu.")
    server_proc.terminate()
    sys.exit(1)

print("✓ Serveur local opérationnel sur http://127.0.0.1:8000")

print("🌐 2/3 Génération du lien public gratuit Cloudflare...")
tunnel_proc = subprocess.Popen(
    [CLOUDFLARED, "tunnel", "--url", "http://127.0.0.1:8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

public_url = None
start_time = time.time()
while time.time() - start_time < 30:
    line = tunnel_proc.stdout.readline()
    if not line:
        continue
    match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
    if match:
        public_url = match.group(0)
        with open("public_url.txt", "w") as f:
            f.write(public_url.strip() + "\n")
        print("\n" + "="*60)
        print(f"🎉 LIEN PUBLIC ACTUJEUNE : {public_url}")
        print("="*60 + "\n")
        break

if not public_url:
    print("❌ Impossible de récupérer l'URL du tunnel.")
    server_proc.terminate()
    tunnel_proc.terminate()
    sys.exit(1)

# Keep processes alive
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    print("\nArrêt des services...")
    server_proc.terminate()
    tunnel_proc.terminate()
