#!/usr/bin/env python3
import sys
from pathlib import Path

# Test the import
try:
    from ui.components.styles import get_custom_css
    print("✓ Import successful!")
    print(f"get_custom_css function: {get_custom_css}")
    css = get_custom_css()
    print(f"CSS length: {len(css)} characters")
except Exception as e:
    print(f"✗ Import failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
