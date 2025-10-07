#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   bash gl_sanity_check.sh [--mode systemd|venv] [--venv-dir /path/to/ghostlink_venv_runner] [--controller-host 127.0.0.1]
#
# Exit code: 0 on PASS, 1 on FAIL, 2 on partial (warnings).

MODE=""
VENV_DIR="${HOME}/gl/ghostlink_venv_runner"
CTL_HOST="127.0.0.1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="${2:-}"; shift 2 ;;
    --venv-dir) VENV_DIR="${2:-}"; shift 2 ;;
    --controller-host) CTL_HOST="${2:-}"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

have_systemd_units() { systemctl list-unit-files | egrep -q 'ghostlink-(controller|peer|bridge)\.service'; }
have_cmd() { command -v "$1" >/dev/null 2>&1; }

PASS=0; FAIL=0; WARN=0
note() { printf "  - %s\n" "$*"; }
ok()   { echo "✓ $*"; PASS=$((PASS+1)); }
warn() { echo "⚠ $*"; WARN=$((WARN+1)); }
bad()  { echo "✗ $*"; FAIL=$((FAIL+1)); }

section() { echo; echo "== $* =="; }

section "Detecting deployment"
DETECTED_MODE=""
if [[ -z "$MODE" ]]; then
  if have_systemd_units; then DETECTED_MODE="systemd"
  elif [[ -x "${VENV_DIR}/run_venv.sh" ]]; then DETECTED_MODE="venv"
  fi
else
  DETECTED_MODE="$MODE"
fi
if [[ -z "$DETECTED_MODE" ]]; then
  bad "Cannot detect deployment mode (no systemd units and no venv runner). Use --mode."
  exit 1
fi
ok "Mode: ${DETECTED_MODE}"

section "Sockets listening (expect 7420 & 9108; 7422 if bridge)"
SS_OUT="$(ss -ltnp 2>/dev/null || true)"
echo "$SS_OUT" | egrep ':7420|:7422|:9108' || true
echo "$SS_OUT" | egrep -q ':7420' && ok "controller socket present" || bad "controller socket missing :7420"
echo "$SS_OUT" | egrep -q ':9108' && ok "metrics socket present"    || warn "metrics socket missing :9108"
echo "$SS_OUT" | egrep -q ':7422' && ok "bridge socket present"     || note "bridge not running (ok if unused)"

# Bind addresses sanity
if echo "$SS_OUT" | egrep -q '127\.0\.0\.1:9108'; then ok "/metrics bound to loopback"; else warn "/metrics not bound to loopback"; fi
if echo "$SS_OUT" | egrep -q '127\.0\.0\.1:7422'; then ok "bridge bound to loopback"; else note "bridge not present or not loopback (check firewall)"; fi

section "Metrics probe"
if have_cmd curl; then
  if curl -fsS "http://127.0.0.1:9108/metrics" | egrep -q '^ghostlink_sigma_fraction'; then
    ok "metrics reachable and exporting ghostlink_*"
  else
    warn "metrics endpoint not reachable or empty"
  fi
else
  warn "curl not found; skipping metrics probe"
fi

section "Log receipts (last 30 lines)"
if [[ "$DETECTED_MODE" == "systemd" ]] && have_cmd journalctl; then
  journalctl -u ghostlink-controller -n 30 --no-pager || true
  if journalctl -u ghostlink-controller -n 300 --no-pager | egrep -q '\[shadow\]'; then
    ok "controller printed window receipts"
  else
    warn "no window receipts seen in recent controller logs"
  fi
else
  tail -n 30 "${VENV_DIR}/.logs/controller.log" 2>/dev/null || true
  if egrep -q '\[shadow\]' "${VENV_DIR}/.logs/controller.log" 2>/dev/null; then
    ok "controller printed window receipts"
  else
    warn "no window receipts found in venv logs"
  fi
fi

section "WireGuard (optional)"
if have_cmd wg; then
  WG="$(wg show 2>/dev/null || true)"
  echo "$WG" | sed -n '1,20p'
  if echo "$WG" | egrep -q 'interface: wg0'; then ok "wg0 up"; else note "wg0 not found (ok if not using WG)"; fi
else
  note "WireGuard not installed (ok if not using WG)"
fi

section "mTLS (optional quick probe)"
# Only run if certs look present
if [[ -r /etc/ghostlink/ca.crt ]] && [[ -r /etc/ghostlink/peer1.crt ]] && [[ -r /etc/ghostlink/peer1.key ]]; then
  if have_cmd openssl; then
    set +e
    OUT=$(echo | openssl s_client -connect "${CTL_HOST}:7420" -CAfile /etc/ghostlink/ca.crt -cert /etc/ghostlink/peer1.crt -key /etc/ghostlink/peer1.key 2>/dev/null | egrep 'Verify return code|subject=' || true)
    set -e
    if [[ -n "$OUT" ]]; then
      echo "$OUT"
      ok "mTLS handshake completed (client cert accepted)"
    else
      warn "mTLS probe did not complete—check controller TLS settings"
    fi
  else
    warn "openssl not found; skipping mTLS probe"
  fi
else
  note "client certs not present at /etc/ghostlink/{peer1.crt,peer1.key,ca.crt}; skipping mTLS probe"
fi

section "Firewall posture (informational)"
if have_cmd ufw; then
  ufw status verbose || true
elif have_cmd firewall-cmd; then
  firewall-cmd --list-all || true
else
  note "No ufw or firewalld detected"
fi

section "Summary"
TOTAL=$((PASS+FAIL+WARN))
echo "Checks: $TOTAL  PASS: $PASS  WARN: $WARN  FAIL: $FAIL"
if [[ $FAIL -gt 0 ]]; then
  echo "Result: FAIL"; exit 1
elif [[ $WARN -gt 0 ]]; then
  echo "Result: PARTIAL"; exit 2
else
  echo "Result: PASS"; exit 0
fi
