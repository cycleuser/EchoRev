# AGENTS.md - EchoRev Project Guide

This document provides guidance for AI coding agents working in this repository.

## Project Overview

EchoRev is a Python GUI application for text direction reversal and RSA encryption/decryption. Built with PySide6 (Qt for Python) and the cryptography library.

## Build/Lint/Test Commands

### Installation
```bash
pip install -e .
# Or with user flag to avoid permission issues:
pip install -e . --user
```

### Dependencies
```bash
pip install PySide6 cryptography requests
```

### Running the Application
```bash
python -c "import echorev; echorev.main()"
```

### Building for Distribution
```bash
# Linux/macOS
python3 setup.py sdist --formats=zip
twine upload dist/*zip

# Windows
python setup.py sdist --formats=zip
twine upload dist/*zip
```

### Testing
No formal test framework is configured. Manual testing can be done by running:
```bash
python -c "import echorev; echorev.main()"
```

For testing individual modules:
```bash
python -c "from echorev import echorev; print('Module loaded successfully')"
```

### Linting/Type Checking
No linter or type checker is configured. If adding, use:
```bash
pip install ruff mypy
ruff check echorev/
mypy echorev/
```

## Code Style Guidelines

### File Headers
All Python files should start with:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

### Imports
- Group imports at the top of the file
- Standard library imports first, then third-party, then local
- Example order:
```python
import sys
import os
import re
import webbrowser

from PySide6.QtWidgets import QMainWindow, QWidget, QTextEdit
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QTranslator
from cryptography.hazmat.primitives.asymmetric import rsa, padding
```

### Naming Conventions
- **Functions/Methods**: snake_case (e.g., `generate_keys`, `load_private_key`)
- **Variables**: snake_case (e.g., `private_key_path`, `max_length`)
- **Classes**: The project uses lowercase class names for main classes (e.g., `echorev`, `echograb`) - maintain this unconventional style for consistency
- **Constants**: lowercase with underscores at module level (e.g., `version`, `date`, `dpi`)
- **Private attributes**: prefix with underscore if needed (not currently used)

### Comments
- This project uses Chinese comments extensively - continue this pattern
- Add descriptive comments for complex logic
- Example:
```python
def generate_keys(self):
    # 生成RSA密钥对 (Generate RSA key pair)
    ...
```

### Error Handling
- Use try/except blocks for operations that may fail (file I/O, network requests)
- Provide user feedback via QMessageBox for GUI errors
- Use print statements for console logging/debugging
- Example:
```python
try:
    r = requests.get(url, allow_redirects=True)
    r.raise_for_status()
except requests.exceptions.ConnectionError:
    QMessageBox.information(self, u'NetWork Error', 'Connection failed')
```

### GUI Conventions
- Use PySide6 (not PyQt5) - the project has migrated from PyQt5
- Set object names with `setObjectName()`
- Connect signals using the pattern: `widget.signal.connect(self.method)`
- Use f-strings for formatted messages in message boxes

### Code Formatting
- Use 4-space indentation
- No strict line length limit enforced
- Blank lines between logical sections
- Avoid trailing whitespace

### Encryption/Security
- RSA key size: 2048 bits
- OAEP padding with SHA256 for RSA encryption
- Chunk size for encryption: 24 bytes (for 2048-bit RSA with OAEP)
- Chunk size for decryption: 256 bytes
- Keys stored in PEM format

### File Structure
```
EchoRev/
├── echorev/
│   ├── __init__.py      # Main application code
│   ├── test.py          # Legacy test/grabber module
│   ├── testGPG.py       # Encryption helper functions
│   └── *.png            # Icon assets
├── setup.py             # Package setup
├── README.md            # Documentation
└── build.sh / build.bat # Build scripts
```

### Version Management
- Version and date are defined at the top of `echorev/__init__.py`:
```python
version = '0.1.1'
date = '2024-10-19'
```

### Key Methods Reference
- `build_ui()`: Construct the GUI layout
- `Magic()`: Handle text reversal transformations
- `MagicEncrypted()`: Encrypt text using loaded public key
- `MagicDecrypted()`: Decrypt text using loaded private key
- `generate_keys()`: Create and save RSA key pair
- `load_private_key()` / `load_public_key()`: Load existing keys

## Notes for Agents

1. When adding new GUI elements, follow the existing pattern in `build_ui()`
2. Use QMessageBox for user confirmations and error messages
3. Maintain backward compatibility with the existing key file format (PEM)
4. The `test.py` file contains legacy PyQt5 code - prefer PySide6 patterns from `__init__.py`
5. Status bar messages should include version info: `self.statusbar.showMessage('The version is ' + version ...)`