import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from db import create_tables
import logging
from fastapi.middleware.cors import CORSMiddleware
from routers import users_router, posts_router, tags_router
from fastapi.staticfiles import StaticFiles


# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

app = FastAPI()

# Include routers
app.include_router(users_router)
app.include_router(posts_router)
app.include_router(tags_router)

app.mount("/static", StaticFiles(directory="uploads"), name="static")

# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await create_tables()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)