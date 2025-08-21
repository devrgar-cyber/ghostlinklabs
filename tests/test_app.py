import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient

from ghostlink.main import app, ipfs, items


@pytest.fixture(autouse=True)
def clear_state():
    items.clear()
    ipfs.storage.clear()


client = TestClient(app)


def test_post_items_stores_data():
    payload = {"name": "item1", "value": 42}
    response = client.post("/items", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "item1"
    assert "hash" in data

    items_resp = client.get("/items")
    assert items_resp.status_code == 200
    items_data = items_resp.json()
    assert len(items_data) == 1
    assert items_data[0]["hash"] == data["hash"]

    ipfs_resp = client.get(f"/ipfs/{data['hash']}")
    assert ipfs_resp.status_code == 200
    assert ipfs_resp.json()["data"] == json.dumps(payload)


def test_symbolic_reasoning():
    resp = client.post("/reasoning/", json={"text": "Life and love through darkness"})
    assert resp.status_code == 200
    assert resp.json()["processed"] == "journey and light through adversity"


def test_ipfs_store_and_retrieve():
    store_resp = client.post("/ipfs/store", json={"data": "hello"})
    assert store_resp.status_code == 200
    cid = store_resp.json()["cid"]

    get_resp = client.get(f"/ipfs/{cid}")
    assert get_resp.status_code == 200
    assert get_resp.json()["data"] == "hello"


def test_handoff_and_done_flow():
    # Utterance mapping to DOWNSHIFT pack
    utterance = "I feel very tired and can't sleep"
    handoff_resp = client.post("/handoff", json={"text": utterance})
    assert handoff_resp.status_code == 200
    data = handoff_resp.json()
    assert data["pack"] == "DOWNSHIFT"
    assert data["deep_link"].startswith("solharmonics://run?pack=DOWNSHIFT")
    assert data["fallback"].endswith("pack=DOWNSHIFT")

    done_resp = client.post("/done", json={"pack": "DOWNSHIFT", "status": "complete", "utterance": utterance})
    assert done_resp.status_code == 200
    done_data = done_resp.json()
    assert done_data["pack"] == "DOWNSHIFT"
    assert "mirror" in done_data
    assert "move" in done_data
    assert done_data["move"].startswith("kill screens")
