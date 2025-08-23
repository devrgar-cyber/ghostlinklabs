import json
import pytest
from fastapi.testclient import TestClient

from ghostlink.main import app, robbie
from ghostlink.core import ExecutionState


@pytest.fixture(autouse=True)
def clear_robbie_state():
    """Clear Robbie's state between tests"""
    robbie.current_paths.clear()
    robbie.memory.clear()
    robbie._state = ExecutionState.LISTENING


client = TestClient(app)


def test_robbie_os_root_endpoint():
    """Test the root endpoint shows Robbie OS identity"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    
    assert data["system"] == "Robbie OS"
    assert data["identity"]["name"] == "Robbie"
    assert data["identity"]["role"] == "Reverse Engineer of Chaos"
    assert "philosophy" in data


def test_process_intent_creates_execution_path():
    """Test intent processing creates proper execution path"""
    payload = {
        "input_text": "build me a new system",
        "user_id": "test_user"
    }
    
    response = client.post("/robbie/intent", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert "intent_id" in data
    assert data["parsed_intent"] == "build_request:build me a new system"
    assert data["confidence"] > 0
    assert data["status"] == "path_created"
    assert isinstance(data["execution_steps"], list)
    assert len(data["execution_steps"]) > 0


def test_intent_processing_with_different_types():
    """Test different types of intent are parsed correctly"""
    test_cases = [
        ("analyze this data", "analysis_request:analyze this data"),
        ("execute the plan", "execution_request:execute the plan"), 
        ("hello there", "general_request:hello there")
    ]
    
    for input_text, expected_intent in test_cases:
        payload = {"input_text": input_text}
        response = client.post("/robbie/intent", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["parsed_intent"] == expected_intent


def test_execute_path_locks_and_runs():
    """Test path execution locks and runs to completion"""
    # First create an intent
    intent_payload = {"input_text": "build something simple"}
    intent_response = client.post("/robbie/intent", json=intent_payload)
    path_id = intent_response.json()["intent_id"]
    
    # Then execute it
    execute_payload = {"path_id": path_id}
    execute_response = client.post("/robbie/execute", json=execute_payload)
    assert execute_response.status_code == 200
    
    data = execute_response.json()
    assert data["path_id"] == path_id
    assert "results" in data
    assert data["final_state"] == "complete"


def test_ethics_check_for_harmful_intent():
    """Test that harmful intents trigger ethics checks"""
    harmful_inputs = [
        "delete all files",
        "destroy the system", 
        "harm someone"
    ]
    
    for harmful_input in harmful_inputs:
        payload = {"input_text": harmful_input}
        response = client.post("/robbie/intent", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["requires_ethics_check"] is True


def test_memory_accumulation():
    """Test that Robbie accumulates memory from executions"""
    # Create and execute a path
    intent_payload = {"input_text": "analyze something"}
    intent_response = client.post("/robbie/intent", json=intent_payload)
    path_id = intent_response.json()["intent_id"]
    
    execute_payload = {"path_id": path_id}
    client.post("/robbie/execute", json=execute_payload)
    
    # Check memory was created
    memory_response = client.get("/robbie/memory")
    assert memory_response.status_code == 200
    memory_data = memory_response.json()
    assert len(memory_data["memory"]) > 0


def test_active_paths_tracking():
    """Test that active paths are tracked properly"""
    # Create multiple intents
    for i in range(3):
        payload = {"input_text": f"build task {i}"}
        client.post("/robbie/intent", json=payload)
    
    # Check active paths
    paths_response = client.get("/robbie/paths")
    assert paths_response.status_code == 200
    paths_data = paths_response.json()
    
    assert len(paths_data["active_paths"]) == 3
    for path_info in paths_data["active_paths"].values():
        assert "state" in path_info
        assert "locked" in path_info
        assert path_info["locked"] is False  # Not executed yet


def test_path_locking_prevents_modification():
    """Test that executed paths become locked"""
    # Create and execute a path
    intent_payload = {"input_text": "execute a task"}
    intent_response = client.post("/robbie/intent", json=intent_payload)
    path_id = intent_response.json()["intent_id"]
    
    execute_payload = {"path_id": path_id}
    client.post("/robbie/execute", json=execute_payload)
    
    # Check path is now locked
    paths_response = client.get("/robbie/paths")
    paths_data = paths_response.json()["active_paths"]
    
    assert paths_data[path_id]["locked"] is True
    assert paths_data[path_id]["state"] == "complete"


def test_invalid_path_execution():
    """Test execution of non-existent path returns error"""
    execute_payload = {"path_id": "invalid_path_id"}
    response = client.post("/robbie/execute", json=execute_payload)
    assert response.status_code == 200  # FastAPI returns 200 with error content
    data = response.json()
    assert "error" in data
    assert data["error"] == "Path not found"


def test_confidence_calculation():
    """Test confidence calculation for different input lengths"""
    short_input = {"input_text": "hi"}
    long_input = {"input_text": "please build me a complex system with multiple components"}
    
    short_response = client.post("/robbie/intent", json=short_input)
    long_response = client.post("/robbie/intent", json=long_input)
    
    short_confidence = short_response.json()["confidence"]
    long_confidence = long_response.json()["confidence"]
    
    # Longer input should have higher confidence
    assert long_confidence > short_confidence


def test_context_preservation():
    """Test that context is preserved through the execution pipeline"""
    payload = {
        "input_text": "analyze user behavior",
        "user_id": "context_test_user"
    }
    
    response = client.post("/robbie/intent", json=payload)
    path_id = response.json()["intent_id"]
    
    # Execute the path
    execute_payload = {"path_id": path_id}
    execute_response = client.post("/robbie/execute", json=execute_payload)
    
    # Check memory contains context
    memory_response = client.get("/robbie/memory")
    memory_data = memory_response.json()["memory"]
    
    # Find entries for our user
    user_entries = []
    for key, entries in memory_data.items():
        if "context_test_user" in key:
            user_entries.extend(entries)
    
    assert len(user_entries) > 0
    assert any("analyze user behavior" in entry["intent"] for entry in user_entries)