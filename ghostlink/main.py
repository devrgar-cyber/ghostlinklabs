import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from .storage import MockIPFS
from .reasoning import process_metaphors
from .core import RobbieCore

app = FastAPI(
    title="Robbie OS",
    description="Sovereign execution system with context-aware intent processing",
    version="1.0.0"
)

# Initialize core systems
ipfs = MockIPFS()
robbie = RobbieCore()
items: list[dict] = []


class Item(BaseModel):
    name: str
    value: int


class TextInput(BaseModel):
    text: str


class DataInput(BaseModel):
    data: str


class IntentInput(BaseModel):
    """Input for Robbie OS intent processing"""
    input_text: str
    user_id: str = "robbie"
    context: Dict[str, Any] = {}


class ExecutionRequest(BaseModel):
    """Request to execute a locked path"""
    path_id: str


@app.get("/")
def root():
    """Robbie OS status and identity"""
    return {
        "system": "Robbie OS",
        "identity": robbie.identity,
        "status": robbie.get_system_state(),
        "philosophy": "Listen to systems, translate chaos to structure"
    }


@app.post("/robbie/intent")
def process_intent(request: IntentInput) -> Dict[str, Any]:
    """
    Process human intent with full context awareness
    
    This is the core of Robbie OS - understanding human intent
    not through keywords, but through full context analysis
    """
    try:
        intent = robbie.process_input(request.input_text, request.user_id)
        path = robbie.create_execution_path(intent)
        
        return {
            "intent_id": path.path_id,
            "parsed_intent": intent.parsed_intent,
            "confidence": intent.confidence,
            "requires_ethics_check": intent.requires_ethics_check,
            "execution_steps": path.steps,
            "status": "path_created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/robbie/execute")
def execute_path(request: ExecutionRequest) -> Dict[str, Any]:
    """
    Execute a sovereign path without deviation
    
    Once locked, the path follows rails to completion
    """
    try:
        result = robbie.lock_and_execute_path(request.path_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/robbie/memory")
def get_memory() -> Dict[str, Any]:
    """Get Robbie's accumulated memory"""
    return {"memory": robbie.memory}


@app.get("/robbie/paths")
def get_active_paths() -> Dict[str, Any]:
    """Get all current execution paths"""
    paths_info = {}
    for path_id, path in robbie.current_paths.items():
        paths_info[path_id] = {
            "state": path.state.value,
            "current_step": path.current_step,
            "total_steps": len(path.steps),
            "locked": path.locked,
            "intent": path.intent.raw_input
        }
    return {"active_paths": paths_info}


# Legacy endpoints for backward compatibility
@app.post("/items")
def create_item(item: Item) -> dict:
    data = item.model_dump()
    data_str = json.dumps(data)
    data_hash = ipfs.store(data_str)
    stored = {**data, "hash": data_hash}
    items.append(stored)
    return stored


@app.get("/items")
def get_items() -> list[dict]:
    return items


@app.post("/reasoning/")
def reasoning_endpoint(text: TextInput) -> dict:
    processed = process_metaphors(text.text)
    return {"processed": processed}


@app.post("/ipfs/store")
def ipfs_store(data: DataInput) -> dict:
    cid = ipfs.store(data.data)
    return {"cid": cid}


@app.get("/ipfs/{data_hash}")
def ipfs_get(data_hash: str) -> dict:
    data = ipfs.retrieve(data_hash)
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return {"data": data}
