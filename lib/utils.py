import time


async def timer(func):
    """Times a function execution time and returns the value in milliseconds."""
    start_time = time.perf_counter()
    await func
    
    return round((time.perf_counter() - start_time) * 1000)
