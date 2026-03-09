from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
import app.db.db_queries as dbq
from app.api.schemas import Snapshot, SpreadOut, InputPairs, PairOut, PostSnapshotOut
from datetime import datetime
from logging import getLogger
from app.services.snapshot_service import run_and_save_snapshot

logger = getLogger(__name__)

def app_creator():
    app = FastAPI()
    return app

app = app_creator()

@app.get("/")
def root():
    return {"message": "Root endpoint of price observer"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
    

@app.get("/ready")
def db_health_check():
    db_ok = dbq.db_health_check()
    if db_ok:
        return {
                "status": "ok",
                "db": "reachable"
                }
    raise HTTPException(status_code=503,
                        detail= {"status": "error", "db": "unreachable"})
    

@app.get("/pairs", response_model=list[PairOut])
def get_pairs():
    return dbq.get_all_pairs()


@app.get("/pairs/history", response_model= list[Snapshot])
def get_pair_history(base: str, quote: str,
                     start: datetime | None = None, end: datetime | None = None,
                     exchange: str | None = None
                     ):
    
    if base == quote:
        raise HTTPException(status_code=400, detail="The base and quote cannot be same")

    if start is not None and end is not None:
        if start > end:
            raise HTTPException(status_code=400, detail="starttime cannot be greater then endtime")

    return dbq.get_pair_timeseries(base, quote, start=start, end=end, exchange=exchange)

    
@app.get("/exchanges")
def get_exchanges():
    return dbq.get_all_exchanges()
    

@app.get("/last-snapshot", response_model=list[Snapshot])
def get_last_snapshot():
    return dbq.get_latest_snapshot()

@app.get("/spreads/{snapshot_id}", response_model=list[SpreadOut])
def get_snapshot_spreads(snapshot_id: int):
    return dbq.get_snapshot_spreads(snapshot_id)


@app.post("/post-snapshot", response_model=PostSnapshotOut)
def post_new_snapshot(pairs: InputPairs):
    result = run_and_save_snapshot(pairs.pairs)
    if result:
        logger.info(f"New snapshot with id: {result['snapshot_id']} saved, {result['rows_count']} records has been added")
    else:
        logger.warning("0 rows has been inserted")
    return result



