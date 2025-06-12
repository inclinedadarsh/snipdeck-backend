from fastapi import FastAPI
from src.db import create_db_and_tables
from contextlib import asynccontextmanager
from src.routes.snippets import router as snippets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up...")
    create_db_and_tables()
    yield
    print("Application shutting down...")


app = FastAPI(lifespan=lifespan)

app.include_router(snippets_router, prefix="/snippets", tags=["snippets"])


@app.get("/")
def read_root():
    return {"message": "Hello World"}
