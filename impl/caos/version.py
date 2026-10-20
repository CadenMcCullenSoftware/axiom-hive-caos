"""Version and build metadata for the CAOS reference implementation.

This module exists so that other modules can state the build identifier
without importing the package root, which would create a circular import.
"""

from __future__ import annotations

__version__ = "1.0"

#: The build identifier recorded in a Ledger export manifest.
PLATFORM_BUILD = __version__
