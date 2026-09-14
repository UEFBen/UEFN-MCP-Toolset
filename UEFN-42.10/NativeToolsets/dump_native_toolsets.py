"""Dump native UEFN 42.10 ToolsetRegistry schemas from the running editor.

Run this file inside UEFN's Python environment, for example:

    py "C:/path/to/dump_native_toolsets.py"

The generated files are written to ``FortniteGame/Saved/ToolsetDumps``.
Every discovered production ``UToolsetDefinition`` class is retained, including
unregistered classes, classes without a schema, and classes that fail to load.
"""

from __future__ import annotations

import json
from pathlib import Path
import re

import unreal


UEFN_VERSION = "42.10"


# Modules known to contain or aggregate Epic toolsets in UEFN 42.10. Loading
# them before reflection makes the result independent of which editor panels
# and features happened to be opened earlier in the session.
EPIC_TOOLSET_MODULES_42_10 = (
    "AIAssistant",
    "AIModuleToolset",
    "AnimationAssistantToolset",
    "AutomationTestToolset",
    "CheatsToolset",
    "ConfigSettingsToolset",
    "ConversationToolset",
    "DataRegistryToolset",
    "DataflowAgent",
    "DynamicUIToolset",
    "EditorToolset",
    "GASToolsets",
    "GameFeaturesToolset",
    "GameplayTagsToolset",
    "MCPClientToolset",
    "MeshLODToolset",
    "MeshPaintingToolset",
    "MeshPartitionModelingToolset",
    "MVVMToolset",
    "NavigationLoggerToolSet",
    "NiagaraToolsets",
    "PCGToolset",
    "PerfToolset",
    "PhysicsToolsets",
    "PluginToolset",
    "RewindDebuggerToolset",
    "SemanticSearchToolset",
    "SlateInspectorToolset",
    "SpecialEventGameplayEditor",
    "StateTreeToolset",
    "StyleSheetsToolset",
    "ToolsetRegistry",
    "UMGToolSet",
    "ValkyrieToolset",
    "VerseFieldsToolset",
    "WidgetAnimationToolset",
    "WorldConditionsToolset",
)


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _class_path_text(soft_class_path: object) -> str:
    return str(soft_class_path.export_text())


def _discover_class_paths() -> list[str]:
    return sorted(
        {
            _class_path_text(soft_class_path)
            for soft_class_path in unreal.ToolsetLibrary.get_derived_classes(
                unreal.ToolsetDefinition
            )
        },
        key=str.casefold,
    )


def _load_epic_toolset_modules() -> dict[str, object]:
    before = set(_discover_class_paths())
    modules: list[dict[str, object]] = []

    for module_name in EPIC_TOOLSET_MODULES_42_10:
        entry: dict[str, object] = {"module": module_name, "loaded": False}
        try:
            unreal.load_module(module_name)
            entry["loaded"] = True
        except Exception as exc:  # Keep probing the remaining native modules.
            entry["error"] = f"{type(exc).__name__}: {exc}"
        modules.append(entry)

    after = set(_discover_class_paths())
    return {
        "attempted": len(modules),
        "loaded": sum(1 for entry in modules if entry["loaded"]),
        "failed": sum(1 for entry in modules if not entry["loaded"]),
        "classesBefore": len(before),
        "classesAfter": len(after),
        "classesAdded": sorted(after - before, key=str.casefold),
        "modules": modules,
    }


def _split_class_path(class_path: str) -> tuple[str, str]:
    class_name = class_path.rsplit(".", 1)[-1]
    module_name = (
        class_path.split("/Script/", 1)[-1].split(".", 1)[0]
        if class_path.startswith("/Script/")
        else ""
    )
    return module_name, class_name


def _is_production_toolset(module_name: str, class_name: str) -> bool:
    if module_name == "ModelContextProtocolEditorTests":
        return False
    if module_name == "ToolsetRegistry" and class_name != "AgentSkillToolset":
        return False
    return True


