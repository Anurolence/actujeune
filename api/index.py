import sys, os
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
print(f"ROOT={ROOT} cwd={os.getcwd()} files={os.listdir(ROOT)[:20]}")
from app.main import app
