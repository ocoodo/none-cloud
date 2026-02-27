import uvicorn
from fastapi import FastAPI

from api.storage import router as storage_router


app = FastAPI()


app.include_router(storage_router)


if __name__ == '__main__':
    uvicorn.run(app)