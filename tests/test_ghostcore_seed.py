from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ghostlink.runtime import ghostlink
from ghostlink.tools import describe_tool, list_tools, tool_manifest


def test_kernel_summary_counts() -> None:
    kernel = ghostlink.load_kernel()
    summary = ghostlink.summarize_kernel(kernel)
    assert summary["kernel_id"] == "GHOSTCORE_FINAL_MAX"
    assert summary["agent_count"] == 64
    assert summary["pipeline_count"] == 12
    assert summary["tool_count"] == len(kernel["tools"])
    assert summary["law_count"] == len(kernel["laws"])


def test_pipeline_routes_consistent_with_seed() -> None:
    kernel = ghostlink.load_kernel()
    routes = ghostlink.gather_pipeline_routes(kernel)
    seed_text = Path("kernel/ghostcore.seed").read_text(encoding="utf-8")

    for pipeline in kernel["pipelines"]:
        assert routes[pipeline["name"]] == pipeline["multipaths"]
        encoded = "|".join(
            [pipeline["name"], pipeline["action"], ";".join(pipeline["multipaths"])]
        )
        assert f"{pipeline['id']}={encoded}" in seed_text


def test_tools_module_matches_kernel_manifest() -> None:
    kernel = ghostlink.load_kernel()
    manifest = tool_manifest()

    assert list_tools() == kernel["tools"]
    for tool_name in kernel["tools"]:
        entry = manifest[tool_name]
        pipeline = next((p for p in kernel["pipelines"] if p["name"] == tool_name), None)
        if pipeline is None:
            assert entry["action"] is None
            assert entry["multipaths"] == []
        else:
            assert entry["action"] == pipeline["action"]
            assert entry["multipaths"] == pipeline["multipaths"]
        assert describe_tool(tool_name) == entry


def test_generated_docs_contain_no_placeholder_language() -> None:
    targets = [
        Path("ghostlink/chains/README.md"),
        Path("ghostlink/chains/pipelines.md"),
        Path("ghostlink/opcode/README.md"),
        Path("ghostlink/opcode/spec.md"),
        Path("ghostlink/docs/README.md"),
        Path("ghostlink/docs/kernel_overview.md"),
        Path("ghostlink/docs/qcl_agents.md"),
        Path("ghostlink/docs/expansion_shards.md"),
        Path("ghostlink/docs/mirrors.md"),
        Path("ghostlink/docs/ui.md"),
        Path("ghostlink/docs/function_register.md"),
        Path("ghostlink/docs/events.md"),
        Path("ghostlink/docs/integrity_manifest.md"),
        Path("ghostlink/docs/rebuild.md"),
        Path("ghostlink/tools/README.md"),
    ]

    for target in targets:
        text = target.read_text(encoding="utf-8").lower()
        assert "placeholder" not in text


def test_protocol_sections_cover_kernel_payload() -> None:
    kernel = ghostlink.load_kernel()
    sections = ghostlink.list_sections()
    expected_sections = {
        "summary",
        "determinism",
        "sovereignty",
        "laws",
        "output_rules",
        "capabilities",
        "agents",
        "pipelines",
        "tools",
        "opcode",
        "expansion_shards",
        "mirrors",
        "ui_layers",
        "ui_drivers",
        "function_register",
        "events",
        "integrity",
        "rebuild",
        "protocol",
    }

    assert expected_sections == set(sections)

    protocol = ghostlink.ghostlink_protocol(kernel)
    for key in expected_sections - {"protocol"}:
        assert key in protocol

    assert protocol["summary"]["kernel_id"] == kernel["kernel_id"]
    assert protocol["rebuild"] == kernel["rebuild"]["steps"]


def test_docs_reflect_kernel_content() -> None:
    kernel = ghostlink.load_kernel()

    agents_doc = Path("ghostlink/docs/qcl_agents.md").read_text(encoding="utf-8")
    for agent in kernel["qcl_agents"]:
        assert f"| {agent['id']} | {agent['role']} |" in agents_doc

    shard_doc = Path("ghostlink/docs/expansion_shards.md").read_text(encoding="utf-8")
    for shard in kernel["expansion_shards"]:
        assert f"| {shard['id']} | {shard['name']} |" in shard_doc

    mirror_doc = Path("ghostlink/docs/mirrors.md").read_text(encoding="utf-8")
    for mirror in kernel["mirrors"]:
        assert f"| {mirror['id']} | {mirror['name']} |" in mirror_doc

    ui_doc = Path("ghostlink/docs/ui.md").read_text(encoding="utf-8")
    for driver in kernel["ui"]["drivers"]:
        assert driver["name"] in ui_doc

    function_doc = Path("ghostlink/docs/function_register.md").read_text(encoding="utf-8")
    for category, entries in kernel["function_register"].items():
        assert f"## {category.replace('_', ' ').title()}" in function_doc
        for entry in entries:
            assert f"- {entry}" in function_doc

    events_doc = Path("ghostlink/docs/events.md").read_text(encoding="utf-8")
    for kind in kernel["events"]["kinds"]:
        assert f"- {kind}" in events_doc

    integrity_doc = Path("ghostlink/docs/integrity_manifest.md").read_text(encoding="utf-8")
    for entry in kernel["integrity"]["manifest"]["files"]:
        assert entry["path"] in integrity_doc

    rebuild_doc = Path("ghostlink/docs/rebuild.md").read_text(encoding="utf-8")
    for step in kernel["rebuild"]["steps"]:
        assert step in rebuild_doc

    overview_doc = Path("ghostlink/docs/kernel_overview.md").read_text(encoding="utf-8")
    for capability in kernel["sovereignty"]["capabilities"]:
        assert capability["cap"] in overview_doc
    denylist = kernel["sovereignty"].get("denylist", [])
    if denylist:
        for entry in denylist:
            assert entry in overview_doc
