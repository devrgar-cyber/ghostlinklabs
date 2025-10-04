# ghostlink/tools/vault_decrypt.py
from __future__ import annotations
from ..runtime.context import Context
from ..runtime.policy import SovereigntyGate
from pathlib import Path

def main(ctx: Context, infile: str, passphrase: str):
    SovereigntyGate.require(ctx, "filesystem", path=infile)
    try:
        from Crypto.Cipher import AES  # type: ignore
        import hashlib
    except Exception as e:
        return {"error": "pycryptodome not installed", "detail": str(e)}
    data = Path(infile).read_bytes()
    nonce, tag, ct = data[:16], data[16:32], data[32:]
    key = hashlib.scrypt(passphrase.encode(), salt=b"ghostlink", n=2**14, r=8, p=1, dklen=32)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    pt = cipher.decrypt_and_verify(ct, tag)
    return {"text": pt.decode(errors='replace')}
