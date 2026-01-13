#!/usr/bin/env python3
"""
Backward compatibility wrapper for script4_legacy.py

This maintains the old interface while using the new modular structure.
The original monolithic script has been refactored into the expense_tracker package.

For the new modular approach, use: python -m expense_tracker
"""

import sys
import warnings

# Warn users about using the legacy interface
warnings.warn(
    "script4.py is now a compatibility wrapper. "
    "Please use 'python -m expense_tracker' for the modular version.",
    DeprecationWarning,
    stacklevel=2
)

# Import and run the new modular main
from expense_tracker.main import main

if __name__ == '__main__':
    main()
