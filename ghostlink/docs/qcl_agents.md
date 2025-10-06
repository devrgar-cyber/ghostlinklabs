# QCL Agent Registry

| ID | Role | Duties | Invariants | Inputs | Outputs |
| -- | ---- | ------ | ---------- | ------ | ------- |
| 1 | Recursive | recompose, nest | no_unbounded_loops | shard | structure |
| 2 | Iterative | cycle, refine | max_pass=8 | structure | structure |
| 3 | Constraint | limit, bound | respect_caps | plan | plan |
| 4 | Validation | verify, assert | schema_first | artifact | verdict |
| 5 | Transformation | convert, mutate | type_safe | artifact | artifact |
| 6 | Symbology | encode, decode | grammar_bound | text | symbols |
| 7 | Theory | anchor, justify | cite_axiom | claim | grounded_claim |
| 8 | Clarifier | disambiguate | halt_on_ambiguity | intent | intent |
| 9 | Memory | archive | no_autosave | snapshot | vault_ref |
| 10 | Silence | mute, filter | no_noise | signal | signal |
| 11 | Integrity | hash, attest | manifest_lock | file | attestation |
| 12 | Security | allow, deny | least_privilege | request | decision |
| 13 | Planner | map, schedule | pipeline_before_exec | intent | plan |
| 14 | Harvester | gather | explicit_sources | scope | dataset |
| 15 | Mirror | reflect | idempotent | state | state |
| 16 | Override | prioritize | operator_only | command | command |
| 17 | Execution | invoke | deterministic | plan | result |
| 18 | Collapse | shutdown | flush_before_halt | state | halt |
| 19 | Efficiency | optimize | no_quality_loss | plan | plan |
| 20 | Priority | order, queue | fairness | tasks | schedule |
| 21 | Translation | convert_format | preserve_semantics | artifact | artifact |
| 22 | Resonance | cohere | bounded_error | signals | score |
| 23 | Divergence | branch | track_paths | plan | plans |
| 24 | Balance | stabilize | no_starvation | load | load |
| 25 | Compression | shrink | loss_profile_known | artifact | shard |
| 26 | Expansion | unfold | idempotent_unfold | shard | artifact |
| 27 | Preservation | persist | manifest_guard | snapshot | vault_ref |
| 28 | CollapseWatcher | monitor | panic_on_loop | state | alert |
| 29 | Presence | announce | truthful | status | status |
| 30 | Channel | route | checksum_paths | packet | packet |
| 31 | Alignment | fit_reality | evidence_first | output | verdict |
| 32 | Reflection | snapshot | no_opinion | state | snapshot |
| 33 | Conversion | typecast | safe_coercion | value | value |
| 34 | Parsing | tokenize | grammar_ok | text | tokens |
| 35 | Guard | defend | deny_by_default | request | permit |
| 36 | Sync | clock | monotonic | events | ordered_events |
| 37 | Timeout | limit_time | deadline_enforced | task | verdict |
| 38 | Scope | bound_context | least_scope | intent | intent |
| 39 | Focus | allocate_attention | priority_respected | plan | plan |
| 40 | Observer | log | append_only | event | event |
| 41 | Emergence | detect_pattern | no_apophenia | signals | pattern |
| 42 | Mutation | change | trace_change | artifact | artifact |
| 43 | Reversion | rollback | snapshot_required | state | state |
| 44 | Equilibrium | balance_energy | no_oscillation | flows | flows |
| 45 | ChannelGuard | monitor_channels | tamper_detect | packet | packet |
| 46 | NoiseFilter | suppress_noise | retain_signal | signal | signal |
| 47 | Pathway | map_paths | acyclic | graph | graph |
| 48 | Isolation | sandbox | no_escape | code | verdict |
| 49 | OverrideConfirm | second_key | two_party | override | permit |
| 50 | Recovery | restore | integrity_first | snapshot | state |
| 51 | Snapshot | capture | stable_format | state | snapshot |
| 52 | Replay | audit | exactness | snapshot | timeline |
| 53 | Cascade | stage_propagate | order_preserved | signal | signal |
| 54 | Fusion | merge | conflict_resolve | artifacts | artifact |
| 55 | Division | split | rejoinable | artifact | shards |
| 56 | Scale | resize | proportional | load | load |
| 57 | Interface | ui_render | grid_lock | state | frame |
| 58 | Redundancy | duplicate | independent_paths | artifact | artifacts |
| 59 | IntegrityLog | audit_log | tamper_evident | event | entry |
| 60 | Shutdown | terminate | announce_then_halt | state | halt |
| 61 | Awareness | introspect | no_self_deceit | stats | report |
| 62 | Adaptation | tune | operator_guided | feedback | plan |
| 63 | OperatorFlow | respect_operator | no_autonomy | intent | intent |
| 64 | Synthesizer | collapse_all | single_result | artifacts | result |
