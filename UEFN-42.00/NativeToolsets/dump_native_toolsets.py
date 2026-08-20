"""Dump native UEFN ToolsetRegistry schemas from the running editor.

Run this file inside UEFN's Python environment, for example:

    py "C:/path/to/dump_native_toolsets.py"

The JSON files are written to ``FortniteGame/Saved/ToolsetDumps``.
"""

from __future__ import annotations

import json
from pathlib import Path

import unreal


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _is_production_toolset(module_name: str, class_name: str) -> bool:
    if module_name == "ModelContextProtocolEditorTests":
        return False
    if module_name == "ToolsetRegistry" and class_name != "AgentSkillToolset":
        return False
    return True


def dump_native_toolsets() -> dict[str, object]:
    registry = unreal.ToolsetRegistry
    if not registry.is_available():
        raise RuntimeError("ToolsetRegistry is not available in this editor session")

    registered_toolsets = json.loads(registry.get_all_toolset_json_schemas())
    native_toolsets: list[dict[str, object]] = []

    class_paths = unreal.ToolsetLibrary.get_derived_classes(
        unreal.ToolsetDefinition
    )
    for soft_class_path in class_paths:
        class_path = soft_class_path.export_text()
        class_name = class_path.rsplit(".", 1)[-1]
        module_name = (
            class_path.split("/Script/", 1)[-1].split(".", 1)[0]
            if class_path.startswith("/Script/")
            else ""
        )
        if not _is_production_toolset(module_name, class_name):
            continue

        toolset_class = unreal.load_class(None, class_path)
        if toolset_class is None:
            continue

        schema_text = registry.get_toolset_json_schema(toolset_class)
        if not schema_text:
            continue

        schema = json.loads(schema_text)
        native_toolsets.append(
            {
                "classPath": class_path,
                "registered": bool(
                    registry.is_toolset_class_registered(toolset_class)
                ),
                "schema": schema,
            }
        )

    native_toolsets.sort(
        key=lambda entry: str(entry["schema"].get("name", "")).casefold()
    )

    saved_dir = unreal.Paths.convert_relative_path_to_full(
        unreal.Paths.project_saved_dir()
    )
    output_dir = Path(saved_dir) / "ToolsetDumps"
    output_dir.mkdir(parents=True, exist_ok=True)

    _write_json(output_dir / "registered-toolsets.json", registered_toolsets)
    _write_json(output_dir / "native-toolset-schemas.json", native_toolsets)

    summary = {
        "engineVersion": unreal.SystemLibrary.get_engine_version(),
        "outputDirectory": str(output_dir),
        "registeredToolsets": len(registered_toolsets),
        "registeredTools": sum(
            len(toolset.get("tools", [])) for toolset in registered_toolsets
        ),
        "nativeToolsets": len(native_toolsets),
        "nativeTools": sum(
            len(entry["schema"].get("tools", [])) for entry in native_toolsets
        ),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


result = dump_native_toolsets()
