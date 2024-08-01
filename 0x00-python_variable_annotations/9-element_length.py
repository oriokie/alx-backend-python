#!/usr/bin/env python3
"""
Annotated function"""
from typing import Tuple, List, Iterable, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Function that takes a list of sequences as arg
    and returns a list of tuples
    """
    return [(i, len(i)) for i in lst]
