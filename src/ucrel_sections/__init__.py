"""Lightweight, colourised console sections, timers and inline unit tests."""

from .sections import Color, Section, TestResult, Timer, UnitTest, fmt

try:
    from ._version import __version__
except ImportError:  # pragma: no cover - only when running from an un-built checkout
    __version__ = "0.0.0"

__all__ = [
    "Color",
    "Section",
    "TestResult",
    "Timer",
    "UnitTest",
    "fmt",
    "__version__",
]
