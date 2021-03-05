import time


async def timer(func):
    """Times a function execution time and returns the value in milliseconds."""
    start_time = time.perf_counter()
    await func
    end_time = time.perf_counter()
    
    return round((end_time - start_time) * 1000)
