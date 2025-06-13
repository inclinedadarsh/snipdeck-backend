from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db import create_db_and_tables
from contextlib import asynccontextmanager
from src.routes.snippets import router as snippets_router
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up...")
    create_db_and_tables()
    yield
    print("Application shutting down...")


app = FastAPI(lifespan=lifespan)

CORS_ORIGINS = os.getenv("CORS_ORIGIN", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # Uses origins from environment variable
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(snippets_router, prefix="/snippets", tags=["snippets"])


@app.get("/")
def read_root():
    return {"message": "Hello World"}
