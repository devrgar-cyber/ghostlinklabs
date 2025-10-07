#!/usr/bin/env bash
set -euo pipefail
# WireGuard bootstrap (controller + peer). Prints public keys and sample wg0.conf.

role="${1:-}"
if [[ "$role" != "controller" && "$role" != "peer" ]]; then
  echo "usage: $0 controller|peer" >&2
  exit 2
fi

mkdir -p /etc/wireguard
umask 077

if [[ ! -f /etc/wireguard/privatekey ]]; then
  wg genkey | tee /etc/wireguard/privatekey | wg pubkey > /etc/wireguard/publickey
fi

echo "[i] Private key: /etc/wireguard/privatekey"
echo "[i] Public  key: /etc/wireguard/publickey"
PUB=$(cat /etc/wireguard/publickey)

if [[ "$role" == "controller" ]]; then
cat <<EOF
[Interface]
Address = 10.7.0.1/24
ListenPort = 51820
PrivateKey = <CONTROLLER_PRIVATE>

# Add peers as needed:
# [Peer]
# PublicKey = <PEER_PUBLIC>
# AllowedIPs = 10.7.0.2/32
EOF
else
cat <<EOF
[Interface]
Address = 10.7.0.2/24
PrivateKey = <PEER_PRIVATE>

[Peer]
PublicKey = <CONTROLLER_PUBLIC>
AllowedIPs = 10.7.0.1/32
Endpoint = <controller_public_ip>:51820
PersistentKeepalive = 25
EOF
fi
