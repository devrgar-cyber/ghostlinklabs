#!/usr/bin/env python3
import argparse, json, hashlib, os, sys, shutil, glob
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
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--manifest", required=True); ap.add_argument("--snapshot-dir"); ap.add_argument("--restore", action="store_true"); args = ap.parse_args()
    manifest = json.loads(open(args.manifest,"r",encoding="utf-8").read())
    mismatches = []
    for entry in manifest.get("hashes", []):
        p, et = entry["path"], entry.get("type","file"); exp = entry["sha256"]
        if et=="dir":
            if not os.path.isdir(p): mismatches.append({"path":p,"reason":"missing dir"})
            else:
                act = hash_dir(p); 
                if act!=exp: mismatches.append({"path":p,"reason":"hash mismatch"})
        else:
            if not os.path.isfile(p): mismatches.append({"path":p,"reason":"missing file"})
            else:
                act = sha256_path(p); 
                if act!=exp: mismatches.append({"path":p,"reason":"hash mismatch"})
    if not mismatches: print("[verify] All good."); sys.exit(0)
    print(f"[verify] Found {len(mismatches)} issues.")
    if args.restore and args.snapshot_dir:
        for m in mismatches:
            path = m["path"]
            src = os.path.join(args.snapshot_dir, os.path.basename(path))
            if os.path.isdir(path):
                os.makedirs(path, exist_ok=True)
                for fp in glob.glob(os.path.join(src, "*")):
                    if os.path.isfile(fp): shutil.copy2(fp, os.path.join(path, os.path.basename(fp)))
                print(f"[restore] dir restored: {path}")
            else:
                if os.path.isfile(src): os.makedirs(os.path.dirname(path), exist_ok=True); shutil.copy2(src, path); print(f"[restore] file restored: {path}")
                else: print(f"[restore] missing in snapshot: {src}")
        sys.exit(2)
    else:
        sys.exit(1)
if __name__=="__main__": main()
