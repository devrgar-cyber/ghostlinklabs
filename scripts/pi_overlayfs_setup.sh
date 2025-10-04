#!/usr/bin/env bash
set -euo pipefail
# Sketch: enable overlayfs RO root; writeable /var/ghostlink
sudo apt-get update
sudo apt-get install -y overlayroot
sudo bash -c 'echo "overlayroot=tmpfs" >> /etc/overlayroot.conf'
mkdir -p /var/ghostlink
echo "Bind vault to /var/ghostlink/vault and outputs there (edit DreamShell vault path if needed)."
