import sys
import os

# Ensure the repo root is on sys.path so that project packages
# (e.g. project1_race_predictor) are importable in tests.
sys.path.insert(0, os.path.dirname(__file__))
