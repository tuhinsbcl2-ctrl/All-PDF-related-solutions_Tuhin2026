"""
PDF Solutions Desktop Application
Main entry point
"""

import sys
import os

# Ensure src is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import main

if __name__ == "__main__":
    main()
