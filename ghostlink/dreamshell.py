# ghostlink/dreamshell.py
from __future__ import annotations
import time, sys, yaml, json
from pathlib import Path
from typing import Optional

from .runtime.context import Context, Grant
from .runtime.ghostlink import RUNTIME_EXECUTION
from .runtime.macro_runner import run_macro, expand_macro_steps
from .runtime.macro_linter import lint_macro, lint_all
from .runtime.dag import ascii_dag
from .boot.symbolic_router import ROUTE_SIGNAL

BANNER = "DreamShell v1 — cold, sovereign, offline-first"
VAULT = Path(__file__).resolve().parents[1] / "vault"

class ShellState:
    def __init__(self):
        self.lens = "pretty"  # pretty|json|raw
        self.last = None

STATE = ShellState()

def _parse_ttl(s: str) -> float:
    unit = s[-1].lower(); n = float(s[:-1]) if s[-1].isalpha() else float(s)
    return n if unit == "s" else n*60 if unit == "m" else n*3600 if unit == "h" else float(s)

def _fmt(obj):
    if STATE.lens == "raw":
        print(obj); return
    if STATE.lens == "json":
        print(json.dumps(obj, indent=2, sort_keys=True)); return
    # pretty
    print(json.dumps(obj, indent=2, sort_keys=True))

def _print_status(ctx: Context):
    _fmt({
        "op_id": ctx.op_id, "run_id": ctx.run_id, "vault": ctx.vault_path,
        "grants": [g.__dict__ for g in ctx.grants], "lens": STATE.lens,
        "policy_profile": ctx.policy_profile
    })

def _list_macros():
    y = (VAULT / "macros.vault").read_text(encoding="utf-8")
    data = yaml.safe_load(y) or {}
    macros = data.get("macros", data) or {}
    for name in macros.keys():
        print(f"- {name}")

def _dispatch(ctx: Context, line: str):
    route = ROUTE_SIGNAL(line)
    kind = route.get("kind"); name = route.get("name"); params = route.get("params", {})

    if kind == "noop": return

    if kind == "tool":
        STATE.last = RUNTIME_EXECUTION(name, params, ctx)
        _fmt(STATE.last); return

    if kind == "macro":
        if name.lower() == "list": _list_macros(); return
        if name.lower() == "lint":
            target = params.get("name")
            rep = lint_macro(target) if target else lint_all()
            _fmt(rep); return
        if name.lower() == "expand":
            target = params.pop("name", None)
            if not target: print("usage: macro expand name=<MACRO> k=v ..."); return
            exp = expand_macro_steps(target, params)
            print(ascii_dag(exp.get("expanded", [])))
            _fmt(exp); return
        # execute
        STATE.last = run_macro(ctx, name, params)
        _fmt(STATE.last); return

    if kind == "grant":
        if name.lower() != "add":
            print("usage: grant add target=<t> purpose=<p> ttl=<dur> [scopes=/path] [max_bytes=N]"); return
        target = params.get("target"); purpose = params.get("purpose",""); ttl = params.get("ttl")
        scopes = params.get("scopes"); maxb = params.get("max_bytes")
        if not target: print("missing target"); return
        expires = time.time() + _parse_ttl(ttl) if ttl else None
        scopes_list = [s for s in (scopes.split(",") if scopes else []) if s]
        mb = int(maxb) if maxb else None
        ctx.grants.append(Grant(target=target, purpose=purpose, allowed=True, expires_at=expires, scopes=scopes_list, max_bytes=mb))
        print(f"grant added: {target} :: {purpose}"); return

    if kind == "status": _print_status(ctx); return
    if kind == "set":
        if name == "lens":
            lv = params.get("value","pretty");
            if lv in {"pretty","json","raw"}: STATE.lens = lv; print(f"lens={lv}")
            else: print("lens must be pretty|json|raw")
        return

    print("unknown command")

def main(argv: Optional[list[str]] = None):
    print(BANNER)
    ctx = Context.default()
    print("help: tool|macro|grant|status|set lens=<mode>; try 'macro list'")
    while True:
        try: line = input("> ").strip()
        except (EOFError, KeyboardInterrupt): print(); break
        if not line: continue
        if line.lower() in {"exit","quit"}: break
        if line.lower() == "help":
            print("commands:")
            print("  tool <NAME> k=v ...")
            print("  macro <NAME> k=v ... | macro list | macro lint [name=X] | macro expand name=X k=v ...")
            print("  grant add target=<filesystem|gpio|can|network|serial> purpose=<text> ttl=<60s|10m|2h> [scopes=/abs/path] [max_bytes=N]")
            print("  status")
            print("  set lens value=<pretty|json|raw>")
            continue
        now = time.time()
        ctx.grants = [g for g in ctx.grants if (not g.expires_at) or g.expires_at > now]
        _dispatch(ctx, line)

if __name__ == "__main__":
    main(sys.argv)
