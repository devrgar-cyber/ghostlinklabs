# Pipeline Topology

| ID | Name | Action | Multipaths |
| --- | --- | --- | --- |
| P-01 | MAP | parse | PLN-1a-skeleton<br>PLN-1b-lex<br>PLN-1c-ast<br>PLN-1d-normalize<br>PLN-1e-index |
| P-02 | CLEANSE | scrub | PLN-2a-trim<br>PLN-2b-dedup<br>PLN-2c-noise<br>PLN-2d-validate<br>PLN-2e-sanitize |
| P-03 | SURGE | accelerate | PLN-3a-fastscan<br>PLN-3b-batch<br>PLN-3c-parallel<br>PLN-3d-throttle<br>PLN-3e-postcheck |
| P-04 | LOCK | bound | PLN-4a-caps<br>PLN-4b-scope<br>PLN-4c-roles<br>PLN-4d-ratelimit<br>PLN-4e-freeze |
| P-05 | SILENCE | mute | PLN-5a-output<br>PLN-5b-logs<br>PLN-5c-events<br>PLN-5d-network<br>PLN-5e-hardware |
| P-06 | REFLECT | mirror | PLN-6a-snapshot<br>PLN-6b-compare<br>PLN-6c-delta<br>PLN-6d-verify<br>PLN-6e-report |
| P-07 | ECHOFRAME_BIND | bind_state | PLN-7a-stamp<br>PLN-7b-chain<br>PLN-7c-uid<br>PLN-7d-proof<br>PLN-7e-store |
| P-08 | WEAVE | connect | PLN-8a-route<br>PLN-8b-bus<br>PLN-8c-topology<br>PLN-8d-cache<br>PLN-8e-verify |
| P-09 | BIND | fuse | PLN-9a-join<br>PLN-9b-conflict<br>PLN-9c-weights<br>PLN-9d-resolve<br>PLN-9e-commit |
| P-10 | SEAL | finalize | PLN-10a-freeze<br>PLN-10b-sign<br>PLN-10c-index<br>PLN-10d-reference<br>PLN-10e-stamp |
| P-11 | SNAPSHOT | capture | PLN-11a-state<br>PLN-11b-meta<br>PLN-11c-hash<br>PLN-11d-store<br>PLN-11e-attest |
| P-12 | COLLAPSE | halt | PLN-12a-flush<br>PLN-12b-zeroize<br>PLN-12c-release<br>PLN-12d-halt<br>PLN-12e-announce |
