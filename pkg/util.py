"""Utility functions."""
from __future__ import print_function
import functools

print = functools.partial(print, flush=True)
