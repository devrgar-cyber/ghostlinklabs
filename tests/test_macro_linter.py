from pathlib import Path

from ghostlink.runtime import macro_linter


def test_scanforge_macro_does_not_warn_for_prev_placeholder(monkeypatch):
    repo_root = Path(__file__).resolve().parents[1]
    vault_dir = repo_root / "vault"

    monkeypatch.setattr(macro_linter, "VAULT", vault_dir)
    monkeypatch.setattr(macro_linter, "MANIFEST", vault_dir / "manifest.json")

    result = macro_linter.lint_macro("SCANFORGE")
    warnings = result.get("warnings", [])
    assert not any("unknown placeholders" in warn for warn in warnings), warnings
