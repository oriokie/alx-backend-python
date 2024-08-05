#!/usr/bin/env python3
""" 2. Measure the runtime """
import asyncio
import random
import time
wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int = 10, max_delay: int = 5) -> float:
    """
    Args:
        n: number of iterations
        max_delay: maximum wait
    Returns:
        time elapsed
    """
    start = time.time()
    asyncio.run(wait_n(n, max_delay))
    end = time.time()
    return (end - start) / n
