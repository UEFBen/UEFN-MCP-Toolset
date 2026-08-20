"""Dump native UEFN 42.00 ToolsetRegistry schemas from the running editor.

Run this file inside UEFN's Python environment, for example:

    py "C:/path/to/dump_native_toolsets.py"

The JSON files are written to ``FortniteGame/Saved/ToolsetDumps``.
Every discovered production ``UToolsetDefinition`` class is retained, including
unregistered classes, classes without a schema, and classes that fail to load.
"""

from __future__ import annotations

import json
from pathlib import Path

import unreal


# Modules known to contain or aggregate Epic toolsets in UEFN 42.00. Loading
# them before reflection makes the result independent of which editor panels
# and features happened to be opened earlier in the session.
EPIC_TOOLSET_MODULES_42_00 = (
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

    for module_name in EPIC_TOOLSET_MODULES_42_00:
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
    module_report = _load_epic_toolset_modules()

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

    saved_dir = unreal.Paths.convert_relative_path_to_full(
        unreal.Paths.project_saved_dir()
    )
    output_dir = Path(saved_dir) / "ToolsetDumps"
    output_dir.mkdir(parents=True, exist_ok=True)

    _write_json(output_dir / "registered-toolsets.json", registered_toolsets)
    _write_json(output_dir / "native-toolset-schemas.json", native_toolsets)
    _write_json(output_dir / "module-load-report.json", module_report)

    summary = {
        "engineVersion": unreal.SystemLibrary.get_engine_version(),
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
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


result = dump_native_toolsets()
