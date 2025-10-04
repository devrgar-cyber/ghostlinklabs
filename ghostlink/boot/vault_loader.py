# ghostlink/boot/vault_loader.py
from pathlib import Path
import yaml

def LOAD_VAULT(vault_dir: str) -> dict:
    vd = Path(vault_dir)
    def load_if(p): return yaml.safe_load(p.read_text()) if p.exists() else {}
    return {
        "core": load_if(vd / "core.vault"),
        "macros": load_if(vd / "macros.vault"),
        "memory": load_if(vd / "memory_layer_01.vault"),
    }
