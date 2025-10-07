#!/usr/bin/env bash
set -euo pipefail

TS="$(date -u +%Y%m%d_%H%M%S)"
OUT_JSON="ghostlink_audit_${TS}.json"
OUT_TXT="ghostlink_audit_${TS}.txt"

# Helper: safe read a file (exists + readable), hash content but do not print raw
hash_file() {
  local f="$1"
  if [[ -r "$f" ]]; then
    sha256sum "$f" | awk '{print $1}'
  else
    echo ""
  fi
}

# Helper: capture cert metadata (no private key)
cert_meta() {
  local crt="$1"
  if [[ -r "$crt" ]]; then
    openssl x509 -in "$crt" -noout -subject -issuer -dates -fingerprint -sha256 2>/dev/null | sed 's/ = /=/g'
  fi
}

collect() {
  echo "{"
  echo "  \"timestamp\":\"$(date -u +%FT%TZ)\","
  echo "  \"host\":\"$(hostname)\","
  echo "  \"uname\":\"$(uname -a | sed 's/\"/\\"/g')\","
  echo "  \"sockets\": $(ss -ltnp 2>/dev/null | egrep ':7420|:7422|:9108' | sed 's/"/\\"/g' | awk 'BEGIN{print "["} {printf "%s{\"line\":\"%s\"}", (NR>1?",":""), $0} END{print "]"}'),"
  echo "  \"firewall\": $( (ufw status verbose || firewall-cmd --list-all || echo 'none') | sed 's/"/\\"/g' | awk 'BEGIN{print "["} {printf "%s{\"line\":\"%s\"}", (NR>1?",":""), $0} END{print "]"}'),"
  echo "  \"wireguard\": $( (wg show || echo 'wg not present') | sed 's/"/\\"/g' | awk 'BEGIN{print "["} {printf "%s{\"line\":\"%s\"}", (NR>1?",":""), $0} END{print "]"}'),"
  # Metrics sample (first 50 lines)
  echo "  \"metrics_head\": $( (curl -fsS http://127.0.0.1:9108/metrics | head -n 50 || echo 'unavailable') | sed 's/"/\\"/g' | awk 'BEGIN{print "["} {printf "%s{\"line\":\"%s\"}", (NR>1?",":""), $0} END{print "]"}'),"
  # systemd status (first 20 lines each) if present
  echo "  \"systemd\": {"
  for s in ghostlink-controller ghostlink-peer ghostlink-bridge; do
    printf "    \"%s\": " "$s"
    (systemctl --no-pager --full status "$s" 2>/dev/null | sed -n '1,20p' || echo "not found") | sed 's/"/\\"/g' | awk 'BEGIN{print "["} {printf "%s{\"line\":\"%s\"}", (NR>1?",":""), $0} END{print "]"}'
    if [[ "$s" != "ghostlink-bridge" ]]; then echo ","; fi
  done
  echo "  },"
  # config fingerprints (no secrets)
  echo "  \"config\": {"
  echo "    \"/etc/default/ghostlink_hash\": \"$(hash_file /etc/default/ghostlink)\","
  echo "    \"GL_ENV_excerpt\": $( (grep -E '^(HOST|PORT|PROMETHEUS_BIND|GL_WINDOW_SEC|GL_.*CAP|GL_GOOD_MAX_C|GL_SCAR_HOT_C|GL_SCAR_SUSTAIN_SEC|GL_MODEL)=' /etc/default/ghostlink 2>/dev/null || true) | sed 's/OPENAI_API_KEY=.*$/OPENAI_API_KEY=<redacted>/' | sed 's/"/\\"/g' | awk 'BEGIN{print "["} {printf "%s{\"line\":\"%s\"}", (NR>1?",":""), $0} END{print "]"}' )"
  echo "  },"
  # cert metadata if exists
  echo "  \"certs\": {"
  for c in /etc/ghostlink/ca.crt /etc/ghostlink/ctl.crt /etc/ghostlink/peer1.crt; do
    b="$(basename "$c")"
    printf "    \"%s\": " "$b"
    cert_meta "$c" | sed 's/"/\\"/g' | awk 'BEGIN{print "["} {printf "%s{\"line\":\"%s\"}", (NR>1?",":""), $0} END{print "]"}'
    if [[ "$b" != "peer1.crt" ]]; then echo ","; fi
  done
  echo "  }"
  echo "}"
}

# Run collection
collect | tee "$OUT_JSON" > /dev/null

# Human-readable TXT summary
{
  echo "GhostLink Audit — $(date -u +%FT%TZ)"
  echo "Host: $(hostname)"
  echo
  echo "[Sockets]"; ss -ltnp 2>/dev/null | egrep ':7420|:7422|:9108' || true
  echo; echo "[Firewall]"; (ufw status verbose || firewall-cmd --list-all || echo 'none') 2>/dev/null
  echo; echo "[WireGuard]"; (wg show || echo 'wg not present') 2>/dev/null | sed -n '1,20p'
  echo; echo "[Metrics head]"; (curl -fsS http://127.0.0.1:9108/metrics | head -n 30 || echo 'unavailable')
  echo; echo "[Systemd]"; for s in ghostlink-controller ghostlink-peer ghostlink-bridge; do echo "== $s =="; systemctl --no-pager --full status "$s" 2>/dev/null | sed -n '1,20p' || echo "not found"; done
  echo; echo "[Config excerpt]"; grep -E '^(HOST|PORT|PROMETHEUS_BIND|GL_WINDOW_SEC|GL_.*CAP|GL_GOOD_MAX_C|GL_SCAR_HOT_C|GL_SCAR_SUSTAIN_SEC|GL_MODEL)=' /etc/default/ghostlink 2>/dev/null || true
  echo; echo "[Certs metadata]"; for c in /etc/ghostlink/ca.crt /etc/ghostlink/ctl.crt /etc/ghostlink/peer1.crt; do echo "-- $c --"; cert_meta "$c"; done
} | tee "$OUT_TXT" >/dev/null

echo "[✓] Wrote $OUT_JSON and $OUT_TXT"
