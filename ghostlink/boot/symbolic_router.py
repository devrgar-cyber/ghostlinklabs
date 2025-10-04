# ghostlink/boot/symbolic_router.py
import shlex

def ROUTE_SIGNAL(line: str):
    parts = shlex.split(line.strip())
    if not parts: return {"kind":"noop"}
    head = parts[0].lower()
    if head in {"tool","macro","grant","set","status"}:
        name = parts[1] if len(parts) > 1 else ""
        rest = parts[2:]
        params = {}
        for kv in rest:
            if "=" in kv:
                k,v = kv.split("=",1); params[k]=v
            elif head=="set" and kv.startswith("lens="):
                k,v = kv.split("=",1); params['value']=v
        return {"kind": head, "name": name, "params": params}
    return {"kind":"noop"}
