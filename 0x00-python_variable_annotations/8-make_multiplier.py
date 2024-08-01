#!/usr/bin/env python3
"""
type-annotated function make_multiplier that takes a
float multiplier as argument and returns a function
that multiplies a float by multiplier.
"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """THe function"""
    def multi_func(value: float) -> float:
        """the multiplier function"""
        return value * multiplier
    return multi_func
