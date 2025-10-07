#!/usr/bin/env bash
set -euo pipefail

# Runs inside a venv (/opt/venv) created at build-time
export PATH="/opt/venv/bin:$PATH"
cd /app

log() { echo "[$(date -u +%FT%TZ)] $*"; }

# Optionally wire TLS env from mounted credentials dir
if [[ -d "/run/ghostlink" ]]; then
  export GL_TLS_CERT="${GL_TLS_CERT:-/run/ghostlink/ctl.crt}"
  export GL_TLS_KEY="${GL_TLS_KEY:-/run/ghostlink/ctl.key}"
  export GL_TLS_CA="${GL_TLS_CA:-/run/ghostlink/ca.crt}"
fi

pids=()

if [[ "${RUN_CONTROLLER:-1}" == "1" ]]; then
  log "starting controller (HOST=${HOST:-127.0.0.1})"
  python /app/gl_controller_metrics.py &
  pids+=($!)
else
  log "controller disabled (RUN_CONTROLLER=0)"
fi

if [[ "${RUN_PEER:-0}" == "1" ]]; then
  log "starting peer (expects sensors via psutil or /sys/class/thermal)"
  python /app/gl_peer.py &
  pids+=($!)
else
  log "peer disabled (RUN_PEER=0)"
fi

if [[ "${RUN_BRIDGE:-0}" == "1" ]]; then
  if [[ -z "${OPENAI_API_KEY:-}" ]]; then
    log "WARN: RUN_BRIDGE=1 but OPENAI_API_KEY is not set; bridge will exit."
  fi
  log "starting OpenAI bridge (127.0.0.1:7422)"
  python /app/gl_openai_bridge.py &
  pids+=($!)
else
  log "bridge disabled (RUN_BRIDGE=0)"
fi

# Wait for any process to exit; then exit with its code
status=0
for pid in "${pids[@]:-}"; do
  if ! wait "$pid"; then status=1; fi
done
exit $status
