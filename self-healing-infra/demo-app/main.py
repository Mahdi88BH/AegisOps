import os
import psutil
import logging
from fastapi import FastAPI
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
    


# endpoint of heavly CPU Computing
@app.get("/slow-query")
async def heavly_query() -> dict:
    logger.info("Initiating highly intensive CPU-bound Computation Pipeline")

    process = psutil.Process()
    # Call cpu_percent once to set a baseline measurement point
    process.cpu_percent(interval=None)

    def fibonacci(n):
        if n <= 0: return 0
        if n == 1: return 1
        return fibonacci(n-1) + fibonacci(n-2)
        
    result = fibonacci(30)

    # Measure total CPU usage across system or current process
    process_cpu = process.cpu_percent(interval=0.1)
    system_cpu = psutil.cpu_percent(interval=0.1)

    logger.info(f"Process CPU Usage: {process_cpu}% | Overall System CPU: {system_cpu}%")

    return {"result": result}