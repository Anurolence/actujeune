import sys, os
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.database import Base, engine
from app import models
Base.metadata.create_all(bind=engine)

from app.main import app
