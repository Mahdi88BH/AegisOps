# Import standard library modules for OS interactions and execution time tracking
import os
import time

# Import third-party libraries for monitoring system resources (RAM/CPU) and API development
import psutil
import logging
from fastapi import FastAPI, concurrency
from contextlib import asynccontextmanager

# Initialize custom logging configuration before creating individual loggers
import logging_config

#
from opentelemetry_config import CPU_Usage, RAM_Usage

# Create a module-level logger using the current module's name
logger = logging.getLogger(__name__)

# Track the current running Python process (used for measuring RAM and CPU usage)
process_monitore = psutil.Process(os.getpid())

# Global in-memory list used to simulate a persistent memory leak
LEAK_STORAGE = []


# Manage application setup (startup) and teardown (shutdown) events
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("FastAPI Application Process Starting Up")
    yield  # Application runs while sitting at this yield point
    logger.info("FastAPI Application Tearing Down")


# Recursive CPU-intensive function to compute the N-th Fibonacci number
def fibonacci(n):
    if n <= 0: return 0
    if n == 1: return 1
    return fibonacci(n-1) + fibonacci(n-2)


# Instantiate the main FastAPI application with the lifespan manager defined above
app = FastAPI(lifespan=lifespan)


# Endpoint designed to simulate progressive memory leaks
@app.get("/leak")
async def get_leak_memory() -> dict:
    # Access the global list so memory stays allocated in heap across requests
    global LEAK_STORAGE

    # Get initial Resident Set Size (RSS) memory consumption converted from Bytes to MB
    current_rss_mb = process_monitore.memory_info().rss / (1024 ** 2)
    logger.info(f"Memory threshold diagnostic check | Current RAM Usage : {current_rss_mb:.2f} MB")
    
    # Intentionally allocate ~500 MB of data to the global array to mimic a leak
    for _ in range(100):
        LEAK_STORAGE.append(bytearray(b"mahdi") * 1000000)
    
    # Measure memory usage again after the allocation
    update_rss_mb = process_monitore.memory_info().rss / (1024 ** 2)
    logger.debug("Memory leakage progression Tracked | Update RMA Value: %.2f MD", update_rss_mb)

    # Set Scraper Metric
    RAM_Usage.set(update_rss_mb, {"endpoint": "/leak"})

    # Return updated RAM usage in Megabytes
    return {
        "RAM": round(update_rss_mb, 2)
    }
    

# Endpoint designed to simulate high CPU workload
@app.get("/slow-query")
async def heavly_query() -> dict:
    logger.info("Initiating highly intensive CPU-bound Computation Pipeline")

    process = psutil.Process()
    
    # Capture wall-clock time and process CPU times prior to starting execution
    start_time = time.perf_counter()
    start_cpu_time = process.cpu_times()

    # Offload synchronous CPU task to a background worker thread so main event loop isn't blocked
    result = await concurrency.run_in_threadpool(fibonacci, 20)

    # Measure time elapsed and CPU time used after completing the calculation
    elapsed_time = time.perf_counter() - start_time
    end_cpu_time = process.cpu_times()

    # Sum total CPU execution time spent in both user mode and system mode
    user_sys_time = (end_cpu_time.user - start_cpu_time.user) + (end_cpu_time.system - start_cpu_time.system)
    
    # Calculate process-specific CPU load percentage relative to wall-clock time
    process_cpu = (user_sys_time / elapsed_time) * 100 if elapsed_time > 0 else 0.0
    
    # Capture current overall system-wide CPU usage percentage
    system_cpu = psutil.cpu_percent(interval=None)

    logger.info(f"Process CPU Usage: {process_cpu:.1f}% | Overall System CPU: {system_cpu}%")

    # Set Scraper Metric
    RAM_Usage.set(system_cpu, {"endpoint": "/slow-query"})

    # Return Process CPU utilization
    return {"CPU": system_cpu}