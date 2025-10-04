# ghostlink/dreamshell.py
from __future__ import annotations
import time, sys, yaml
from pathlib import Path
from typing import Optional

from .runtime.context import Context, Grant
from .runtime.ghostlink import RUNTIME_EXECUTION
from .runtime.macro_runner import run_macro, expand_macro_steps
from .runtime.macro_linter import lint_macro, lint_all
from .boot.symbolic_router import ROUTE_SIGNAL

BANNER = "DreamShell v1 — cold, sovereign, offline-first"
VAULT = Path(__file__).resolve().parents[1] / "vault"

def _parse_ttl(s: str) -> float:
    unit = s[-1].lower(); n = float(s[:-1]) if s[-1].isalpha() else float(s)
    return n if unit == "s" else n*60 if unit == "m" else n*3600 if unit == "h" else float(s)

def _print_status(ctx: Context):
    print("status:")
    print(f"  op_id: {ctx.op_id}")
    print(f"  vault:{ctx.vault_path}")
    for g in ctx.grants:
        ttl = None if not g.expires_at else max(0, int(g.expires_at - time.time()))
        print(f"  grant: {g.target} :: {g.purpose} :: allowed={g.allowed} :: ttl={ttl}")

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
        print(RUNTIME_EXECUTION(name, params, ctx)); return

    if kind == "macro":
        # macro sub-commands
        if name.lower() == "list":
            _list_macros(); return
        if name.lower() == "lint":
            target = params.get("name")
            rep = lint_macro(target) if target else lint_all()
            print(rep); return
        if name.lower() == "expand":
            target = params.pop("name", None)
            if not target: print("usage: macro expand name=<MACRO> k=v ..."); return
            print(expand_macro_steps(target, params)); return
        # execute a macro
        print(run_macro(ctx, name, params)); return

    if kind == "grant":
        if name.lower() != "add":
            print("usage: grant add target=<t> purpose=<p> ttl=<dur>"); return
        target = params.get("target"); purpose = params.get("purpose",""); ttl = params.get("ttl")
        if not target: print("missing target"); return
        expires = time.time() + _parse_ttl(ttl) if ttl else None
        ctx.grants.append(Grant(target=target, purpose=purpose, allowed=True, expires_at=expires))
        print(f"grant added: {target} :: {purpose}"); return

    if kind == "status":
        _print_status(ctx); return

    print("unknown command")

def main(argv: Optional[list[str]] = None):
    print(BANNER)
    ctx = Context.default()
    print("help: tool|macro|grant|status; try 'macro list'")
    while True:
        try: line = input("> ").strip()
        except (EOFError, KeyboardInterrupt): print(); break
        if not line: continue
        if line.lower() in {"exit","quit"}: break
        if line.lower() == "help":
            print("commands:")
            print("  tool <NAME> k=v ...")
            print("  macro <NAME> k=v ...           # run macro")
            print("  macro list")
            print("  macro lint [name=<MACRO>]")
            print("  macro expand name=<MACRO> k=v ...")
            print("  grant add target=<filesystem|gpio|can|network> purpose=<text> ttl=<60s|10m|2h>")
            print("  status")
            continue
        now = time.time()
        ctx.grants = [g for g in ctx.grants if (not g.expires_at) or g.expires_at > now]
        _dispatch(ctx, line)

if __name__ == "__main__":  # pragma: no cover
    main(sys.argv)
