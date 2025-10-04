# ghostlink/runtime/context.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os, time, uuid

@dataclass(frozen=True)
class Grant:
    target: str
    purpose: str
    allowed: bool
    expires_at: Optional[float] = None

@dataclass
class Context:
    op_id: str
    cwd: str
    vault_path: str
    grants: List[Grant]
    env: Dict[str,str]
    nonce: str
    dry_run: bool = False

    @classmethod
    def default(cls):
        return cls(
            op_id=str(uuid.uuid4()),
            cwd=os.getcwd(),
            vault_path=os.path.join(os.getcwd(), "vault"),
            grants=[], env=dict(os.environ), nonce=str(time.time())
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
