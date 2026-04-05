from fastapi import FastAPI
from app.api.routers import exchanges, health, pairs, snapshots, spreads
from app.logging_config import root_logger_config


root_logger_config()

app = FastAPI()

app.include_router(exchanges.router)
app.include_router(health.router)
app.include_router(pairs.router)
app.include_router(snapshots.router)
app.include_router(spreads.router)


@app.get("/")
def root():
    return {"message": "Root directory for price observer"}

#TODO: добавить метаданные через Path, Query, Body во все ендпоинты 
# добавить все Dependencies
# limit + offset, для