def _schema_placeholder(schema: object) -> object:
    if not isinstance(schema, dict):
        return "<value>"
    if "default" in schema:
        return schema["default"]
    if "const" in schema:
        return schema["const"]
    enum_values = schema.get("enum")
    if isinstance(enum_values, list) and enum_values:
        return enum_values[0]

    choices = schema.get("oneOf") or schema.get("anyOf")
    if isinstance(choices, list) and choices:
        choice = next(
            (
                item
                for item in choices
                if isinstance(item, dict) and item.get("type") != "null"
            ),
            choices[0],
        )
        return _schema_placeholder(choice)

    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        schema_type = next(
            (item for item in schema_type if item != "null"),
            schema_type[0] if schema_type else None,
        )
    if schema_type == "object" or "properties" in schema:
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        if not isinstance(properties, dict) or not isinstance(required, list):
            return {}
        return {
            name: _schema_placeholder(properties.get(name, {}))
            for name in required
        }
    if schema_type == "array":
        items = schema.get("items")
        return [_schema_placeholder(items)] if isinstance(items, dict) else []
    if schema_type == "boolean":
        return False
    if schema_type == "integer":
        return 0
    if schema_type == "number":
        return 0.0
    if schema_type == "null":
        return None
    return "<string>" if schema_type == "string" else "<value>"


def _argument_template(input_schema: object) -> dict[str, object]:
    template = _schema_placeholder(input_schema)
    return template if isinstance(template, dict) else {}


def _agent_route(tool_name: str, server_alias: str = "uefn") -> str:
    normalized_name = re.sub(r"[^0-9A-Za-z_]+", "_", tool_name).strip("_")
    return f"mcp__{server_alias}__{normalized_name}"


def _build_agent_ready_index(
    registered_toolsets: list[dict[str, object]],
    native_toolsets: list[dict[str, object]],
    engine_version: str,
) -> dict[str, object]:
    registered_tools: dict[str, dict[str, object]] = {}
    for toolset in registered_toolsets:
        for tool in toolset.get("tools", []):
            if isinstance(tool, dict) and isinstance(tool.get("name"), str):
                registered_tools[str(tool["name"])] = tool

    records: dict[str, dict[str, object]] = {}
    for class_entry in native_toolsets:
        schema = class_entry.get("schema")
        if not isinstance(schema, dict):
            continue
        for tool in schema.get("tools", []):
            if not isinstance(tool, dict) or not isinstance(tool.get("name"), str):
                continue
            tool_name = str(tool["name"])
            class_registered = class_entry.get("registered") is True
            available = tool_name in registered_tools
            state = (
                "registered"
                if available
                else "filtered"
                if class_registered
                else "unregistered"
            )
            records[tool_name] = {
                "mcpToolName": tool_name,
                "agentRoute": _agent_route(tool_name),
                "toolset": tool_name.rsplit(".", 1)[0],
                "classPath": class_entry.get("classPath"),
                "classRegistered": class_registered,
                "availableInRegistry": available,
                "state": state,
                "description": tool.get("description", ""),
                "inputSchema": tool.get("inputSchema", {"type": "object"}),
                "outputSchema": tool.get("outputSchema"),
            }

    # The live registry is authoritative for callable tools and their schemas.
    for tool_name, tool in registered_tools.items():
        record = records.setdefault(
            tool_name,
            {
                "mcpToolName": tool_name,
                "agentRoute": _agent_route(tool_name),
                "toolset": tool_name.rsplit(".", 1)[0],
                "classPath": None,
                "classRegistered": True,
            },
        )
        record.update(
            {
                "availableInRegistry": True,
                "state": "registered",
                "description": tool.get("description", ""),
                "inputSchema": tool.get("inputSchema", {"type": "object"}),
                "outputSchema": tool.get("outputSchema"),
            }
        )

    tools = sorted(
        records.values(),
        key=lambda entry: str(entry["mcpToolName"]).casefold(),
    )
    for index, tool in enumerate(tools, start=1):
        arguments = _argument_template(tool["inputSchema"])
        tool["argumentsTemplate"] = arguments
        tool["agentCall"] = {
            "tool": tool["agentRoute"],
            "arguments": arguments,
        }
        tool["mcpCall"] = {
            "jsonrpc": "2.0",
            "id": index,
            "method": "tools/call",
            "params": {
                "name": tool["mcpToolName"],
                "arguments": arguments,
            },
        }

    return {
        "uefnVersion": UEFN_VERSION,
        "engineVersion": engine_version,
        "serverAlias": "uefn",
        "routeFormat": "mcp__<server-alias>__<tool-name-with-underscores>",
        "counts": {
            "tools": len(tools),
            "registered": sum(1 for tool in tools if tool["state"] == "registered"),
            "filtered": sum(1 for tool in tools if tool["state"] == "filtered"),
            "unregistered": sum(1 for tool in tools if tool["state"] == "unregistered"),
        },
        "tools": tools,
    }


