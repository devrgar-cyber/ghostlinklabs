# Runtime Adaptation Guide

The MAX kernel ships with deterministic guardrails that allow the runtime to spin up layered sandboxes, provide an immersive-yet-muted interface, and guarantee that operational data never leaves operator control. All values below are derived directly from `kernel/gl-kernel.max.json` so the guide remains synchronized with the seed.

## Sandbox Matrix

- **Determinism Controls:** manual_only, background_processes=false, replayable, hash_algo=sha256
- **Capability Floor:** filesystem.read, filesystem.write
- **Governance:** Laws L-01 through L-07 and output rules R-01 through R-08 shape every sandbox cycle.

| Pipeline | Action | Pace | Stage Count | Stages |
|----------|--------|------|-------------|--------|
| MAP | parse | steady | 5 | PLN-1a-skeleton → PLN-1b-lex → PLN-1c-ast → PLN-1d-normalize → PLN-1e-index |
| CLEANSE | scrub | steady | 5 | PLN-2a-trim → PLN-2b-dedup → PLN-2c-noise → PLN-2d-validate → PLN-2e-sanitize |
| SURGE | accelerate | accelerated | 5 | PLN-3a-fastscan → PLN-3b-batch → PLN-3c-parallel → PLN-3d-throttle → PLN-3e-postcheck |
| LOCK | bound | governed | 5 | PLN-4a-caps → PLN-4b-scope → PLN-4c-roles → PLN-4d-ratelimit → PLN-4e-freeze |
| SILENCE | mute | muted | 5 | PLN-5a-output → PLN-5b-logs → PLN-5c-events → PLN-5d-network → PLN-5e-hardware |
| REFLECT | mirror | steady | 5 | PLN-6a-snapshot → PLN-6b-compare → PLN-6c-delta → PLN-6d-verify → PLN-6e-report |
| ECHOFRAME_BIND | bind_state | steady | 5 | PLN-7a-stamp → PLN-7b-chain → PLN-7c-uid → PLN-7d-proof → PLN-7e-store |
| WEAVE | connect | steady | 5 | PLN-8a-route → PLN-8b-bus → PLN-8c-topology → PLN-8d-cache → PLN-8e-verify |
| BIND | fuse | steady | 5 | PLN-9a-join → PLN-9b-conflict → PLN-9c-weights → PLN-9d-resolve → PLN-9e-commit |
| SEAL | finalize | governed | 5 | PLN-10a-freeze → PLN-10b-sign → PLN-10c-index → PLN-10d-reference → PLN-10e-stamp |
| SNAPSHOT | capture | steady | 5 | PLN-11a-state → PLN-11b-meta → PLN-11c-hash → PLN-11d-store → PLN-11e-attest |
| COLLAPSE | halt | steady | 5 | PLN-12a-flush → PLN-12b-zeroize → PLN-12c-release → PLN-12d-halt → PLN-12e-announce |

## Immersive Interface

- **Layers:** CLI_OVERLAY, SYMBOLIC_UI, DIAGNOSTIC_SURFACE
- **Drivers:** ALIGN_GRID (grid=80x24), STACK_TOOL, PATH_TRACE (glyphs=→,↓,↑,↗,↘), PAD_FILL (glyphs=░,·,~), BUILD_UI_LAYOUT, PRESSURE_BAR (glyphs=░,▒,▓,█), MIRROR_SYMMETRY, UI_NERVES
- **Quiet Route:** The SILENCE pipeline (mute) ensures output, log, and event channels can be throttled without breaking determinism.
- **Growth Tracks:** Function register categories provide progressive milestones spanning core, runtime, network, symbology_ui, enforcement, session, ui_tools, tool_primitives, t_funcs, and specialized capabilities.

## Custody Manifest

- **Signature Required:** false
- **Denylist:** bio_protocols, explosives, radioactive_handling
- **Capabilities:** filesystem.read, filesystem.write, filesystem.exec, network.http.get, network.http.post, network.tcp, hardware.gpio, hardware.can, hardware.i2c, hardware.spi
- **Integrity Manifest:** ghostlink/runtime/ghostlink.py, ghostlink/tools/map_tool.py, ghostlink/function_registry.py (hashes populated during attestation)
- **Policy:** restore_on_mismatch=true

These guarantees let operators orchestrate layered simulations, time-dilated replay cycles, and adaptive interfaces without surrendering custody of artifacts or control surfaces.
