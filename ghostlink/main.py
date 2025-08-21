import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .storage import MockIPFS
from .reasoning import process_metaphors
from .solharmonics import (
    route_pack,
    summarize,
    build_deeplink,
    build_web_fallback,
    return_payload,
)

app = FastAPI(title="GhostLink")

ipfs = MockIPFS()
items: list[dict] = []


class Item(BaseModel):
    name: str
    value: int


class TextInput(BaseModel):
    text: str


class DataInput(BaseModel):
    data: str


class HandoffInput(BaseModel):
    text: str


class DoneInput(BaseModel):
    pack: str
    status: str
    utterance: str | None = None


@app.post("/items")
def create_item(item: Item) -> dict:
    data = item.dict()
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


@app.post("/handoff")
def handoff(req: HandoffInput) -> dict:
    pack = route_pack(req.text)
    summary = summarize(req.text)
    deep_link = build_deeplink(pack, summary)
    fallback = build_web_fallback(pack)
    return {"pack": pack, "deep_link": deep_link, "fallback": fallback}


@app.post("/done")
def done(req: DoneInput) -> dict:
    payload = return_payload(req.pack, utterance=req.utterance or "")
    payload["status"] = req.status
    payload["pack"] = req.pack
    return payload
