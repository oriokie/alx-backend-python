#!/usr/bin/env python3
"""Measure the runtime"""
import asyncio
import timeit
import random
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """Measure the runtime"""
    start = timeit.default_timer()
    await asyncio.gather(*(async_comprehension() for i in range(4)))
    end = timeit.default_timer()
    return end - start
