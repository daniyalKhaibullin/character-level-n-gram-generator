# run_experiment.py (Initial part)
import os
from src.pipeline import create_data_dir, initialize_gutenberg_cache

# --- Data Initialization ---
# 1. Ensure the /data directory exists
create_data_dir()

# 2. Initialize the Gutenberg cache (long running, one-time task)
initialize_gutenberg_cache()

# ... rest of the experiment setup