from fastapi import FastAPI
from app.api.routers import exchanges, health, pairs, snapshots, spreads, auth
from app.logging_config import root_logger_config


root_logger_config()

app = FastAPI()

app.include_router(exchanges.router)
app.include_router(health.router)
app.include_router(pairs.router)
app.include_router(snapshots.router)
app.include_router(spreads.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Root directory for price observer"}

