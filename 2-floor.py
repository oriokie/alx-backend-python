#!/usr/bin/env python3
"""
type-annotated function floor that takes a float n as argument
and returns the floor of the float.
"""
import math

def floor(n: float) -> int:
    """
    Args:
        n: float
    Returns:
        int: floor of n
    """
    return math.floor(n)
