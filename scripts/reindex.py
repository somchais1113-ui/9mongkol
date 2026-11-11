import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from app.engine import config
from app.db import initialize, reindex_all
initialize(); config.cache_clear(); print('Re-indexed',reindex_all(),'numbers')
