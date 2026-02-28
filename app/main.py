import uvicorn
from fastapi import FastAPI

from database import init_db
from api.storage import router as storage_router


app = FastAPI()


app.include_router(storage_router)


@app.on_event('startup')
async def startup():
    await init_db()


if __name__ == '__main__':
    uvicorn.run(app)