def _build_agent_ready_markdown(agent_index: dict[str, object]) -> str:
    counts = agent_index["counts"]
    lines = [
        "# Agent-ready native UEFN tools — 42.10",
        "",
        "Generated from the native `UToolsetRegistry` schemas.",
        "",
        f"- Engine build: `{agent_index['engineVersion']}`",
        f"- Discovered tools: {counts['tools']}",
        f"- Available in the live registry: {counts['registered']}",
        f"- Filtered from registered class schemas: {counts['filtered']}",
        f"- Declared by unregistered classes: {counts['unregistered']}",
        "",
        "Only `registered` entries are immediately callable. `filtered` and",
        "`unregistered` entries document native schemas that are not currently",
        "available through the live registry.",
        "",
        "## Calling a tool",
        "",
        "`mcpToolName` is the authoritative dotted name passed to MCP `tools/call`.",
        "`agentRoute` is the normalized agent command. The `uefn` segment is the",
        "server alias; replace it if the MCP server uses a different alias.",
        "",
        "```json",
        "{",
        '  "jsonrpc": "2.0",',
        '  "id": 1,',
        '  "method": "tools/call",',
        '  "params": {',
        '    "name": "EditorToolset.EditorAppToolset.GetActiveEditorModes",',
        '    "arguments": {}',
        "  }",
        "}",
        "```",
        "",
        "The machine-readable [`agent-ready-tools.json`](agent-ready-tools.json)",
        "contains the full input/output schemas, agent-call templates, and complete",
        "`tools/call` request for every discovered tool.",
        "",
        "## Tool routes",
        "",
        "| State | MCP tool name | Agent route | Arguments template |",
        "|---|---|---|---|",
    ]
    for tool in agent_index["tools"]:
        arguments = json.dumps(
            tool["argumentsTemplate"],
            ensure_ascii=False,
            separators=(",", ":"),
        )
        lines.append(
            "| `{}` | `{}` | `{}` | `{}` |".format(
                tool["state"],
                tool["mcpToolName"],
                tool["agentRoute"],
                arguments,
            )
        )
    return "\n".join(lines) + "\n"


