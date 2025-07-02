from fastapi import FastAPI
from app.settings import settings
from starlette.middleware.cors import CORSMiddleware
from app.routes import api_router

app = FastAPI()

if settings.ALLOW_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.ALLOW_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)

@app.get("/", status_code=200)
async def health():
    return {"message": "What's Up? Bro!"}
