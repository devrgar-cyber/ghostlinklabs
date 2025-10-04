# ghostlink/runtime/context.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os, time, uuid, random

@dataclass(frozen=True)
class Grant:
    target: str                        # e.g., "filesystem","gpio","can","network","serial"
    purpose: str
    allowed: bool
    expires_at: Optional[float] = None
    scopes: Optional[List[str]] = None # path prefixes (filesystem) or iface names
    max_bytes: Optional[int] = None    # per-op cap

@dataclass
class Context:
    op_id: str
    run_id: str
    cwd: str
    vault_path: str
    grants: List[Grant]
    env: Dict[str,str]
    nonce: str
    rng_seed: int
    metrics_enabled: bool = True
    policy_profile: str = "dev"       # dev | field | locked
    dry_run: bool = False

    @classmethod
    def default(cls):
        seed = int(time.time() * 1000) ^ os.getpid() ^ random.getrandbits(32)
        return cls(
            op_id=str(uuid.uuid4()),
            run_id=str(uuid.uuid4()),
            cwd=os.getcwd(),
            vault_path=os.path.join(os.getcwd(), "vault"),
            grants=[], env=dict(os.environ), nonce=str(time.time()), rng_seed=seed
        )

@dataclass(frozen=True)
class Receipt:
    ts: float
    command: str
    tool: str
    params: Dict[str, Any]
    status: str
    sha256_input: str
    sha256_output: str
    artifacts: List[str]
    run_id: Optional[str] = None
    duration_ms: Optional[int] = None
