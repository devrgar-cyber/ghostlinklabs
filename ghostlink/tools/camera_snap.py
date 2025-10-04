# ghostlink/tools/camera_snap.py
from __future__ import annotations
from pathlib import Path
from ..runtime.context import Context
from ..runtime.policy import SovereigntyGate

def main(ctx: Context, outfile: str = "snapshot.jpg"):
    p = Path(ctx.vault_path).parent / "outputs" / outfile
    SovereigntyGate.require(ctx, "filesystem", path=str(p))
    try:
        import picamera2  # type: ignore
    except Exception as e:
        return {"error": "picamera2 not available", "detail": str(e)}
    p.parent.mkdir(parents=True, exist_ok=True)
    cam = picamera2.Picamera2(); cam.configure(cam.create_still_configuration()); cam.start(); cam.capture_file(str(p)); cam.stop()
    return {"artifact": str(p), "_artifacts": [str(p)]}
