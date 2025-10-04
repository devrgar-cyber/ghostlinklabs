# ghostlink/tools/vault_encrypt.py
from __future__ import annotations
from ..runtime.context import Context
from ..runtime.policy import SovereigntyGate
from pathlib import Path

# Requires pycryptodome (Crypto.Cipher)

def main(ctx: Context, infile: str, outfile: str, passphrase: str):
    SovereigntyGate.require(ctx, "filesystem", path=infile)
    target = Path(ctx.vault_path).parent / "outputs" / outfile if not Path(outfile).is_absolute() else Path(outfile)
    SovereigntyGate.require(ctx, "filesystem", path=str(target))
    try:
        from Crypto.Cipher import AES  # type: ignore
        from Crypto.Random import get_random_bytes  # type: ignore
        import hashlib
    except Exception as e:
        return {"error": "pycryptodome not installed", "detail": str(e)}
    data = Path(infile).read_bytes()
    key = hashlib.scrypt(passphrase.encode(), salt=b"ghostlink", n=2**14, r=8, p=1, dklen=32)
    nonce = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(data)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(nonce + tag + ct)
    return {"artifact": str(target), "_artifacts": [str(target)]}
