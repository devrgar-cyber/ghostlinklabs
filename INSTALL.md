# GhostLink — Full Suite

This bundle gives you three deployment paths and the tools to harden, audit, and operate:

- **Systemd** (recommended on a rack/server)
- **Virtual environment** (no root, dev-friendly)
- **Docker** (containerized, host network by default)

Also included: firewall hardening, periodic sanity-check, OS update+restart, audit collector, and a bridge to ChatGPT.

## Quick install (systemd, minimal + safe)

```bash
tar xzf ghostlink_full_suite.tgz
cd ghostlink_full_suite
sudo bash install.sh --systemd --harden
```

Then verify:
```bash
bash gl_sanity_check.sh
curl -s 127.0.0.1:9108/metrics | head
```

## Other modes

- **Virtualenv (no system changes):**
  ```bash
  tar xzf ghostlink_venv_runner.tgz -C ~/
  cd ~/ghostlink_venv_runner
  bash run_venv.sh up
  bash run_venv.sh status
  ```

- **Docker:**
  ```bash
  tar xzf ghostlink_container_ctx.tgz
  cd ghostlink_container_ctx
  docker build -t ghostlink:0.1 .
  docker compose up -d
  docker logs -f ghostlink
  ```

## Optional security layers

- **WireGuard overlay:**
  ```bash
  sudo bash ghostlink_automation_cfg/bootstrap/gl_wireguard_bootstrap.sh controller
  ```

- **mTLS for app sockets:**
  ```bash
  sudo bash ghostlink_automation_cfg/bootstrap/gl_tls_bootstrap.sh /etc/ghostlink
  sudo systemctl restart ghostlink-controller
  ```

## Operate

- **Update + restart:** `sudo bash gl_update_and_restart.sh`
- **Sanity check:** `bash gl_sanity_check.sh`
- **Audit snapshot:** `bash ghostlink_audit_chat/gl_audit_collect.sh`
- **Talk to ChatGPT via local bridge:**
  ```bash
  cd ghostlink_audit_chat
  export OPENAI_API_KEY=sk-...; python3 gl_openai_bridge_v2.py  # window 1
  python3 gl_talk_cli.py chat                                   # window 2
  ```
