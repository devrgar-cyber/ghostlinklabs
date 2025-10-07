#!/usr/bin/env bash
set -euo pipefail
# mTLS bootstrap: creates CA, server(cert for controller), and a peer client cert.

GL_DIR=${1:-/etc/ghostlink}
mkdir -p "$GL_DIR"
umask 077
cd "$GL_DIR"

# CA
if [[ ! -f ca.key ]]; then
  openssl genrsa -out ca.key 4096
  openssl req -x509 -new -key ca.key -sha256 -days 3650 -out ca.crt -subj "/CN=GhostLink-CA"
fi

# Server (controller)
openssl genrsa -out ctl.key 4096
openssl req -new -key ctl.key -out ctl.csr -subj "/CN=controller.wg"
openssl x509 -req -in ctl.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out ctl.crt -days 825 -sha256

# Peer1 (client)
openssl genrsa -out peer1.key 4096
openssl req -new -key peer1.key -out peer1.csr -subj "/CN=peer1.wg"
openssl x509 -req -in peer1.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out peer1.crt -days 825 -sha256

chown -R root:ghostlink "$GL_DIR"
chmod 640 "$GL_DIR"/*.key

echo "[✓] Certificates created under $GL_DIR"
echo "[i] Controller/server: ctl.crt ctl.key"
echo "[i] Peer/client: peer1.crt peer1.key"
echo "[i] CA: ca.crt (distribute to all nodes)"
