#!/usr/bin/env python3
import argparse, json, hashlib, os, sys, glob
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
    ap = argparse.ArgumentParser(); ap.add_argument("--manifest", required=True); ap.add_argument("--report", required=True); args = ap.parse_args()
    manifest = json.loads(open(args.manifest,"r",encoding="utf-8").read())
    checks, mismatches = [], 0
    for entry in manifest.get("hashes", []):
        p, et = entry["path"], entry.get("type","file")
        exp = entry["sha256"]
        exists = os.path.isdir(p) if et=="dir" else os.path.isfile(p)
        if not exists: checks.append({"path":p,"status":"missing"}); mismatches += 1; continue
        act = hash_dir(p) if et=="dir" else sha256_path(p)
        ok = (act==exp); checks.append({"path":p,"status":"ok" if ok else "mismatch","expected":exp,"actual":act}); mismatches += 0 if ok else 1
    rep = {"manifest": os.path.abspath(args.manifest), "results": checks, "mismatches": mismatches}
    open(args.report,"w",encoding="utf-8").write(json.dumps(rep, indent=2))
    print(f"[integrity] mismatches={mismatches} → report: {args.report}"); sys.exit(0 if mismatches==0 else 1)
if __name__=="__main__": main()
