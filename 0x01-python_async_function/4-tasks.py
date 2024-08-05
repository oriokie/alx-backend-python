#!/usr/bin/env python3
""" 4. Tasks """
import asyncio
from typing import List
from 3-tasks import task_wait_random

async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """
    task_wait_random is being called.


    Args:
        n: number of iterations
        max_delay: maximum wait
    Returns:
        list of random floats
    """
    delays = [task_wait_random(max_delay) for _ in range(n)]
    
    completed_delays = []
    for task in asyncio.as_completed(delays):
        completed_delays.append(await task)
    
    return completed_delays
