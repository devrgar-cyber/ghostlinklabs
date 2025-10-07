#!/usr/bin/env bash
set -euo pipefail

# Orchestrates a systemd or venv install and runs hardening/sanity as requested.
# Usage:
#   sudo bash install.sh --systemd [--harden] [--wg] [--mtls]
#   bash install.sh --venv
#
# Flags:
#   --systemd    Install controller+peer (and optionally bridge) as services
#   --venv       Unpack venv runner to ~/ghostlink_venv_runner and start it
#   --docker     Unpack container ctx (no run)
#   --harden     Apply firewall hardening (loopback bindings, minimal allowlist)
#   --wg         WireGuard bootstrap notes (prints configs; no auto peer add)
#   --mtls       Generate mTLS certs (CA/server/client) under /etc/ghostlink
#   --bridge     Enable bridge service (requires OPENAI_API_KEY set later)
#   --no-sanity  Skip final sanity check

MODE=""
HARDEN=0
WG=0
MTLS=0
BRIDGE=0
RUN_SANITY=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --systemd) MODE="systemd"; shift ;;
    --venv) MODE="venv"; shift ;;
    --docker) MODE="docker"; shift ;;
    --harden) HARDEN=1; shift ;;
    --wg) WG=1; shift ;;
    --mtls) MTLS=1; shift ;;
    --bridge) BRIDGE=1; shift ;;
    --no-sanity) RUN_SANITY=0; shift ;;
    *) echo "Unknown arg: $1"; exit 2 ;;
  esac
done

need_root() { if [[ $EUID -ne 0 ]]; then echo "Run as root: sudo $0 $*"; exit 1; fi; }
have() { command -v "$1" >/dev/null 2>&1; }

do_systemd() {
  need_root
  echo "[*] Installing automation config via Ansible-like copier"
  # If automation bundle present, use it; otherwise unpack minimal pkg
  if [[ -f ghostlink_automation_cfg.tgz ]]; then
    tar xzf ghostlink_automation_cfg.tgz
    pushd ghostlink_automation_cfg >/dev/null
    # Manual install without Ansible: copy files into place
    useradd --system --home /opt/ghostlink --shell /usr/sbin/nologin ghostlink 2>/dev/null || true
    install -d -o ghostlink -g ghostlink /opt/ghostlink
    # Controller (env-driven), peer, bridge
    cp -f gl_controller_metrics_env.py /opt/ghostlink/gl_controller_metrics.py
    cp -f gl_peer.py /opt/ghostlink/gl_peer.py
    cp -f gl_openai_bridge.py /opt/ghostlink/gl_openai_bridge.py
    chown ghostlink:ghostlink /opt/ghostlink/*.py
    # Env
    install -d -m 0755 /etc/default
    if [[ ! -f /etc/default/ghostlink ]]; then
      cp -f ghostlink.env /etc/default/ghostlink
      chown root:ghostlink /etc/default/ghostlink
      chmod 640 /etc/default/ghostlink
    fi
    # Units
    cp -f ansible/roles/ghostlink/templates/ghostlink-controller.service.j2 /etc/systemd/system/ghostlink-controller.service
    cp -f ansible/roles/ghostlink/templates/ghostlink-peer.service.j2       /etc/systemd/system/ghostlink-peer.service
    cp -f ansible/roles/ghostlink/templates/ghostlink-bridge.service.j2     /etc/systemd/system/ghostlink-bridge.service
    systemctl daemon-reload
    systemctl enable ghostlink-controller ghostlink-peer
    systemctl restart ghostlink-controller || true
    systemctl restart ghostlink-peer || true
    if [[ $BRIDGE -eq 1 ]]; then
      systemctl enable --now ghostlink-bridge || true
    fi
    popd >/dev/null
  else
    echo "[!] ghostlink_automation_cfg.tgz missing."
    exit 1
  fi
}

do_venv() {
  echo "[*] Installing virtual environment runner in ~/ghostlink_venv_runner"
  tar xzf ghostlink_venv_runner.tgz -C ~/
  pushd ~/ghostlink_venv_runner >/dev/null
  bash run_venv.sh up
  bash run_venv.sh status || true
  popd >/dev/null
}

do_docker() {
  echo "[*] Unpacking Docker context (build manually)"
  tar xzf ghostlink_container_ctx.tgz
  echo "Next:"
  echo "  cd ghostlink_container_ctx && docker build -t ghostlink:0.1 . && docker compose up -d"
}

do_harden() {
  need_root
  if [[ -f ghostlink_port_hardening.sh ]]; then
    bash ghostlink_port_hardening.sh apply
  else
    echo "[!] hardening script not found."
  fi
}

do_wg() {
  need_root
  if [[ -d ghostlink_automation_cfg/bootstrap ]]; then
    bash ghostlink_automation_cfg/bootstrap/gl_wireguard_bootstrap.sh controller || true
  else
    echo "[!] WG bootstrap not found."
  fi
}

do_mtls() {
  need_root
  if [[ -d ghostlink_automation_cfg/bootstrap ]]; then
    bash ghostlink_automation_cfg/bootstrap/gl_tls_bootstrap.sh /etc/ghostlink
  else
    echo "[!] TLS bootstrap not found."
  fi
}

case "$MODE" in
  systemd) do_systemd ;;
  venv) do_venv ;;
  docker) do_docker ;;
  *) echo "Choose a mode: --systemd | --venv | --docker"; exit 2 ;;
esac

[[ $HARDEN -eq 1 ]] && do_harden
[[ $WG -eq 1      ]] && do_wg
[[ $MTLS -eq 1    ]] && do_mtls

if [[ $RUN_SANITY -eq 1 ]]; then
  echo "[*] Running sanity check"
  if [[ -f gl_sanity_check.sh ]]; then
    bash gl_sanity_check.sh || true
  else
    echo "[!] sanity script not found."
  fi
fi

echo "[✓] Install complete."
