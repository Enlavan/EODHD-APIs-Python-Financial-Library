#APIs/__init__.py — backward-compatibility shim
#
# All old class names are still importable from here but trigger
# deprecation warnings pointing to the new locations.

from eodhd.APIs._shim import __getattr__  # noqa: F401
