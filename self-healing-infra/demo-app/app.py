from fastapi import FastAPI
from logging_config import logger_root
import sys

# Globale Variable to simuliate the leak storage
LEAK_STORAGE = []

app = FastAPI()


# endpoint of Memory Leak
@app.get("/leak")
def get_leak_memory() -> None:
    # Acces the global Variable
    global LEAK_STORAGE
    storage_gb = sys.getsizeof(LEAK_STORAGE) / 1024**3
    storage = round(storage_gb, 2)
    logger_root.debug(f"The current size of consumming memory {storage}")
    # Increase storage of RAM
    for _ in range(100):
        LEAK_STORAGE.append(bytearray(b"mahdi") * 1000000)
    logger_root.debug(f"The Storage Increasing to => {storage}")



# endpoint of heavly CPU usage
@app.get("/slow-query")
def heavly_query() -> None:
    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1
        return fibonacci(n-1) + fibonacci(n-2)
        
    fibonacci(10)


