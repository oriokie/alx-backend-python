#!/usr/bin/env python3
""" 1. Let's execute multiple coroutines at the same time with async """
import asyncio
import random
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(max_delay: int = 10) -> List[float]:
    """
    Args:
        max_delay: maximum wait
    Returns:
        list of random floats
    """
    delays = [wait_random(max_delay) for i in range(max_delay)]
    return [await delay for delay in asyncio.as_completed(delays)]
