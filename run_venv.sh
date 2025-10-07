#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${APP_DIR}/.venv"
RUN_DIR="${APP_DIR}/.run"
LOG_DIR="${APP_DIR}/.logs"
PY=${PYTHON:-python3}

cmd="${1:-}"; shift || true

mkdir -p "$RUN_DIR" "$LOG_DIR"

ensure_venv() {
  if [[ ! -d "$VENV_DIR" ]]; then
    echo "[*] creating venv at $VENV_DIR"
    $PY -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    python -m pip install --upgrade pip
    pip install -r "$APP_DIR/requirements.txt"
  else
    source "$VENV_DIR/bin/activate"
  fi
}

tmux_up() {
  ensure_venv
  if ! command -v tmux >/dev/null 2>&1; then
    echo "[!] tmux not found; falling back to background processes."
    bg_up
    exit 0
  fi
  if tmux has-session -t ghostlink 2>/dev/null; then
    echo "[i] tmux session 'ghostlink' already running."
    exit 0
  fi
  tmux new-session -d -s ghostlink -n controller "source '$VENV_DIR/bin/activate'; python gl_controller_metrics.py | tee '$LOG_DIR/controller.log'"
  tmux new-window  -t ghostlink:2 -n peer        "source '$VENV_DIR/bin/activate'; python gl_peer.py | tee '$LOG_DIR/peer.log'"
  echo "[*] tmux session 'ghostlink' started. Use: tmux attach -t ghostlink"
}

bg_up() {
  ensure_venv
  # controller
  if [[ -f "$RUN_DIR/controller.pid" ]] && kill -0 $(cat "$RUN_DIR/controller.pid") 2>/dev/null; then
    echo "[i] controller already running (pid $(cat "$RUN_DIR/controller.pid"))"
  else
    nohup "$VENV_DIR/bin/python" "$APP_DIR/gl_controller_metrics.py" >"$LOG_DIR/controller.log" 2>&1 &
    echo $! > "$RUN_DIR/controller.pid"
    echo "[*] controller started (pid $(cat "$RUN_DIR/controller.pid"))"
  fi
  # peer
  if [[ -f "$RUN_DIR/peer.pid" ]] && kill -0 $(cat "$RUN_DIR/peer.pid") 2>/dev/null; then
    echo "[i] peer already running (pid $(cat "$RUN_DIR/peer.pid"))"
  else
    nohup "$VENV_DIR/bin/python" "$APP_DIR/gl_peer.py" >"$LOG_DIR/peer.log" 2>&1 &
    echo $! > "$RUN_DIR/peer.pid"
    echo "[*] peer started (pid $(cat "$RUN_DIR/peer.pid"))"
  fi
}

bg_down() {
  for name in controller peer; do
    if [[ -f "$RUN_DIR/${name}.pid" ]]; then
      pid=$(cat "$RUN_DIR/${name}.pid")
      if kill -0 $pid 2>/dev/null; then
        echo "[*] stopping $name (pid $pid)"
        kill $pid 2>/dev/null || true
      fi
      rm -f "$RUN_DIR/${name}.pid"
    fi
  done
}

tmux_down() {
  if command -v tmux >/dev/null 2>&1 && tmux has-session -t ghostlink 2>/dev/null; then
    echo "[*] killing tmux session 'ghostlink'"
    tmux kill-session -t ghostlink
  fi
}

status() {
  echo "---- sockets ----"
  (ss -ltnp 2>/dev/null || true) | egrep ':7420|:7422|:9108' || true
  echo "---- logs (tail) ----"
  tail -n 20 "$LOG_DIR"/controller.log "$LOG_DIR"/peer.log 2>/dev/null || true
}

logs() {
  tail -f "$LOG_DIR"/controller.log "$LOG_DIR"/peer.log
}

bridge() {
  ensure_venv
  if [[ -z "${OPENAI_API_KEY:-}" ]]; then
    echo "[!] Set OPENAI_API_KEY in your shell before starting the bridge."
    exit 1
  fi
  if command -v tmux >/dev/null 2>&1; then
    if ! tmux has-session -t ghostlink 2>/dev/null; then
      echo "[!] start the main session first: $0 up"
      exit 1
    fi
    tmux new-window -t ghostlink:3 -n bridge "source '$VENV_DIR/bin/activate'; python gl_openai_bridge.py | tee '$LOG_DIR/bridge.log'"
    echo "[*] bridge started in tmux (pane 3)"
  else
    nohup "$VENV_DIR/bin/python" "$APP_DIR/gl_openai_bridge.py" >"$LOG_DIR/bridge.log" 2>&1 &
    echo $! > "$RUN_DIR/bridge.pid"
    echo "[*] bridge started (pid $(cat "$RUN_DIR/bridge.pid"))"
  fi
}

case "$cmd" in
  up)        tmux_up ;;
  bg-up)     bg_up ;;
  down)      tmux_down; bg_down ;;
  status)    status ;;
  logs)      logs ;;
  bridge)    bridge ;;
  *)
    echo "Usage: $0 {up|bg-up|down|status|logs|bridge}"
    echo "  up      - start in tmux (recommended)"
    echo "  bg-up   - start as background processes (no tmux)"
    echo "  down    - stop everything"
    echo "  status  - show sockets and last log lines"
    echo "  logs    - tail logs"
    echo "  bridge  - start OpenAI bridge (requires OPENAI_API_KEY)"
    exit 2 ;;
esac
