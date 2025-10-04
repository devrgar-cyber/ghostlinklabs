# ghostlink/runtime/ghostlink.py
import time, json, hashlib, importlib
from pathlib import Path
from .context import Context, Receipt
from .policy import Wraithgate
from .receipts import write_receipt
from .verify_and_restore import verify_manifest

BASE = Path(__file__).resolve().parents[1]
VAULT = BASE / "vault"
MANIFEST = VAULT / "manifest.json"

def _sha256(b: bytes) -> str: return hashlib.sha256(b).hexdigest()

def _run_tool(ctx: Context, tool: str, params: dict):
    Wraithgate.enforce(ctx, tool, params)
    mod = importlib.import_module(f"ghostlink.tools.{tool.lower()}")
    return mod.main(ctx, **params)

def RUNTIME_EXECUTION(tool: str, params: dict, ctx: Context):
    verify_manifest(MANIFEST)
    t0 = time.time()
    try:
        out = _run_tool(ctx, tool, params)
        status = "ok"
    except Exception as e:
        out = {"error": type(e).__name__, "detail": str(e)}
        status = "fail"
    t1 = time.time()
    rec = Receipt(
        ts=t1, command=tool, tool=tool, params=params, status=status,
        sha256_input=_sha256(json.dumps(params, sort_keys=True).encode()),
        sha256_output=_sha256(json.dumps(out, sort_keys=True).encode()),
        artifacts=[]
    )
    write_receipt(VAULT / "receipts.log", rec)
    return out