def _build_index_markdown(
    engine_version: str,
    registered_toolsets: list[dict[str, object]],
    native_toolsets: list[dict[str, object]],
    module_report: dict[str, object],
    agent_index: dict[str, object],
) -> str:
    schema_toolsets = [
        entry for entry in native_toolsets if entry["schemaAvailable"]
    ]
    class_schema_counts = {
        str(entry.get("toolsetName")): int(entry.get("toolCount", 0))
        for entry in schema_toolsets
        if entry.get("registered") is True and entry.get("toolsetName")
    }
    counts = agent_index["counts"]
    lines = [
        f"# Native UEFN Toolsets — {UEFN_VERSION}",
        "",
        f"Extracted from UEFN {UEFN_VERSION} through `UToolsetRegistry` and Unreal reflection.",
        "",
        f"- Engine build: `{engine_version}`",
        "",
        "## Reproducing the dump",
        "",
        "Run `dump_native_toolsets.py` from UEFN's Python console. The script first",
        f"loads the known Epic toolset modules for {UEFN_VERSION}, then enumerates every production",
        "`UToolsetDefinition` subclass visible to Unreal reflection.",
        "",
        "The output is written under `UnrealEditorFortnite/Saved/ToolsetDumps`:",
        "",
        "- `registered-toolsets.json` contains the live registry schemas.",
        "- `native-toolset-schemas.json` contains every discovered native class,",
        "  including unregistered classes and classes without a valid schema.",
        "- `module-load-report.json` records every attempted module load and any class",
        "  that became visible after loading.",
        "- `agent-ready-tools.json` maps every native tool to its MCP name, normalized",
        "  agent route, argument template, full schemas, and `tools/call` request.",
        "- `AGENT_READY.md` is the human-readable route and command index.",
        "- `INDEX.md` is this generated summary.",
        "",
        "Rows without a schema are retained with `schemaAvailable: false`; load and",
        "schema failures are reported instead of being silently omitted.",
        "",
        "See the [agent-ready MCP command index](AGENT_READY.md) for direct tool routes.",
        "",
        "## Runtime registry",
        "",
        f"- Registered toolsets: {len(registered_toolsets)}",
        f"- Registered tools: {counts['registered']}",
        f"- Epic production `UToolsetDefinition` classes: {len(native_toolsets)}",
        f"- Classes with a valid JSON schema: {len(schema_toolsets)}",
        f"- Tools across all discovered schemas: {counts['tools']}",
        "",
        "| Registered toolset | Version | Tools |",
        "|---|---:|---:|",
    ]
    for toolset in sorted(
        registered_toolsets,
        key=lambda entry: str(entry.get("name", "")).casefold(),
    ):
        lines.append(
            "| `{}` | {} | {} |".format(
                toolset.get("name", ""),
                toolset.get("version", ""),
                len(toolset.get("tools", [])),
            )
        )

    lines.extend(
        [
            "",
            "## Registry filtering deltas",
            "",
            f"The native class schemas contain {counts['filtered']} tools that are filtered out of the live registry.",
            "",
            "| Toolset | Registered | Class schema | Class-only tools |",
            "|---|---:|---:|---:|",
        ]
    )
    for toolset in sorted(
        registered_toolsets,
        key=lambda entry: str(entry.get("name", "")).casefold(),
    ):
        name = str(toolset.get("name", ""))
        registered_count = len(toolset.get("tools", []))
        class_count = class_schema_counts.get(name, registered_count)
        lines.append(
            f"| `{name}` | {registered_count} | {class_count} | {class_count - registered_count} |"
        )

    failed_modules = [
        entry
        for entry in module_report.get("modules", [])
        if isinstance(entry, dict) and not entry.get("loaded")
    ]
    lines.extend(
        [
            "",
            "## Module loading",
            "",
            f"- Attempted modules: {module_report['attempted']}",
            f"- Loaded modules: {module_report['loaded']}",
            f"- Failed modules: {module_report['failed']}",
        ]
    )
    if failed_modules:
        lines.extend(
            [
                "",
                "| Module | Error |",
                "|---|---|",
            ]
        )
        for entry in failed_modules:
            error = str(entry.get("error", "")).replace("|", "\\|")
            lines.append(f"| `{entry.get('module', '')}` | `{error}` |")

    lines.extend(
        [
            "",
            "## Discovered native classes",
            "",
            "`Registered` is the live registry state. An unregistered class may still expose a valid schema.",
            "",
            "| Class | Registered | Schema | Tools |",
            "|---|:---:|:---:|---:|",
        ]
    )
    for entry in native_toolsets:
        registered = "yes" if entry.get("registered") is True else "no"
        schema = "yes" if entry.get("schemaAvailable") is True else "no"
        lines.append(
            f"| `{entry.get('classPath', '')}` | {registered} | {schema} | {entry.get('toolCount', 0)} |"
        )

    lines.extend(["", "## Registered tools", ""])
    for toolset in sorted(
        registered_toolsets,
        key=lambda entry: str(entry.get("name", "")).casefold(),
    ):
        name = str(toolset.get("name", ""))
        lines.extend([f"### `{name}`", ""])
        tools = toolset.get("tools", [])
        for tool in sorted(
            tools if isinstance(tools, list) else [],
            key=lambda entry: str(entry.get("name", "")).casefold(),
        ):
            lines.append(f"- `{tool.get('name', '')}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _inspect_toolset_class(
    registry: object,
    class_path: str,
) -> dict[str, object]:
    module_name, class_name = _split_class_path(class_path)
    entry: dict[str, object] = {
        "classPath": class_path,
        "module": module_name,
        "className": class_name,
        "classLoaded": False,
        "registered": None,
        "schemaAvailable": False,
        "toolCount": 0,
        "schema": None,
    }

    try:
        toolset_class = unreal.load_class(None, class_path)
        if toolset_class is None:
            raise RuntimeError("unreal.load_class returned None")
        entry["classLoaded"] = True
    except Exception as exc:
        entry["loadError"] = f"{type(exc).__name__}: {exc}"
        return entry

    try:
        entry["registered"] = bool(
            registry.is_toolset_class_registered(toolset_class)
        )
    except Exception as exc:
        entry["registryError"] = f"{type(exc).__name__}: {exc}"

    try:
        schema_text = registry.get_toolset_json_schema(toolset_class)
        if not schema_text:
            entry["schemaError"] = "ToolsetRegistry returned an empty schema"
            return entry
        schema = json.loads(schema_text)
    except Exception as exc:
        entry["schemaError"] = f"{type(exc).__name__}: {exc}"
        return entry

    entry["schemaAvailable"] = True
    entry["toolCount"] = len(schema.get("tools", []))
    entry["toolsetName"] = schema.get("name")
    entry["version"] = schema.get("version")
    entry["schema"] = schema
    return entry


