# GhostLink Quickstart

## 1) Install deps
```

pip install -r requirements.txt

```

## 2) Seed the vault
```

python scripts/init_vault.py

```

## 3) Generate manifest hashes
```

python scripts/hash_manifest.py --write

```

## 4) Launch DreamShell
```

python -m ghostlink.dreamshell

```

### Try a run
```

grant add target=filesystem purpose=ro ttl=10m
tool status
tool scan source=vault/core.vault
macro DEEPWALK file=vault/core.vault
macro SCANFORGE file=vault/core.vault

```
Artifacts land in `outputs/`, receipts in `vault/receipts.log`.
