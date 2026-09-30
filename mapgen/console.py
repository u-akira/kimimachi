"""Console encoding helpers for Windows and other locale-dependent environments."""
import sys


def configure_utf8_stdio():
    """Make CLI logs safe for Unicode output without breaking redirected streams."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")
