#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   sudo bash gl_update_and_restart.sh [--mode systemd|venv] [--venv-dir /path/to/ghostlink_venv_runner]
# Defaults:
#   --mode systemd   (if systemd units detected)
#   --mode venv      (if run_venv.sh detected and no systemd units)
#
# It will:
#   1) Update OS packages via apt/dnf/yum
#   2) Restart GhostLink (systemd: controller/peer/bridge; venv: down/up or bridge restart)
#   3) Print health checks (sockets & last log lines)

MODE=""
VENV_DIR="${HOME}/gl/ghostlink_venv_runner"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="${2:-}"; shift 2 ;;
    --venv-dir) VENV_DIR="${2:-}"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

need_root() {
  if [[ $EUID -ne 0 ]]; then
    echo "Please run as root: sudo $0 $*" >&2
    exit 1
  fi
}

pkg_update() {
  echo "[*] Updating OS packages..."
  if command -v apt-get >/dev/null 2>&1; then
    DEBIAN_FRONTEND=noninteractive apt-get update -y
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
  elif command -v dnf >/dev/null 2>&1; then
    dnf -y upgrade
  elif command -v yum >/dev/null 2>&1; then
    yum -y update
  else
    echo "[!] No supported package manager found (apt/dnf/yum). Skipping OS updates."
  fi
  echo "[✓] OS packages updated."
}

have_systemd_units() {
  systemctl list-unit-files | egrep -q 'ghostlink-(controller|peer|bridge)\.service'
}

restart_systemd() {
  echo "[*] Restarting GhostLink systemd services..."
  systemctl daemon-reload || true
  systemctl restart ghostlink-controller.service
  systemctl restart ghostlink-peer.service || true
  systemctl restart ghostlink-bridge.service || true
  echo "[*] Status (first 15 lines each):"
  systemctl --no-pager --full status ghostlink-controller.service | sed -n '1,15p' || true
  systemctl --no-pager --full status ghostlink-peer.service       | sed -n '1,15p' || true
  systemctl --no-pager --full status ghostlink-bridge.service     | sed -n '1,15p' || true
}

restart_venv() {
  if [[ ! -x "${VENV_DIR}/run_venv.sh" ]]; then
    echo "[!] Venv runner not found at ${VENV_DIR}/run_venv.sh"
    exit 2
  fi
  echo "[*] Restarting GhostLink venv at ${VENV_DIR} ..."
  bash "${VENV_DIR}/run_venv.sh" down || true
  bash "${VENV_DIR}/run_venv.sh" up
  echo "[*] Venv status:"
  bash "${VENV_DIR}/run_venv.sh" status || true
}

health_checks() {
  echo "---- Sockets (expect 7420 & 9108; 7422 if bridge) ----"
  ss -ltnp | egrep ':7420|:7422|:9108' || true
  echo "---- Metrics probe (localhost) ----"
  curl -s http://127.0.0.1:9108/metrics | head -n 10 || echo "[i] metrics not reachable locally (expected if controller stopped)"
  echo "---- Recent controller logs ----"
  if command -v journalctl >/dev/null 2>&1 && have_systemd_units; then
    journalctl -u ghostlink-controller -n 30 --no-pager || true
  else
    tail -n 30 "${VENV_DIR}/.logs/controller.log" 2>/dev/null || true
  fi
}

main() {
  need_root
  pkg_update

  DETECTED_MODE=""
  if [[ -z "$MODE" ]]; then
    if have_systemd_units; then DETECTED_MODE="systemd"
    elif [[ -x "${VENV_DIR}/run_venv.sh" ]]; then DETECTED_MODE="venv"
    fi
  else
    DETECTED_MODE="$MODE"
  fi

  case "$DETECTED_MODE" in
    systemd) restart_systemd ;;
    venv)    restart_venv ;;
    *) echo "[!] Could not detect deployment mode. Use: --mode systemd|venv"; exit 2 ;;
  esac

  health_checks
  echo "[✓] Updates applied and GhostLink restarted."
}

main "$@"
