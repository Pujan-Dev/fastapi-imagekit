from fastapi import FastAPI

from core_features.routers import router
from database.database import Base, engine
from database import models  # noqa: F401

app = FastAPI(title="Insta Like Backend")
app.include_router(router)


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"app": "Insta like backend", "status": "running"}
