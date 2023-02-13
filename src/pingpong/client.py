from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.pingpong.producer import FibonacciRpcClient

app = FastAPI(swagger_ui_parameters={"displayRequestDuration": True})


fibonacci_rpc = FibonacciRpcClient()


@app.get("/")
def to_docs():
    return RedirectResponse("/docs")


@app.get("/fibonacci")
async def fibonacci(x: int = 10):
    to_send = dict(x=x)
    response = fibonacci_rpc.call(to_send)
    return response
