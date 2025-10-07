#!/usr/bin/env python3
"""
ghostknife.py — Compact GhostLink CLI (non-autonomous)
Commands:
  scan                 → create/refresh ghostlink_fill_queue_full.csv (up to 1200)
  autoforge A B        → forge stubs for [A..B] into /mnt/data/auto_stubs_A_B/
  manifest             → expand pristine_bundle.manifest to current artifacts
  checkpoint           → write a checkpoint JSON with guard hash
"""
import argparse, os, re, json, hashlib, glob, pandas as pd
from datetime import datetime
ROOT = "/mnt/data"
def sha256_path(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
def hash_dir(path):
    entries = []
    for p in sorted(glob.glob(os.path.join(path, "*"))):
        if os.path.isfile(p):
            entries.append(os.path.basename(p) + ":" + sha256_path(p))
    return hashlib.sha256(("\n".join(entries)).encode()).hexdigest()
def full_dump_text():
    parts = sorted(glob.glob(os.path.join(ROOT, "SCRIPTS_2_FULL_DUMP.part*.txt")))
    return "".join(open(p,"r",encoding="utf-8",errors="ignore").read()+"\n" for p in parts)
def cmd_scan():
    text = full_dump_text()
    pats = [r"\bTODO\b", r"\bFIXME\b", r"\bTBD\b", r"\bmissing\b", r"\bnot found\b",
            r"\bundefined\b", r"\bnull\b", r"\bplaceholder\b", r"\bincomplete\b",
            r"\bto be filled\b", r"\bpending\b", r"\b\?\?\?\b", r"\bXXX\b"]
    rgx = re.compile("|".join(pats), re.IGNORECASE)
    seen, lines = set(), []
    for line in text.splitlines():
        if rgx.search(line):
            s = " ".join(line.strip().split())
            if s and s not in seen: lines.append(s); seen.add(s)
    N = min(1200, len(lines))
    out = os.path.join(ROOT, "ghostlink_fill_queue_full.csv")
    pd.DataFrame({"priority": range(1, N+1), "missing_marker_line": lines[:N]}).to_csv(out, index=False)
    print(f"[scan] wrote {out} with {N} rows")
def forge_range(a,b):
    csvp = os.path.join(ROOT, "ghostlink_fill_queue_full.csv")
    if not os.path.exists(csvp): raise SystemExit("[autoforge] run 'scan' first.")
    df = pd.read_csv(csvp); lines = df["missing_marker_line"].astype(str).tolist()
    a = max(1,int(a)); b = min(int(b), len(lines))
    outdir = os.path.join(ROOT, f"auto_stubs_{a}_{b}"); os.makedirs(outdir, exist_ok=True)
    from datetime import datetime as _dt
    for idx in range(a,b+1):
        line = lines[idx-1]
        path = os.path.join(outdir, f"stub_{idx:04d}.md")
        with open(path,"w",encoding="utf-8") as f:
            f.write(f"---\n"); f.write(f"id: auto_stub_{idx:04d}\n")
            f.write(f"origin: fill_queue_full[{idx}]\n"); f.write("status: AUTO-FORGED\n")
            f.write(f"created: {_dt.now().isoformat()}\n---\n\n")
            f.write(f"## Context\n{line}\n\n## Intent\nDescribe inputs/outputs.\n\n")
            f.write("## Draft\n- [ ] Define IO\n- [ ] Minimal skeleton\n- [ ] Tests\n")
    print(f"[autoforge] forged stubs in {outdir}")
def expand_manifest():
    manifest_path = os.path.join(ROOT, "pristine_bundle.manifest")
    try: manifest = json.loads(open(manifest_path,"r",encoding="utf-8").read())
    except Exception: manifest = {"name":"ghostlinklabs_pristine_bundle","hashes":[],"whitelist":{"scripts":[]}} 
    artifacts = [
        os.path.join(ROOT,"macros.vault"), os.path.join(ROOT,"persona.vault"),
        os.path.join(ROOT,"vault_manager.py"), os.path.join(ROOT,"ghostknife.py"),
        os.path.join(ROOT,"integrity_monitor.py"), os.path.join(ROOT,"verify_and_restore.py"),
        os.path.join(ROOT,"ghostlink_fill_queue.csv"), os.path.join(ROOT,"ghostlink_fill_queue_full.csv"),
    ] + glob.glob(os.path.join(ROOT,"auto_stubs_*")) + glob.glob(os.path.join(ROOT,"auto_stubs_*.zip"))
    new_hashes = []
    for a in artifacts:
        if not os.path.exists(a): continue
        if os.path.isdir(a): new_hashes.append({"path":a,"sha256":hash_dir(a),"type":"dir"})
        else: new_hashes.append({"path":a,"sha256":sha256_path(a),"type":"file"})
    manifest["hashes"] = [h for h in manifest.get("hashes",[]) if h["path"] not in {x["path"] for x in new_hashes}] + new_hashes
    wl = set(manifest.get("whitelist",{}).get("scripts",[])); wl.update(["vault_manager.py","ghostknife.py","integrity_monitor.py","verify_and_restore.py"])
    manifest["whitelist"]["scripts"] = sorted(wl)
    with open(manifest_path,"w",encoding="utf-8") as f: f.write(json.dumps(manifest, indent=2))
    print(f"[manifest] updated {manifest_path} with {len(manifest['hashes'])} entries")
def checkpoint():
    ckpt_dir = os.path.join(ROOT, "checkpoints"); os.makedirs(ckpt_dir, exist_ok=True)
    snap = {"ts": datetime.now().isoformat()}
    snap["guard_hash"] = hashlib.sha256(json.dumps(snap, sort_keys=True).encode()).hexdigest()
    path = os.path.join(ckpt_dir, f"ckpt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(path,"w",encoding="utf-8") as f: f.write(json.dumps(snap, indent=2))
    print(f"[checkpoint] wrote {path}")
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("command", choices=["scan","autoforge","manifest","checkpoint"]); ap.add_argument("args", nargs="*"); ns=ap.parse_args()
    if ns.command=="scan": cmd_scan()
    elif ns.command=="autoforge":
        if len(ns.args)!=2: raise SystemExit("usage: ghostknife.py autoforge <start> <end>"); forge_range(ns.args[0], ns.args[1])
        forge_range(ns.args[0], ns.args[1])
    elif ns.command=="manifest": expand_manifest()
    elif ns.command=="checkpoint": checkpoint()
if __name__=="__main__": main()
