# flake8: noqa

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    docs_url="/api/_/docs",
    openapi_url="/api/_/openapi.json",
    redoc_url="/api/_/redoc",
)


class OkResponse(BaseModel):
    ok: bool = False


@app.get("/api")
def handle_api() -> OkResponse:
    return OkResponse(ok=True)


# ~~~~~~~~ MOUNT YOUR API BELOW HERE ~~~~~~~~

from app_alexander_sidorov.api.v1 import app as api_alexander_sidorov

app.mount("/api/alexander_sidorov", api_alexander_sidorov)
