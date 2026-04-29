import sys
import os

# Allow pytest to find modules inside src/ from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))