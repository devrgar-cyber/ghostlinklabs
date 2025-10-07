from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

KERNEL_PATH = Path(__file__).resolve().parents[2] / "kernel" / "gl-kernel.max.json"


NEWLINE = chr(10)


def load_kernel(path: Path = KERNEL_PATH) -> dict[str, Any]:
    """Load the MAX kernel description from disk."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def summarize_kernel(kernel: dict[str, Any]) -> dict[str, Any]:
    """Return headline metrics for the kernel."""
    return {
        "kernel_id": kernel["kernel_id"],
        "version": kernel["version"],
        "agent_count": len(kernel["qcl_agents"]),
        "pipeline_count": len(kernel["pipelines"]),
        "tool_count": len(kernel["tools"]),
        "law_count": len(kernel["laws"]),
    }


def gather_pipeline_routes(kernel: dict[str, Any]) -> dict[str, list[str]]:
    """Map each pipeline name to its multipath list."""
    return {pipe["name"]: list(pipe["multipaths"]) for pipe in kernel["pipelines"]}


def gather_capabilities(kernel: dict[str, Any]) -> list[str]:
    """Extract capability identifiers from the sovereignty section."""
    return [cap["cap"] for cap in kernel["sovereignty"]["capabilities"]]


def gather_determinism(kernel: dict[str, Any]) -> dict[str, Any]:
    """Return determinism controls."""
    return dict(kernel["determinism"])


def gather_sovereignty(kernel: dict[str, Any]) -> dict[str, Any]:
    """Return sovereignty configuration."""
    sovereignty = kernel["sovereignty"].copy()
    sovereignty["denylist"] = list(sovereignty.get("denylist", []))
    sovereignty["capabilities"] = list(sovereignty.get("capabilities", []))
    return sovereignty


def gather_expansion_shards(kernel: dict[str, Any]) -> list[dict[str, Any]]:
    return [dict(shard) for shard in kernel["expansion_shards"]]


def gather_mirrors(kernel: dict[str, Any]) -> list[dict[str, Any]]:
    return [dict(mirror) for mirror in kernel["mirrors"]]


def gather_ui_layers(kernel: dict[str, Any]) -> list[str]:
    return list(kernel["ui"]["layers"])


def gather_ui_drivers(kernel: dict[str, Any]) -> list[dict[str, Any]]:
    return [dict(driver) for driver in kernel["ui"]["drivers"]]


def gather_function_register(kernel: dict[str, Any]) -> dict[str, list[str]]:
    return {key: list(values) for key, values in kernel["function_register"].items()}


def gather_events(kernel: dict[str, Any]) -> dict[str, Any]:
    return {
        "trace_event": dict(kernel["events"]["trace_event"]),
        "kinds": list(kernel["events"]["kinds"]),
    }


def gather_integrity(kernel: dict[str, Any]) -> dict[str, Any]:
    manifest = kernel["integrity"].get("manifest", {})
    return {
        "manifest": {
            "files": [dict(entry) for entry in manifest.get("files", [])]
        },
        "policy": dict(kernel["integrity"].get("policy", {})),
    }


def gather_rebuild(kernel: dict[str, Any]) -> list[str]:
    return list(kernel["rebuild"].get("steps", []))


def ghostlink_protocol(kernel: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = kernel if kernel is not None else load_kernel()
    return {
        "summary": summarize_kernel(payload),
        "determinism": gather_determinism(payload),
        "sovereignty": gather_sovereignty(payload),
        "laws": list(payload["laws"]),
        "output_rules": list(payload["output_rules"]),
        "capabilities": gather_capabilities(payload),
        "agents": list(payload["qcl_agents"]),
        "pipelines": list(payload["pipelines"]),
        "tools": list(payload["tools"]),
        "opcode": dict(payload["opcode"]),
        "expansion_shards": gather_expansion_shards(payload),
        "mirrors": gather_mirrors(payload),
        "ui_layers": gather_ui_layers(payload),
        "ui_drivers": gather_ui_drivers(payload),
        "function_register": gather_function_register(payload),
        "events": gather_events(payload),
        "integrity": gather_integrity(payload),
        "rebuild": gather_rebuild(payload),
    }


SECTION_HANDLERS = {
    "summary": summarize_kernel,
    "determinism": gather_determinism,
    "sovereignty": gather_sovereignty,
    "laws": lambda kernel: list(kernel["laws"]),
    "output_rules": lambda kernel: list(kernel["output_rules"]),
    "capabilities": gather_capabilities,
    "agents": lambda kernel: list(kernel["qcl_agents"]),
    "pipelines": lambda kernel: list(kernel["pipelines"]),
    "tools": lambda kernel: list(kernel["tools"]),
    "opcode": lambda kernel: dict(kernel["opcode"]),
    "expansion_shards": gather_expansion_shards,
    "mirrors": gather_mirrors,
    "ui_layers": gather_ui_layers,
    "ui_drivers": gather_ui_drivers,
    "function_register": gather_function_register,
    "events": gather_events,
    "integrity": gather_integrity,
    "rebuild": gather_rebuild,
    "protocol": ghostlink_protocol,
}


def list_sections() -> list[str]:
    return list(SECTION_HANDLERS.keys())


def _select_section(kernel: dict[str, Any], section: str) -> Any:
    try:
        handler = SECTION_HANDLERS[section]
    except KeyError as exc:
        raise ValueError(f"Unsupported section: {section}") from exc
    return handler(kernel)


def _render_section(section: str, data: Any) -> str:
    if section == "summary":
        pairs = [(key.replace("_", " ").title(), str(value)) for key, value in data.items()]
        width = max(len(label) for label, _ in pairs)
        return NEWLINE.join(f"{label:<{width}} : {value}" for label, value in pairs)
    if section == "determinism":
        pairs = [(key.replace("_", " ").title(), value) for key, value in data.items()]
        width = max(len(label) for label, _ in pairs)
        return NEWLINE.join(f"{label:<{width}} : {value}" for label, value in pairs)
    if section == "sovereignty":
        deny = ", ".join(data.get("denylist", [])) or "<none>"
        caps = [f"- {entry['cap']} (default={str(entry['default']).lower()})" for entry in data.get("capabilities", [])]
        block = ["Denylist: " + deny, "Capabilities:"] + caps
        return NEWLINE.join(block)
    if section == "agents":
        lines: list[str] = []
        for agent in data:
            head = f"[{agent['id']:02d}] {agent['role']}"
            duties = ", ".join(agent["duties"])
            invariants = ", ".join(agent["invariants"])
            lines.append(head)
            lines.append(f"  duties     : {duties}")
            lines.append(f"  invariants : {invariants}")
            lines.append(f"  in -> out  : {', '.join(agent['in'])} -> {', '.join(agent['out'])}")
        return NEWLINE.join(lines)
    if section == "pipelines":
        lines = []
        for pipe in data:
            lines.append(f"[{pipe['id']}] {pipe['name']} :: {pipe['action']}")
            lines.append(f"  multipaths : {', '.join(pipe['multipaths'])}")
        return NEWLINE.join(lines)
    if section == "tools":
        return NEWLINE.join(f"- {tool}" for tool in data)
    if section == "laws":
        lines = []
        for law in data:
            lines.append(f"{law['id']} {law['name']}")
            lines.append(f"  enforce : {', '.join(law['enforce'])}")
        return NEWLINE.join(lines)
    if section == "output_rules":
        lines = []
        for rule in data:
            lines.append(f"{rule['id']} {rule['name']}")
            lines.append(f"  subrules : {', '.join(rule['sub'])}")
        return NEWLINE.join(lines)
    if section == "opcode":
        grammar = data["grammar"]
        lines = ["Grammar:", grammar, "", "Mappings:"]
        lines.extend(f"- {entry}" for entry in data["map"])
        return NEWLINE.join(lines)
    if section == "capabilities":
        return NEWLINE.join(f"- {item}" for item in data)
    if section == "expansion_shards":
        lines = []
        for shard in data:
            variants = ", ".join(shard["variants"])
            lines.append(f"{shard['id']} {shard['name']} — {shard['purpose']} (variants: {variants})")
        return NEWLINE.join(lines)
    if section == "mirrors":
        return NEWLINE.join(f"{mirror['id']} {mirror['name']} — {mirror['domain']}" for mirror in data)
    if section == "ui_layers":
        return NEWLINE.join(f"- {layer}" for layer in data)
    if section == "ui_drivers":
        lines = []
        for driver in data:
            details = []
            if "grid" in driver:
                details.append(f"grid={driver['grid']}")
            if "glyphs" in driver:
                details.append(f"glyphs={','.join(driver['glyphs'])}")
            detail_str = ", ".join(details) if details else ""
            suffix = f" ({detail_str})" if detail_str else ""
            lines.append(f"{driver['name']} — {driver['desc']}{suffix}")
        return NEWLINE.join(lines)
    if section == "function_register":
        lines = []
        for category, entries in data.items():
            lines.append(f"[{category}]" )
            lines.extend(f"- {entry}" for entry in entries)
            lines.append("")
        return NEWLINE.join(lines).strip()
    if section == "events":
        schema = json.dumps(data["trace_event"], indent=2)
        kinds = NEWLINE.join(f"- {item}" for item in data["kinds"])
        return NEWLINE.join(["Schema:", schema, "", "Kinds:", kinds])
    if section == "integrity":
        lines = ["Manifest:"]
        for entry in data["manifest"]["files"]:
            lines.append(f"- {entry['path']} → {entry['sha256']}")
        policy = ", ".join(f"{key}={value}" for key, value in data["policy"].items()) or "<none>"
        lines.append("")
        lines.append(f"Policy: {policy}")
        return NEWLINE.join(lines)
    if section == "rebuild":
        return NEWLINE.join(f"{index}. {step}" for index, step in enumerate(data, start=1))
    if section == "protocol":
        return json.dumps(data, indent=2)
    raise ValueError(f"Unsupported section: {section}")


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Inspect the GhostLink MAX kernel artifact")
    parser.add_argument(
        "section",
        nargs="?",
        default="summary",
        choices=tuple(list_sections()),
        help="Kernel section to display.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of formatted text.")
    parser.add_argument(
        "--list-sections",
        action="store_true",
        help="List available sections and exit.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.list_sections:
        print(NEWLINE.join(list_sections()))
        return

    kernel = load_kernel()
    data = _select_section(kernel, args.section)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(_render_section(args.section, data))


if __name__ == "__main__":
    main()
