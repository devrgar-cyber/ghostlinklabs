# GhostLink — A Sovereign AI Framework

GhostLink is a sovereign AI framework with symbolic reasoning and diagnostic tools.

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/devrgar-cyber/ghostlinklabs.git
cd ghostlinklabs

# Install in editable mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### Using pip (when published)

```bash
pip install ghostlink
```

## Virtual Environment Runner

This folder lets you run GhostLink **locally** inside a Python virtualenv (no system services).

## Quickstart
```bash
# unpack this folder somewhere, then:
cd ghostlink_venv_runner

# start in tmux (creates .venv and installs deps on first run)
bash run_venv.sh up

# watch logs (in tmux) or:
bash run_venv.sh logs

# check status (listening sockets + last log lines)
bash run_venv.sh status

# stop everything
bash run_venv.sh down
```

## OpenAI bridge (optional)
```bash
export OPENAI_API_KEY=sk-...
export GL_MODEL=gpt-4.1-mini
bash run_venv.sh bridge
```

## Notes
- Controller listens on 127.0.0.1:7420 and exposes Prometheus metrics at 127.0.0.1:9108/metrics.
- Peer streams real machine temperature at 1 Hz; if no sensors are found, it logs an error and keeps trying.
- All logs go under `.logs/`; pids (non-tmux mode) under `.run/`.

## Package Structure

The `ghostlink` package includes:
- **core**: Core symbolic reasoning components
- **diagnostic**: Diagnostic and analysis tools
- **runtime**: Runtime execution environment
- **automation**: Automation and orchestration tools
- **tools**: Utility tools and helpers
- **docs**: Documentation and specifications

## Development

### Running Tests

```bash
# Install test dependencies
pip install -e ".[test]"

# Run tests
pytest tests/
```

### Code Quality

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Format code
black ghostlink/

# Lint code
ruff check ghostlink/
```

## License

Proprietary - See LICENSE file for details.
