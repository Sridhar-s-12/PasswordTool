#!/usr/bin/env python3
"""
Simple runner script for the Password Strength Analyzer & Wordlist Generator.

This script can be used to run the application without installing it.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pass_tool.gui import main
    main()
except ImportError as e:
    print("Error: Required modules not found.")
    print("Please install dependencies: pip install -r requirements.txt")
    print(f"Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error running application: {e}")
    sys.exit(1)
