from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime

from schemas import PickupRequest

# Database helpers are provided by the environment
# - db: Mongo database handle
# - create_document(collection_name, data): inserts document with auto timestamps
# - get_documents(collection_name, filter_dict=None, limit: int = 50): queries documents
from database import db, create_document, get_documents  # type: ignore

app = FastAPI(title="SRKLAUNDRY API", version="1.0.0")

# CORS (open for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"service": "SRKLAUNDRY API", "status": "ok", "time": datetime.utcnow().isoformat() + "Z"}


@app.get("/test")
async def test_connection():
    try:
        # Perform a simple ping by listing collections
        _ = await db.list_collection_names()
        return {"ok": True, "database": str(db.name)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")


@app.post("/pickup")
async def create_pickup(request: PickupRequest):
    try:
        data = request.model_dump()
        doc = await create_document("pickuprequest", data)
        return {"success": True, "data": doc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create pickup request: {e}")


@app.get("/pickup")
async def list_pickups(limit: int = 50, status: Optional[str] = None):
    try:
        filter_dict = {"status": status} if status else {}
        docs = await get_documents("pickuprequest", filter_dict=filter_dict, limit=limit)
        return {"success": True, "count": len(docs), "data": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch pickup requests: {e}")
