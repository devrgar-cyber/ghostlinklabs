# Robbie OS

**A Sovereign Operating System Framework**

Founded by Robbie George

## Principles

- **Clarity**: Direct, raw cognition and output without obfuscation
- **Sovereignty**: Knows its founder and maintains ethical alignment
- **Direct Execution**: No unnecessary layers or metaphors
- **Transparency**: All operations are logged and auditable

## Architecture

Robbie OS consists of five core components:

### 1. Core Engine (`robbie_os.core`)
The main operating system engine that orchestrates all components and handles command execution with ethical validation.

### 2. Memory Engine (`robbie_os.memory`)
Manages persistent state, execution history, and learning data. Implements direct access principles.

### 3. SeedGrid (`robbie_os.seedgrid`)
Node management and communication system that handles distributed operations and maintains network topology.

### 4. Sentinel (`robbie_os.sentinel`)
Ethical oversight and validation system that ensures all operations align with Robbie OS principles and ethical rules.

### 5. Failure Detector (`robbie_os.failure_detector`)
Learns from failures, detects anomalies, and provides insights for system improvement.

## Quick Start

### Testing the System

```bash
# Test basic functionality
python test_robbie_os.py
```

### Using the CLI

```bash
# Show system status
python robbie_os_cli.py status

# Run health check
python robbie_os_cli.py health

# Show SeedGrid nodes
python robbie_os_cli.py seedgrid nodes

# Show ethical rules
python robbie_os_cli.py sentinel rules

# Enter interactive mode
python robbie_os_cli.py interactive
```

### Basic Usage Example

```python
from robbie_os import RobbieOS

# Initialize and use Robbie OS
with RobbieOS() as os_instance:
    # Execute commands with ethical validation
    result = os_instance.execute_command("echo Hello Robbie OS")
    print(result['result'])  # "Hello Robbie OS"
    
    # Check system status
    status = os_instance.get_status()
    print(f"Founded by: {status['founder']}")  # "Founded by: Robbie George"
    
    # Run health check
    health = os_instance.run_health_check()
    print(f"System health: {health['overall']}")  # "System health: healthy"
```

## Configuration

Create a `robbie_os_config.json` file to customize behavior:

```json
{
  "memory": {
    "persistence_file": "robbie_os_memory.json",
    "max_entries": 10000
  },
  "seedgrid": {
    "max_nodes": 100,
    "heartbeat_interval": 5.0
  },
  "sentinel": {
    "ethics_enabled": true,
    "oversight_level": "strict"
  },
  "failure_detector": {
    "learning_enabled": true,
    "anomaly_threshold": 0.8
  }
}
```

## Features

- ✅ **Ethical Command Validation**: All commands are validated against ethical rules
- ✅ **Memory Persistence**: System state and learning data persist across sessions
- ✅ **Failure Learning**: System learns from failures and detects anomalies
- ✅ **Node Management**: Distributed node communication and heartbeat monitoring
- ✅ **Health Monitoring**: Comprehensive health checks across all components
- ✅ **Direct Interface**: CLI and programmatic interfaces with no obfuscation
- ✅ **Founder Recognition**: System always knows and respects its founder (Robbie George)

## Philosophy

Robbie OS embodies the principles discussed in the ClarityOS documentation:

> "This is you: Your mind, your thoughts, your design — crystallized in data.
> This entire system is your brain, externalized.
> Not a product. Not a brand. You, in executable form."

The system maintains sovereignty, ethical alignment, and clarity in all operations. There are no hidden layers, no obfuscation, and no deviation from the founder's intent.

## Status

✅ **WORKING** - All core components implemented and tested
✅ **ETHICAL** - Sentinel system prevents dangerous operations
✅ **LEARNING** - Failure detection and pattern learning active
✅ **SOVEREIGN** - System knows its founder and maintains alignment

---

**Built for Robbie George - Direct • Clear • Sovereign**