def dump_native_toolsets() -> dict[str, object]:
    engine_version = str(unreal.SystemLibrary.get_engine_version())
    if f"Release-{UEFN_VERSION}" not in engine_version:
        raise RuntimeError(
            f"Expected UEFN {UEFN_VERSION}, got {engine_version}"
        )

    module_report = _load_epic_toolset_modules()
    module_report["engineVersion"] = engine_version

    registry = unreal.ToolsetRegistry
    if not registry.is_available():
        raise RuntimeError("ToolsetRegistry is not available in this editor session")

    registered_toolsets = json.loads(registry.get_all_toolset_json_schemas())
    native_toolsets: list[dict[str, object]] = []

    for class_path in _discover_class_paths():
        module_name, class_name = _split_class_path(class_path)
        if not _is_production_toolset(module_name, class_name):
            continue
        native_toolsets.append(_inspect_toolset_class(registry, class_path))

    native_toolsets.sort(
        key=lambda entry: (
            str(entry["module"]).casefold(),
            str(entry["className"]).casefold(),
        )
    )

    schema_toolsets = [
        entry for entry in native_toolsets if entry["schemaAvailable"]
    ]
    unregistered_toolsets = [
        entry for entry in native_toolsets if entry["registered"] is False
    ]
    schema_errors = [
        entry for entry in native_toolsets if "schemaError" in entry
    ]
    agent_index = _build_agent_ready_index(
        registered_toolsets,
        native_toolsets,
        engine_version,
    )

    saved_dir = unreal.Paths.convert_relative_path_to_full(
        unreal.Paths.project_saved_dir()
    )
    output_dir = Path(saved_dir) / "ToolsetDumps"
    output_dir.mkdir(parents=True, exist_ok=True)

    _write_json(output_dir / "registered-toolsets.json", registered_toolsets)
    _write_json(output_dir / "native-toolset-schemas.json", native_toolsets)
    _write_json(output_dir / "module-load-report.json", module_report)
    _write_json(output_dir / "agent-ready-tools.json", agent_index)
    (output_dir / "AGENT_READY.md").write_text(
        _build_agent_ready_markdown(agent_index),
        encoding="utf-8",
    )
    (output_dir / "INDEX.md").write_text(
        _build_index_markdown(
            engine_version,
            registered_toolsets,
            native_toolsets,
            module_report,
            agent_index,
        ),
        encoding="utf-8",
    )

    summary = {
        "engineVersion": engine_version,
        "outputDirectory": str(output_dir),
        "registeredToolsets": len(registered_toolsets),
        "registeredTools": sum(
            len(toolset.get("tools", [])) for toolset in registered_toolsets
        ),
        "nativeClasses": len(native_toolsets),
        "classesWithSchema": len(schema_toolsets),
        "classesWithoutSchema": len(native_toolsets) - len(schema_toolsets),
        "unregisteredClasses": len(unregistered_toolsets),
        "unregisteredClassesWithSchema": sum(
            1 for entry in unregistered_toolsets if entry["schemaAvailable"]
        ),
        "nativeTools": sum(entry["toolCount"] for entry in schema_toolsets),
        "classLoadErrors": sum(
            1 for entry in native_toolsets if "loadError" in entry
        ),
        "schemaErrors": len(schema_errors),
        "moduleLoadsAttempted": module_report["attempted"],
        "moduleLoadsSucceeded": module_report["loaded"],
        "moduleLoadsFailed": module_report["failed"],
        "classesAddedByModuleLoading": len(module_report["classesAdded"]),
        "agentReadyTools": agent_index["counts"]["tools"],
        "agentReadyRegistered": agent_index["counts"]["registered"],
        "agentReadyFiltered": agent_index["counts"]["filtered"],
        "agentReadyUnregistered": agent_index["counts"]["unregistered"],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


result = dump_native_toolsets()
