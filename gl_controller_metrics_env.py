#!/usr/bin/env python3
# GhostLink Controller — read-only, Prometheus /metrics, ENV-configurable
import os, socket, json, time, math
from collections import defaultdict
from prometheus_client import start_http_server, Gauge, Counter

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "7420"))
WIN  = int(os.getenv("GL_WINDOW_SEC", "20"))
GOOD_MAX = float(os.getenv("GL_GOOD_MAX_C", "80.0"))
SCAR_HOT = float(os.getenv("GL_SCAR_HOT_C", "85.0"))
SCAR_SUSTAIN = int(os.getenv("GL_SCAR_SUSTAIN_SEC", "5"))

SIGMA_FRAC      = Gauge('ghostlink_sigma_fraction',      'Good fraction in last window',          ['roi'])
SCAR_FLAG       = Gauge('ghostlink_scar_flag',           'Scar in last window (0/1)',             ['roi'])
WINDOW_SAMPLES  = Gauge('ghostlink_window_samples',      'Samples counted in last window',        ['roi'])
GOOD_SAMPLES    = Counter('ghostlink_good_samples_total','Cumulative good samples',               ['roi'])
TOTAL_SAMPLES   = Counter('ghostlink_samples_total',     'Cumulative samples',                    ['roi'])
SCAR_WINDOWS    = Counter('ghostlink_scar_windows_total','Cumulative windows containing a scar',  ['roi'])

def _recv_lines(conn):
    buf = b""
    while True:
        chunk = conn.recv(4096)
        if not chunk: break
        buf += chunk
        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1)
            line = line.strip()
            if line: yield line

def main():
    # metrics bind (fixed to loopback by design; change via PROM_BIND if needed)
    prom_bind = os.getenv("PROMETHEUS_BIND", "127.0.0.1:9108")
    host_m, port_m = prom_bind.split(":")
    start_http_server(int(port_m), addr=host_m)
    print(f"[controller] /metrics at http://{prom_bind}/metrics")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT)); s.listen(1)
        print(f"[controller] listening on {HOST}:{PORT} (WIN={WIN}s GOOD_MAX={GOOD_MAX}C SCAR_HOT={SCAR_HOT}C SCAR_SUSTAIN={SCAR_SUSTAIN}s)")
        conn, addr = s.accept()
        with conn:
            print(f"[controller] peer {addr} connected")
            hot_streak = defaultdict(int)
            last_win   = defaultdict(lambda: None)
            win_stats  = defaultdict(lambda: {"n":0,"good":0,"scar":False})

            def flush(zone, w):
                st = win_stats[(zone,w)]
                if st["n"]==0: return
                roi = f"rack.{zone}"
                good_frac = st["good"]/st["n"]
                scar_bit  = 1 if st["scar"] else 0
                print(f"[shadow] roi={roi} win={w} Σ={good_frac:.3f} SCAR={scar_bit} n={st['n']}")
                SIGMA_FRAC.labels(roi).set(good_frac)
                SCAR_FLAG.labels(roi).set(scar_bit)
                WINDOW_SAMPLES.labels(roi).set(st["n"])
                GOOD_SAMPLES.labels(roi).inc(st["good"])
                TOTAL_SAMPLES.labels(roi).inc(st["n"])
                if st["scar"]: SCAR_WINDOWS.labels(roi).inc()
                del win_stats[(zone,w)]

            for raw in _recv_lines(conn):
                try:
                    msg = json.loads(raw.decode("utf-8"))
                except Exception:
                    continue
                if msg.get("type") != "sample": continue

                data  = msg.get("data",{})
                zone  = data.get("zone","core")
                ts    = float(msg.get("ts", time.time()))
                temp  = data.get("cpu_temp_c", None)
                fault = data.get("fault", None)
                if temp is None: continue

                hot = temp > SCAR_HOT
                hot_streak[zone] = hot_streak[zone] + 1 if hot else 0
                scar = bool(fault) or (hot_streak[zone] >= SCAR_SUSTAIN)
                good = (not fault) and (temp <= GOOD_MAX)

                w  = int(math.floor(ts/WIN))
                lw = last_win[zone]
                if lw is not None and w != lw:
                    flush(zone, lw)
                last_win[zone] = w

                st = win_stats[(zone,w)]
                st["n"] += 1
                st["good"] += 1 if good else 0
                st["scar"] = st["scar"] or scar

            for (zone,w) in list(win_stats.keys()):
                flush(zone,w)

if __name__ == "__main__":
    main()
