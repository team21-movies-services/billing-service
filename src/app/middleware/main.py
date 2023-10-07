import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.middleware.request_id import RequestIdHeaderMiddleware

logger = logging.getLogger(__name__)

origins = ["http://localhost:8000"]


def setup_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_middleware(RequestIdHeaderMiddleware)
