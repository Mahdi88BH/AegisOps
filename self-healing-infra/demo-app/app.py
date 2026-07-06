from fastapi import FastAPI
import sys

# Globale Variable to simuliate the leak storage
LEAK_STORAGE = []

app = FastAPI()


# endpoint of Memory Leak
@app.get("/leak")
def get_leak_memory() -> None:
    # Acces the global Variable
    global LEAK_STORAGE
    # Increase storage of RAM
    for _ in range(100):
        LEAK_STORAGE.append(bytearray(b"mahdi") * 1000000)
    # Get the current size
    print(sys.getsizeof(LEAK_STORAGE))



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


