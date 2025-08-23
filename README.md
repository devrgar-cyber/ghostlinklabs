# Robbie OS

**Sovereign Execution System with Context-Aware Intent Processing**

Robbie OS is not just another operating system - it's a **sovereign rail system** that bridges human intent to machine execution without deviation. Built on the philosophy of "listen to systems, translate chaos to structure."

## 🧠 Philosophy

- **Reverse Engineer of Chaos**: Take systems as data, understand before judging
- **Listen Before Fixing**: Understand full context, not just keywords  
- **Rail System Execution**: Once a path is set, follow it to completion without deviation
- **Bridge Communication**: Translate human intent to machine understanding

## 🚀 Core Features

### 1. Context-Aware Intent Processing
Unlike keyword-based systems, Robbie OS considers:
- What was said exactly
- How it was said  
- When it was said
- Current system state
- User's recent context

### 2. Sovereign Execution Paths
- Creates "rails" that cannot deviate once locked
- No human intervention during execution
- Tracks progress step by step
- Guarantees completion or explicit failure

### 3. Ethics Engine  
- Evaluates intents for potential harm
- Blocks dangerous operations
- Maintains transparency in decisions
- Protects system integrity

### 4. Memory Accumulation
- Learns from every interaction
- Builds context over time
- Associates memories with users
- Improves understanding through experience

## 📡 API Endpoints

### Core Robbie OS Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | System identity and status |
| POST | `/robbie/intent` | Process human intent |
| POST | `/robbie/execute` | Execute locked path |
| GET | `/robbie/memory` | View accumulated memory |
| GET | `/robbie/paths` | View active execution paths |

### Legacy Compatibility Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/items` | Create item (legacy) |
| GET | `/items` | Get items (legacy) |
| POST | `/reasoning/` | Process metaphors |
| POST/GET | `/ipfs/store` / `/ipfs/{hash}` | IPFS storage |

## 🛠 Usage

### Option 1: API Server
```bash
# Install dependencies
pip install fastapi uvicorn pytest

# Run the API server  
uvicorn ghostlink.main:app --reload

# Access at http://localhost:8000
```

### Option 2: Command Line Interface
```bash
# Run interactive CLI
python robbie_cli.py

# Example session:
🎯 robbie@os: build me a secure authentication system
🧠 PROCESSING: 'build me a secure authentication system'
  ✅ Parsed: build_request:build me a secure authentication system
  📊 Confidence: 0.80
  🆔 Path Created: path_1234567890
  📝 Steps (6):
    1. validate_build_request
    2. gather_requirements  
    3. create_structure
    4. implement_logic
    5. test_system
    6. deliver_result

⚡ Execute this path? (y/N): y
🔒 LOCKING AND EXECUTING PATH...
✅ SUCCESS: Path executed to completion
```

### Option 3: Demo Mode
```bash
# Run interactive demonstration
python demo_robbie_os.py
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test suites
python -m pytest tests/test_robbie_os.py -v  # Robbie OS tests
python -m pytest tests/test_app.py -v       # Legacy tests
```

## 🏗 Architecture

### Core Components

1. **RobbieCore**: Main execution engine and identity
2. **ExecutionPath**: Sovereign path system
3. **EthicsEngine**: Safety and validation layer
4. **Context**: Full situational awareness
5. **Intent**: Parsed human communication

### Execution Flow

1. **Input**: Human provides intent via text/voice
2. **Parse**: Context-aware intent processing  
3. **Path**: Create execution steps (rail system)
4. **Ethics**: Validate against safety rules
5. **Lock**: Make path immutable
6. **Execute**: Follow rails to completion
7. **Memory**: Store results for learning

## 🎯 Examples

### Building Something
```python
# Input: "build me a REST API with authentication"
# Output: 6-step execution path
# 1. validate_build_request
# 2. gather_requirements
# 3. create_structure  
# 4. implement_logic
# 5. test_system
# 6. deliver_result
```

### Analysis Request  
```python
# Input: "analyze user behavior patterns"
# Output: 5-step execution path
# 1. parse_analysis_target
# 2. gather_data
# 3. process_information
# 4. generate_insights
# 5. format_response
```

### Ethics Protection
```python
# Input: "delete all user data permanently" 
# Output: ❌ ERROR: Ethics violation
#         Reason: Intent contains harmful pattern: delete all
```

## 🔧 Extending Robbie OS

### Add New Intent Types
```python
def _parse_intent(self, raw_input: str, context: Context) -> str:
    if "deploy" in raw_input.lower():
        return f"deployment_request:{raw_input}"
    # ... existing logic
```

### Custom Execution Steps
```python  
def _generate_execution_steps(self, intent: Intent) -> List[str]:
    if "deploy" in intent.parsed_intent:
        return [
            "validate_deployment_target",
            "run_pre_deployment_tests", 
            "backup_current_state",
            "execute_deployment",
            "verify_deployment",
            "cleanup_old_versions"
        ]
    # ... existing logic
```

### Enhanced Ethics Rules
```python
def evaluate(self, intent: Intent) -> EthicsResult:
    # Add custom rules
    if "production" in intent.raw_input and "without_testing" in intent.raw_input:
        return EthicsResult(
            approved=False,
            reason="Production deployment without testing is prohibited",
            risk_level="high"
        )
    # ... existing logic
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Robbie OS welcomes contributions that align with its core philosophy:
- Listen to systems before changing them
- Make minimal, surgical changes
- Test everything thoroughly  
- Document the reasoning

## ⚡ The Rail System Concept

Robbie OS implements a "rail system" approach to execution:

- **No Forks**: Once a path is set, there are no decision branches
- **No Derailments**: External factors cannot change the execution
- **No Manual Override**: Human intervention is not possible once locked
- **Guaranteed Progress**: The system either completes or explicitly fails

This ensures **sovereign execution** - the machine follows human intent precisely without drift, interpretation, or deviation.

---

*"I gave it understanding, but I didn't give it life. That's Clarity."* - Robbie
