import uvicorn
import os
from routes.api import app  # noqa: F401

if __name__ == "__main__":

    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    if HOST is None:
        HOST = "127.0.0.1"
    if PORT is None:
        PORT = 8000    
    PORT = int(PORT)
    
    # web launch demo
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)