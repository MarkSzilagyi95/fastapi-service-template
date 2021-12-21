import uvicorn
from fastapi import FastAPI

from app.demo.api.demo import demo

app = FastAPI()

app.include_router(demo)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
