from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# For generating models
from db.database import engine
from db import models
# ----------------
from routers import user, post, comment
# For auth
from auth import authentication
# For Cors
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(authentication.router)
# For CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Generating models
models.Base.metadata.create_all(engine)
app.mount("/images", StaticFiles(directory='images'), name="images ")
