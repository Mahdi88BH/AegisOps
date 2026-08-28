import os
import time
import psutil
import logging
from fastapi import FastAPI, concurrency
from contextlib import asynccontextmanager

# Initialize logging config before creating loggers
import logging_config

# Create Named Root Logger
logger = logging.getLogger(__name__)
process_monitore = psutil.Process(os.getpid())

# Globale Variable to simuliate the leak storage
LEAK_STORAGE = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI Application Process Starting Up")
    yield
    logger.info("FastAPI Application Tearing Down")


app = FastAPI(lifespan=lifespan)


# Endpoint of Memory Leak
@app.get("/leak")
async def get_leak_memory() -> dict:
    # Acces the global Variable
    global LEAK_STORAGE

    # The RAM Consumption RSS (Resident Set Size) in MegaBytes
    current_rss_mb = process_monitore.memory_info().rss / (1024 ** 2)
    logger.info(f"Memory threshold diagnostic check | Current RAM Usage : {current_rss_mb:.2f} MB")
    
    
    # Intentionally Leak Memory For simulation Purpose
    for _ in range(100):
        LEAK_STORAGE.append(bytearray(b"mahdi") * 1000000)
    

    update_rss_mb = process_monitore.memory_info().rss / (1024 ** 2)
    logger.debug("Memory leakage progression Tracked | Update RMA Value: %.2f MD", update_rss_mb)


    return {
        "satuts": "leaked",
        "current_ram_mb": round(update_rss_mb, 2)
    }
    

def fibonacci(n):
        if n <= 0: return 0
        if n == 1: return 1
        return fibonacci(n-1) + fibonacci(n-2)

# endpoint of heavly CPU Computing
@app.get("/slow-query")
async def heavly_query() -> dict:
    logger.info("Initiating highly intensive CPU-bound Computation Pipeline")

    process = psutil.Process()
    
    # Capture CPU timing before workload
    start_time = time.perf_counter()
    start_cpu_time = process.cpu_times()

    # Offload CPU task so FastAPI event loop remains responsive
    # Use n=35 so it actually takes noticeable CPU work (~1-2 seconds)
    result = await concurrency.run_in_threadpool(fibonacci, 20)

    # Calculate CPU utilization during the work execution
    elapsed_time = time.perf_counter() - start_time
    end_cpu_time = process.cpu_times()

    user_sys_time = (end_cpu_time.user - start_cpu_time.user) + (end_cpu_time.system - start_cpu_time.system)
    
    # Process CPU usage percentage over the duration of the workload
    process_cpu = (user_sys_time / elapsed_time) * 100 if elapsed_time > 0 else 0.0
    system_cpu = psutil.cpu_percent(interval=None)

    logger.info(f"Process CPU Usage: {process_cpu:.1f}% | Overall System CPU: {system_cpu}%")

    return {"result": result}