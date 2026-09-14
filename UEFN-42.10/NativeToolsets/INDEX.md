# Native UEFN Toolsets — 42.10

Extracted from UEFN 42.10 through `UToolsetRegistry` and Unreal reflection.

- Engine build: `6.0.0-57819926+++Fortnite+Release-42.10`

## Reproducing the dump

Run `dump_native_toolsets.py` from UEFN's Python console. The script first
loads the known Epic toolset modules for 42.10, then enumerates every production
`UToolsetDefinition` subclass visible to Unreal reflection.

The output is written under `UnrealEditorFortnite/Saved/ToolsetDumps`:

- `registered-toolsets.json` contains the live registry schemas.
- `native-toolset-schemas.json` contains every discovered native class,
  including unregistered classes and classes without a valid schema.
- `module-load-report.json` records every attempted module load and any class
  that became visible after loading.
- `agent-ready-tools.json` maps every native tool to its MCP name, normalized
  agent route, argument template, full schemas, and `tools/call` request.
- `AGENT_READY.md` is the human-readable route and command index.
- `INDEX.md` is this generated summary.

Rows without a schema are retained with `schemaAvailable: false`; load and
schema failures are reported instead of being silently omitted.

See the [agent-ready MCP command index](AGENT_READY.md) for direct tool routes.

## Runtime registry

- Registered toolsets: 30
- Registered tools: 383
- Epic production `UToolsetDefinition` classes: 61
- Classes with a valid JSON schema: 60
- Tools across all discovered schemas: 762

| Registered toolset | Version | Tools |
|---|---:|---:|
| `editor_toolset.toolsets.actor.ActorTools` | 1.0 | 18 |
| `editor_toolset.toolsets.asset.AssetTools` | 1.0 | 17 |
| `editor_toolset.toolsets.curve_table.CurveTableTools` | 1.0 | 10 |
| `editor_toolset.toolsets.data_table.DataTableTools` | 1.0 | 11 |
| `editor_toolset.toolsets.material.MaterialTools` | 1.0 | 25 |
| `editor_toolset.toolsets.material_instance.MaterialInstanceTools` | 1.0 | 14 |
| `editor_toolset.toolsets.object.ObjectTools` | 1.0 | 6 |
| `editor_toolset.toolsets.primitive.PrimitiveTools` | 1.0 | 4 |
| `editor_toolset.toolsets.programmatic.ProgrammaticToolset` | 1.0 | 2 |
| `editor_toolset.toolsets.scene.SceneTools` | 1.0 | 24 |
| `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools` | 1.0 | 22 |
| `editor_toolset.toolsets.static_mesh.StaticMeshTools` | 1.0 | 16 |
| `editor_toolset.toolsets.texture.TextureTools` | 1.0 | 4 |
| `EditorToolset.EditorAppToolset` | 1.0 | 37 |
| `EditorToolset.LogsToolset` | 1.0 | 4 |
| `GameplayTagsToolset.GameplayTagsToolset` | 1.0 | 4 |
| `MVVMToolset.MVVMToolset` | 1.0 | 15 |
| `NiagaraToolsets.NiagaraToolset_Assets` | 1.0 | 3 |
| `NiagaraToolsets.NiagaraToolset_Component` | 1.0 | 4 |
| `NiagaraToolsets.NiagaraToolset_Info` | 1.0 | 1 |
| `NiagaraToolsets.NiagaraToolset_System` | 1.0 | 46 |
| `PhysicsToolsets.PhysicsAssetToolset` | 1.0 | 17 |
| `UMGToolSet.UMGToolSet` | 1.0 | 21 |
| `ValkyrieToolset.DeviceToolset` | 1.0 | 9 |
| `ValkyrieToolset.EntityToolset` | 1.0 | 13 |
| `ValkyrieToolset.SessionToolset` | 1.0 | 8 |
| `ValkyrieToolset.ValkyriePythonToolset` | 1.0 | 2 |
| `ValkyrieToolset.VerseToolset` | 1.0 | 10 |
| `VerseFieldsToolset.VerseFieldsToolset` | 1.0 | 6 |
| `WidgetAnimationToolset.WidgetAnimationToolset` | 1.0 | 10 |

## Registry filtering deltas

The native class schemas contain 18 tools that are filtered out of the live registry.

| Toolset | Registered | Class schema | Class-only tools |
|---|---:|---:|---:|
| `editor_toolset.toolsets.actor.ActorTools` | 18 | 18 | 0 |
| `editor_toolset.toolsets.asset.AssetTools` | 17 | 20 | 3 |
| `editor_toolset.toolsets.curve_table.CurveTableTools` | 10 | 10 | 0 |
| `editor_toolset.toolsets.data_table.DataTableTools` | 11 | 11 | 0 |
| `editor_toolset.toolsets.material.MaterialTools` | 25 | 25 | 0 |
| `editor_toolset.toolsets.material_instance.MaterialInstanceTools` | 14 | 14 | 0 |
| `editor_toolset.toolsets.object.ObjectTools` | 6 | 6 | 0 |
| `editor_toolset.toolsets.primitive.PrimitiveTools` | 4 | 4 | 0 |
| `editor_toolset.toolsets.programmatic.ProgrammaticToolset` | 2 | 2 | 0 |
| `editor_toolset.toolsets.scene.SceneTools` | 24 | 28 | 4 |
| `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools` | 22 | 22 | 0 |
| `editor_toolset.toolsets.static_mesh.StaticMeshTools` | 16 | 16 | 0 |
| `editor_toolset.toolsets.texture.TextureTools` | 4 | 4 | 0 |
| `EditorToolset.EditorAppToolset` | 37 | 40 | 3 |
| `EditorToolset.LogsToolset` | 4 | 4 | 0 |
| `GameplayTagsToolset.GameplayTagsToolset` | 4 | 8 | 4 |
| `MVVMToolset.MVVMToolset` | 15 | 16 | 1 |
| `NiagaraToolsets.NiagaraToolset_Assets` | 3 | 4 | 1 |
| `NiagaraToolsets.NiagaraToolset_Component` | 4 | 4 | 0 |
| `NiagaraToolsets.NiagaraToolset_Info` | 1 | 1 | 0 |
| `NiagaraToolsets.NiagaraToolset_System` | 46 | 46 | 0 |
| `PhysicsToolsets.PhysicsAssetToolset` | 17 | 17 | 0 |
| `UMGToolSet.UMGToolSet` | 21 | 23 | 2 |
| `ValkyrieToolset.DeviceToolset` | 9 | 9 | 0 |
| `ValkyrieToolset.EntityToolset` | 13 | 13 | 0 |
| `ValkyrieToolset.SessionToolset` | 8 | 8 | 0 |
| `ValkyrieToolset.ValkyriePythonToolset` | 2 | 2 | 0 |
| `ValkyrieToolset.VerseToolset` | 10 | 10 | 0 |
| `VerseFieldsToolset.VerseFieldsToolset` | 6 | 6 | 0 |
| `WidgetAnimationToolset.WidgetAnimationToolset` | 10 | 10 | 0 |

## Module loading

- Attempted modules: 37
- Loaded modules: 35
- Failed modules: 2

| Module | Error |
|---|---|
| `MCPClientToolset` | `KeyError: "load_module: 'MCPClientToolset' isn't a known module name"` |
| `SemanticSearchToolset` | `KeyError: "load_module: 'SemanticSearchToolset' isn't a known module name"` |

## Discovered native classes

`Registered` is the live registry state. An unregistered class may still expose a valid schema.

| Class | Registered | Schema | Tools |
|---|:---:|:---:|---:|
| `/EditorToolset/Python/editor_toolset/toolsets/actor_PY.ActorTools` | yes | yes | 18 |
| `/EditorToolset/Python/editor_toolset/toolsets/asset_PY.AssetTools` | yes | yes | 20 |
| `/EditorToolset/Python/editor_toolset/toolsets/blueprint_PY.BlueprintTools` | no | yes | 71 |
| `/EditorToolset/Python/editor_toolset/toolsets/curve_table_PY.CurveTableTools` | yes | yes | 10 |
| `/EditorToolset/Python/editor_toolset/toolsets/data_asset_PY.DataAssetTools` | no | yes | 2 |
| `/EditorToolset/Python/editor_toolset/toolsets/data_table_PY.DataTableTools` | yes | yes | 11 |
| `/EditorToolset/Python/editor_toolset/toolsets/material_instance_PY.MaterialInstanceTools` | yes | yes | 14 |
| `/EditorToolset/Python/editor_toolset/toolsets/material_PY.MaterialTools` | yes | yes | 25 |
| `/EditorToolset/Python/editor_toolset/toolsets/object_PY.ObjectTools` | yes | yes | 6 |
| `/EditorToolset/Python/editor_toolset/toolsets/primitive_PY.PrimitiveTools` | yes | yes | 4 |
| `/EditorToolset/Python/editor_toolset/toolsets/programmatic_PY.ProgrammaticToolset` | yes | yes | 2 |
| `/EditorToolset/Python/editor_toolset/toolsets/scene_PY.SceneTools` | yes | yes | 28 |
| `/EditorToolset/Python/editor_toolset/toolsets/skeletal_mesh_PY.SkeletalMeshTools` | yes | yes | 22 |
| `/EditorToolset/Python/editor_toolset/toolsets/static_mesh_PY.StaticMeshTools` | yes | yes | 16 |
| `/EditorToolset/Python/editor_toolset/toolsets/string_table_PY.StringTableTools` | no | yes | 9 |
| `/EditorToolset/Python/editor_toolset/toolsets/texture_PY.TextureTools` | yes | yes | 4 |
| `/Script/AIAssistant.AIAssistantToolset` | no | yes | 2 |
| `/Script/AutomationTestToolset.AutomationTestToolset` | no | yes | 7 |
| `/Script/CheatsToolset.CheatsToolset` | no | yes | 2 |
| `/Script/ConfigSettingsToolset.ConfigSettingsToolset` | no | yes | 8 |
| `/Script/DataflowAgent.DataflowAgentToolset` | no | yes | 22 |
| `/Script/DataRegistryToolset.DataRegistryTools` | no | yes | 7 |
| `/Script/DynamicUIToolset.DynamicUIToolset` | no | yes | 66 |
| `/Script/EditorToolset.EditorAppToolset` | yes | yes | 40 |
| `/Script/EditorToolset.LogsToolset` | yes | yes | 4 |
| `/Script/EditorToolset.SourceControlToolset` | no | yes | 4 |
| `/Script/EditorToolset.UserDefinedEnumToolset` | no | yes | 8 |
| `/Script/EditorToolset.UserDefinedStructToolset` | no | yes | 14 |
| `/Script/GameFeaturesToolset.GameFeaturesToolset` | no | yes | 12 |
| `/Script/GameplayTagsToolset.GameplayTagsToolset` | yes | yes | 8 |
| `/Script/GASToolsets.AbilitySystemInspectorToolset` | no | yes | 4 |
| `/Script/GASToolsets.AttributeSetToolset` | no | yes | 2 |
| `/Script/GASToolsets.GameplayCueToolset` | no | yes | 8 |
| `/Script/MVVMToolset.MVVMToolset` | yes | yes | 16 |
| `/Script/NavigationLoggerToolSet.NavigationLoggerToolSet` | no | yes | 9 |
| `/Script/NiagaraToolsets.NiagaraToolset` | no | no | 0 |
| `/Script/NiagaraToolsets.NiagaraToolset_Assets` | yes | yes | 4 |
| `/Script/NiagaraToolsets.NiagaraToolset_Blueprint` | no | yes | 2 |
| `/Script/NiagaraToolsets.NiagaraToolset_Component` | yes | yes | 4 |
| `/Script/NiagaraToolsets.NiagaraToolset_Info` | yes | yes | 1 |
| `/Script/NiagaraToolsets.NiagaraToolset_System` | yes | yes | 46 |
| `/Script/PCGToolset.PCGSpatialToolset` | no | yes | 1 |
| `/Script/PCGToolset.PCGToolset` | no | yes | 30 |
| `/Script/PerfToolset.GpuProfilerToolset` | no | yes | 1 |
| `/Script/PerfToolset.StatsToolset` | no | yes | 2 |
| `/Script/PhysicsToolsets.PhysicsAssetToolset` | yes | yes | 17 |
| `/Script/PluginToolset.PluginToolset` | no | yes | 17 |
| `/Script/RewindDebuggerToolset.RewindDebuggerToolset` | no | yes | 9 |
| `/Script/SlateInspectorToolset.SlateInspectorToolset` | no | yes | 14 |
| `/Script/SpecialEventGameplayEditor.SpecialEventToolset` | no | yes | 2 |
| `/Script/StyleSheetsToolset.StyleSheetsToolset` | no | yes | 20 |
| `/Script/ToolsetRegistry.AgentSkillToolset` | no | yes | 4 |
| `/Script/UMGToolSet.UMGToolSet` | yes | yes | 23 |
| `/Script/ValkyrieToolset.DeviceToolset` | yes | yes | 9 |
| `/Script/ValkyrieToolset.EntityToolset` | yes | yes | 13 |
| `/Script/ValkyrieToolset.SessionToolset` | yes | yes | 8 |
| `/Script/ValkyrieToolset.ValkyriePythonToolset` | yes | yes | 2 |
| `/Script/ValkyrieToolset.VerseToolset` | yes | yes | 10 |
| `/Script/VerseFieldsToolset.VerseFieldsToolset` | yes | yes | 6 |
| `/Script/WidgetAnimationToolset.WidgetAnimationToolset` | yes | yes | 10 |
| `/Script/WorldConditionsToolset.WorldConditionTools` | no | yes | 2 |

## Registered tools

### `editor_toolset.toolsets.actor.ActorTools`

- `editor_toolset.toolsets.actor.ActorTools.add_component`
- `editor_toolset.toolsets.actor.ActorTools.add_tag`
- `editor_toolset.toolsets.actor.ActorTools.diff`
- `editor_toolset.toolsets.actor.ActorTools.get_actor_bounds`
- `editor_toolset.toolsets.actor.ActorTools.get_actor_transform`
- `editor_toolset.toolsets.actor.ActorTools.get_component_actor`
- `editor_toolset.toolsets.actor.ActorTools.get_components`
- `editor_toolset.toolsets.actor.ActorTools.get_label`
- `editor_toolset.toolsets.actor.ActorTools.get_parent_component`
- `editor_toolset.toolsets.actor.ActorTools.get_root_component`
- `editor_toolset.toolsets.actor.ActorTools.get_tags`
- `editor_toolset.toolsets.actor.ActorTools.has_tag`
- `editor_toolset.toolsets.actor.ActorTools.look_at`
- `editor_toolset.toolsets.actor.ActorTools.remove_component`
- `editor_toolset.toolsets.actor.ActorTools.remove_tag`
- `editor_toolset.toolsets.actor.ActorTools.set_actor_transform`
- `editor_toolset.toolsets.actor.ActorTools.set_label`
- `editor_toolset.toolsets.actor.ActorTools.set_parent_component`

### `editor_toolset.toolsets.asset.AssetTools`

- `editor_toolset.toolsets.asset.AssetTools.create_folder`
- `editor_toolset.toolsets.asset.AssetTools.delete`
- `editor_toolset.toolsets.asset.AssetTools.duplicate`
- `editor_toolset.toolsets.asset.AssetTools.exists`
- `editor_toolset.toolsets.asset.AssetTools.find_assets`
- `editor_toolset.toolsets.asset.AssetTools.get_asset_class`
- `editor_toolset.toolsets.asset.AssetTools.get_asset_tags`
- `editor_toolset.toolsets.asset.AssetTools.get_dependencies`
- `editor_toolset.toolsets.asset.AssetTools.get_metadata_tags`
- `editor_toolset.toolsets.asset.AssetTools.get_referencers`
- `editor_toolset.toolsets.asset.AssetTools.is_dirty`
- `editor_toolset.toolsets.asset.AssetTools.list_folders`
- `editor_toolset.toolsets.asset.AssetTools.load_asset`
- `editor_toolset.toolsets.asset.AssetTools.move`
- `editor_toolset.toolsets.asset.AssetTools.reload_asset`
- `editor_toolset.toolsets.asset.AssetTools.save_assets`
- `editor_toolset.toolsets.asset.AssetTools.update_metadata_tags`

### `editor_toolset.toolsets.curve_table.CurveTableTools`

- `editor_toolset.toolsets.curve_table.CurveTableTools.add_key`
- `editor_toolset.toolsets.curve_table.CurveTableTools.add_row`
- `editor_toolset.toolsets.curve_table.CurveTableTools.create`
- `editor_toolset.toolsets.curve_table.CurveTableTools.diff`
- `editor_toolset.toolsets.curve_table.CurveTableTools.get_keys`
- `editor_toolset.toolsets.curve_table.CurveTableTools.import_file`
- `editor_toolset.toolsets.curve_table.CurveTableTools.list_rows`
- `editor_toolset.toolsets.curve_table.CurveTableTools.remove_row`
- `editor_toolset.toolsets.curve_table.CurveTableTools.rename_row`
- `editor_toolset.toolsets.curve_table.CurveTableTools.set_keys`

### `editor_toolset.toolsets.data_table.DataTableTools`

- `editor_toolset.toolsets.data_table.DataTableTools.add_rows`
- `editor_toolset.toolsets.data_table.DataTableTools.create`
- `editor_toolset.toolsets.data_table.DataTableTools.diff`
- `editor_toolset.toolsets.data_table.DataTableTools.get_rows`
- `editor_toolset.toolsets.data_table.DataTableTools.get_schema`
- `editor_toolset.toolsets.data_table.DataTableTools.import_file`
- `editor_toolset.toolsets.data_table.DataTableTools.list_rows`
- `editor_toolset.toolsets.data_table.DataTableTools.remove_rows`
- `editor_toolset.toolsets.data_table.DataTableTools.rename_rows`
- `editor_toolset.toolsets.data_table.DataTableTools.search_row_structs`
- `editor_toolset.toolsets.data_table.DataTableTools.set_rows`

### `editor_toolset.toolsets.material.MaterialTools`

- `editor_toolset.toolsets.material.MaterialTools.add_expression`
- `editor_toolset.toolsets.material.MaterialTools.connect_expressions`
- `editor_toolset.toolsets.material.MaterialTools.connect_to_output`
- `editor_toolset.toolsets.material.MaterialTools.create_function`
- `editor_toolset.toolsets.material.MaterialTools.create_material`
- `editor_toolset.toolsets.material.MaterialTools.create_parameter_collection`
- `editor_toolset.toolsets.material.MaterialTools.delete_expression`
- `editor_toolset.toolsets.material.MaterialTools.delete_parameter_group`
- `editor_toolset.toolsets.material.MaterialTools.delete_unused_expressions`
- `editor_toolset.toolsets.material.MaterialTools.diff_function`
- `editor_toolset.toolsets.material.MaterialTools.diff_material`
- `editor_toolset.toolsets.material.MaterialTools.disconnect_expressions`
- `editor_toolset.toolsets.material.MaterialTools.disconnect_from_output`
- `editor_toolset.toolsets.material.MaterialTools.get_expression_input_names`
- `editor_toolset.toolsets.material.MaterialTools.get_expression_inputs`
- `editor_toolset.toolsets.material.MaterialTools.get_expression_output_names`
- `editor_toolset.toolsets.material.MaterialTools.get_expressions`
- `editor_toolset.toolsets.material.MaterialTools.get_property_input`
- `editor_toolset.toolsets.material.MaterialTools.get_referencing_materials`
- `editor_toolset.toolsets.material.MaterialTools.get_statistics`
- `editor_toolset.toolsets.material.MaterialTools.layout_expressions`
- `editor_toolset.toolsets.material.MaterialTools.list_expression_classes`
- `editor_toolset.toolsets.material.MaterialTools.list_parameter_groups`
- `editor_toolset.toolsets.material.MaterialTools.recompile`
- `editor_toolset.toolsets.material.MaterialTools.rename_parameter_group`

### `editor_toolset.toolsets.material_instance.MaterialInstanceTools`

- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.clear_parameters`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.create`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.diff`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.get_scalar_parameter`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.get_static_switch_parameter`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.get_texture_parameter`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.get_vector_parameter`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.list_parameters`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.set_parameter_override`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.set_parent`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.set_scalar_parameter`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.set_static_switch_parameter`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.set_texture_parameter`
- `editor_toolset.toolsets.material_instance.MaterialInstanceTools.set_vector_parameter`

### `editor_toolset.toolsets.object.ObjectTools`

- `editor_toolset.toolsets.object.ObjectTools.get_class`
- `editor_toolset.toolsets.object.ObjectTools.get_properties`
- `editor_toolset.toolsets.object.ObjectTools.list_properties`
- `editor_toolset.toolsets.object.ObjectTools.reset_properties`
- `editor_toolset.toolsets.object.ObjectTools.search_subclasses`
- `editor_toolset.toolsets.object.ObjectTools.set_properties`

### `editor_toolset.toolsets.primitive.PrimitiveTools`

- `editor_toolset.toolsets.primitive.PrimitiveTools.add_cone`
- `editor_toolset.toolsets.primitive.PrimitiveTools.add_cube`
- `editor_toolset.toolsets.primitive.PrimitiveTools.add_cylinder`
- `editor_toolset.toolsets.primitive.PrimitiveTools.add_sphere`

### `editor_toolset.toolsets.programmatic.ProgrammaticToolset`

- `editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script`
- `editor_toolset.toolsets.programmatic.ProgrammaticToolset.get_execution_environment`

### `editor_toolset.toolsets.scene.SceneTools`

- `editor_toolset.toolsets.scene.SceneTools.add_actors_to_data_layer`
- `editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset`
- `editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_class`
- `editor_toolset.toolsets.scene.SceneTools.create_data_layer_asset`
- `editor_toolset.toolsets.scene.SceneTools.create_level`
- `editor_toolset.toolsets.scene.SceneTools.delete_folder`
- `editor_toolset.toolsets.scene.SceneTools.diff`
- `editor_toolset.toolsets.scene.SceneTools.find_actors`
- `editor_toolset.toolsets.scene.SceneTools.get_actor_asset_path`
- `editor_toolset.toolsets.scene.SceneTools.get_actors_in_data_layer`
- `editor_toolset.toolsets.scene.SceneTools.get_actors_in_folder`
- `editor_toolset.toolsets.scene.SceneTools.get_collision_channels`
- `editor_toolset.toolsets.scene.SceneTools.get_current_level`
- `editor_toolset.toolsets.scene.SceneTools.get_data_layers`
- `editor_toolset.toolsets.scene.SceneTools.get_folders`
- `editor_toolset.toolsets.scene.SceneTools.load_actors`
- `editor_toolset.toolsets.scene.SceneTools.load_level`
- `editor_toolset.toolsets.scene.SceneTools.remove_actors_from_data_layer`
- `editor_toolset.toolsets.scene.SceneTools.remove_from_scene`
- `editor_toolset.toolsets.scene.SceneTools.rename_folder`
- `editor_toolset.toolsets.scene.SceneTools.save_actor`
- `editor_toolset.toolsets.scene.SceneTools.set_actor_folder`
- `editor_toolset.toolsets.scene.SceneTools.trace_world`
- `editor_toolset.toolsets.scene.SceneTools.unload_actors`

### `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools`

- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.add_socket`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.assign_physics_asset`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_bone_children`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_bone_names`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_bone_parent`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_bounds`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_lod_count`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_material`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_material_slots`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_morph_target_names`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_physics_asset`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_section_count`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_skeleton`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_socket_bone`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_socket_names`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_socket_transform`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_vertex_count`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.import_file`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.remove_socket`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.rename_socket`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.set_material`
- `editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.set_socket_transform`

### `editor_toolset.toolsets.static_mesh.StaticMeshTools`

- `editor_toolset.toolsets.static_mesh.StaticMeshTools.generate_convex_collisions`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.generate_lods`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.get_bounds`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.get_lod_count`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.get_lod_thresholds`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.get_material`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.get_material_slots`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.get_triangle_count`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.get_vertex_count`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.import_file`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.is_nanite_enabled`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.remove_collisions`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.remove_lods`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.set_lod_thresholds`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.set_material`
- `editor_toolset.toolsets.static_mesh.StaticMeshTools.set_nanite_enabled`

### `editor_toolset.toolsets.texture.TextureTools`

- `editor_toolset.toolsets.texture.TextureTools.export_png`
- `editor_toolset.toolsets.texture.TextureTools.get_size`
- `editor_toolset.toolsets.texture.TextureTools.import_file`
- `editor_toolset.toolsets.texture.TextureTools.read_texture`

### `EditorToolset.EditorAppToolset`

- `EditorToolset.EditorAppToolset.AddAssetsToCollection`
- `EditorToolset.EditorAppToolset.CaptureAssetImage`
- `EditorToolset.EditorAppToolset.CaptureEditorImage`
- `EditorToolset.EditorAppToolset.CaptureViewport`
- `EditorToolset.EditorAppToolset.CreateCollection`
- `EditorToolset.EditorAppToolset.DestroyCollection`
- `EditorToolset.EditorAppToolset.FocusOnActors`
- `EditorToolset.EditorAppToolset.GetActiveEditorModes`
- `EditorToolset.EditorAppToolset.GetAssetThumbnails`
- `EditorToolset.EditorAppToolset.GetCameraTransform`
- `EditorToolset.EditorAppToolset.GetCollectionAssets`
- `EditorToolset.EditorAppToolset.GetContentBrowserPath`
- `EditorToolset.EditorAppToolset.GetCVarValue`
- `EditorToolset.EditorAppToolset.GetOpenAssets`
- `EditorToolset.EditorAppToolset.GetSelectedActors`
- `EditorToolset.EditorAppToolset.GetSelectedAssets`
- `EditorToolset.EditorAppToolset.GetSelectedOutlinerFolders`
- `EditorToolset.EditorAppToolset.GetShowFlag`
- `EditorToolset.EditorAppToolset.GetVisibleActors`
- `EditorToolset.EditorAppToolset.ListCollections`
- `EditorToolset.EditorAppToolset.ListEditorModes`
- `EditorToolset.EditorAppToolset.ListShowFlags`
- `EditorToolset.EditorAppToolset.OpenEditorForAsset`
- `EditorToolset.EditorAppToolset.RemoveAssetsFromCollection`
- `EditorToolset.EditorAppToolset.ScreenCoordsToWorld`
- `EditorToolset.EditorAppToolset.SearchCVars`
- `EditorToolset.EditorAppToolset.SelectActors`
- `EditorToolset.EditorAppToolset.SelectAssets`
- `EditorToolset.EditorAppToolset.SelectOutlinerFolders`
- `EditorToolset.EditorAppToolset.SetCameraTransform`
- `EditorToolset.EditorAppToolset.SetContentBrowserPath`
- `EditorToolset.EditorAppToolset.SetCVarValue`
- `EditorToolset.EditorAppToolset.SetEditorMode`
- `EditorToolset.EditorAppToolset.SetShowFlag`
- `EditorToolset.EditorAppToolset.SetViewportViewMode`
- `EditorToolset.EditorAppToolset.ShowNotification`
- `EditorToolset.EditorAppToolset.WorldPosToScreenCoords`

### `EditorToolset.LogsToolset`

- `EditorToolset.LogsToolset.GetLogCategories`
- `EditorToolset.LogsToolset.GetLogEntries`
- `EditorToolset.LogsToolset.GetVerbosity`
- `EditorToolset.LogsToolset.SetVerbosity`

### `GameplayTagsToolset.GameplayTagsToolset`

- `GameplayTagsToolset.GameplayTagsToolset.FindReferencersByTag`
- `GameplayTagsToolset.GameplayTagsToolset.GetTagInfo`
- `GameplayTagsToolset.GameplayTagsToolset.ListTags`
- `GameplayTagsToolset.GameplayTagsToolset.ListTagsInSource`

### `MVVMToolset.MVVMToolset`

- `MVVMToolset.MVVMToolset.AddViewModelProperty`
- `MVVMToolset.MVVMToolset.AddViewModelToWidget`
- `MVVMToolset.MVVMToolset.CreateViewBinding`
- `MVVMToolset.MVVMToolset.CreateViewEventBinding`
- `MVVMToolset.MVVMToolset.FixupMVVMData`
- `MVVMToolset.MVVMToolset.GetWidgetViewConfig`
- `MVVMToolset.MVVMToolset.ListBindableWidgetProperties`
- `MVVMToolset.MVVMToolset.ListConversionFunctions`
- `MVVMToolset.MVVMToolset.ListViewModels`
- `MVVMToolset.MVVMToolset.ListWidgetViewBindings`
- `MVVMToolset.MVVMToolset.ListWidgetViewEvents`
- `MVVMToolset.MVVMToolset.ListWidgetViewModels`
- `MVVMToolset.MVVMToolset.RemoveWidgetViewBinding`
- `MVVMToolset.MVVMToolset.SetBindingMode`
- `MVVMToolset.MVVMToolset.SetWidgetViewConfig`

### `NiagaraToolsets.NiagaraToolset_Assets`

- `NiagaraToolsets.NiagaraToolset_Assets.FindNiagaraScripts`
- `NiagaraToolsets.NiagaraToolset_Assets.GetAssetDiscoveryInfo`
- `NiagaraToolsets.NiagaraToolset_Assets.GetNiagaraScriptDigest`

### `NiagaraToolsets.NiagaraToolset_Component`

- `NiagaraToolsets.NiagaraToolset_Component.GetUserVariables`
- `NiagaraToolsets.NiagaraToolset_Component.GetVariable`
- `NiagaraToolsets.NiagaraToolset_Component.SetSystem`
- `NiagaraToolsets.NiagaraToolset_Component.SetVariable`

### `NiagaraToolsets.NiagaraToolset_Info`

- `NiagaraToolsets.NiagaraToolset_Info.UEnum_Info`

### `NiagaraToolsets.NiagaraToolset_System`

- `NiagaraToolsets.NiagaraToolset_System.AddEmitter`
- `NiagaraToolsets.NiagaraToolset_System.AddModule`
- `NiagaraToolsets.NiagaraToolset_System.AddRenderer`
- `NiagaraToolsets.NiagaraToolset_System.AddSetParameterEntry`
- `NiagaraToolsets.NiagaraToolset_System.AddSetParametersModule`
- `NiagaraToolsets.NiagaraToolset_System.AddUserVariables`
- `NiagaraToolsets.NiagaraToolset_System.ApplyStackIssueFix`
- `NiagaraToolsets.NiagaraToolset_System.CreateNiagaraSystem`
- `NiagaraToolsets.NiagaraToolset_System.GetAvailableDynamicInputs`
- `NiagaraToolsets.NiagaraToolset_System.GetDataInterfaceSchema`
- `NiagaraToolsets.NiagaraToolset_System.GetDynamicInputChain`
- `NiagaraToolsets.NiagaraToolset_System.GetDynamicInputSchema`
- `NiagaraToolsets.NiagaraToolset_System.GetDynamicInputSchemaFromAsset`
- `NiagaraToolsets.NiagaraToolset_System.GetEmitterData`
- `NiagaraToolsets.NiagaraToolset_System.GetEmitterInputValues`
- `NiagaraToolsets.NiagaraToolset_System.GetEmitterSchema`
- `NiagaraToolsets.NiagaraToolset_System.GetEmitterSummary`
- `NiagaraToolsets.NiagaraToolset_System.GetEmitterTopology`
- `NiagaraToolsets.NiagaraToolset_System.GetModuleInputValues`
- `NiagaraToolsets.NiagaraToolset_System.GetModuleSchema`
- `NiagaraToolsets.NiagaraToolset_System.GetModuleSchemaFromAsset`
- `NiagaraToolsets.NiagaraToolset_System.GetModuleTopology`
- `NiagaraToolsets.NiagaraToolset_System.GetRendererData`
- `NiagaraToolsets.NiagaraToolset_System.GetRendererSchema`
- `NiagaraToolsets.NiagaraToolset_System.GetScriptStackInputValues`
- `NiagaraToolsets.NiagaraToolset_System.GetScriptStackTopology`
- `NiagaraToolsets.NiagaraToolset_System.GetStackInputData`
- `NiagaraToolsets.NiagaraToolset_System.GetStackInputSchema`
- `NiagaraToolsets.NiagaraToolset_System.GetStackInputTopology`
- `NiagaraToolsets.NiagaraToolset_System.GetStackIssues`
- `NiagaraToolsets.NiagaraToolset_System.GetSystemCompileState`
- `NiagaraToolsets.NiagaraToolset_System.GetSystemData`
- `NiagaraToolsets.NiagaraToolset_System.GetSystemDependencies`
- `NiagaraToolsets.NiagaraToolset_System.GetSystemSchema`
- `NiagaraToolsets.NiagaraToolset_System.GetSystemSummary`
- `NiagaraToolsets.NiagaraToolset_System.GetUserVariables`
- `NiagaraToolsets.NiagaraToolset_System.RemoveEmitter`
- `NiagaraToolsets.NiagaraToolset_System.RemoveModule`
- `NiagaraToolsets.NiagaraToolset_System.RemoveRenderer`
- `NiagaraToolsets.NiagaraToolset_System.RemoveSetParameterEntry`
- `NiagaraToolsets.NiagaraToolset_System.RemoveUserVariables`
- `NiagaraToolsets.NiagaraToolset_System.SetEmitterData`
- `NiagaraToolsets.NiagaraToolset_System.SetModuleEnabled`
- `NiagaraToolsets.NiagaraToolset_System.SetRendererData`
- `NiagaraToolsets.NiagaraToolset_System.SetStackInputData`
- `NiagaraToolsets.NiagaraToolset_System.SetSystemData`

### `PhysicsToolsets.PhysicsAssetToolset`

- `PhysicsToolsets.PhysicsAssetToolset.AddBody`
- `PhysicsToolsets.PhysicsAssetToolset.AddConstraint`
- `PhysicsToolsets.PhysicsAssetToolset.CreateFromMesh`
- `PhysicsToolsets.PhysicsAssetToolset.GetBodyMassScale`
- `PhysicsToolsets.PhysicsAssetToolset.GetBodyNames`
- `PhysicsToolsets.PhysicsAssetToolset.GetBodyPhysicsMode`
- `PhysicsToolsets.PhysicsAssetToolset.GetBodyShapes`
- `PhysicsToolsets.PhysicsAssetToolset.GetConstraints`
- `PhysicsToolsets.PhysicsAssetToolset.RemoveBody`
- `PhysicsToolsets.PhysicsAssetToolset.RemoveConstraint`
- `PhysicsToolsets.PhysicsAssetToolset.RemoveShape`
- `PhysicsToolsets.PhysicsAssetToolset.SetBodyMassScale`
- `PhysicsToolsets.PhysicsAssetToolset.SetBodyPhysicsMode`
- `PhysicsToolsets.PhysicsAssetToolset.SetBox`
- `PhysicsToolsets.PhysicsAssetToolset.SetCapsule`
- `PhysicsToolsets.PhysicsAssetToolset.SetConstraintLimits`
- `PhysicsToolsets.PhysicsAssetToolset.SetSphere`

### `UMGToolSet.UMGToolSet`

- `UMGToolSet.UMGToolSet.AddUIComponent`
- `UMGToolSet.UMGToolSet.AddWidget`
- `UMGToolSet.UMGToolSet.CompileWidgetBlueprint`
- `UMGToolSet.UMGToolSet.CreateWidgetBlueprint`
- `UMGToolSet.UMGToolSet.GetNamedSlots`
- `UMGToolSet.UMGToolSet.GetWidgetClassInfo`
- `UMGToolSet.UMGToolSet.GetWidgetDescription`
- `UMGToolSet.UMGToolSet.GetWidgets`
- `UMGToolSet.UMGToolSet.GetWidgetTreeDepth`
- `UMGToolSet.UMGToolSet.ListWidgetBlueprints`
- `UMGToolSet.UMGToolSet.ListWidgetClasses`
- `UMGToolSet.UMGToolSet.MoveUIComponent`
- `UMGToolSet.UMGToolSet.MoveWidget`
- `UMGToolSet.UMGToolSet.RemoveUIComponent`
- `UMGToolSet.UMGToolSet.RemoveWidget`
- `UMGToolSet.UMGToolSet.RenameWidget`
- `UMGToolSet.UMGToolSet.ReplaceWidgetWithChild`
- `UMGToolSet.UMGToolSet.ReplaceWidgetWithNamedSlot`
- `UMGToolSet.UMGToolSet.ReplaceWidgetWithTemplate`
- `UMGToolSet.UMGToolSet.SetNamedSlotContent`
- `UMGToolSet.UMGToolSet.WrapWidgets`

### `ValkyrieToolset.DeviceToolset`

- `ValkyrieToolset.DeviceToolset.AddEventBinding`
- `ValkyrieToolset.DeviceToolset.GetBindingOptions`
- `ValkyrieToolset.DeviceToolset.GetDeviceProperties`
- `ValkyrieToolset.DeviceToolset.ListDeviceAssets`
- `ValkyrieToolset.DeviceToolset.ListDeviceProperties`
- `ValkyrieToolset.DeviceToolset.ListEventBindings`
- `ValkyrieToolset.DeviceToolset.PlaceDevice`
- `ValkyrieToolset.DeviceToolset.RemoveEventBinding`
- `ValkyrieToolset.DeviceToolset.SetDeviceProperty`

### `ValkyrieToolset.EntityToolset`

- `ValkyrieToolset.EntityToolset.AddComponent`
- `ValkyrieToolset.EntityToolset.CreateEntity`
- `ValkyrieToolset.EntityToolset.DeleteEntity`
- `ValkyrieToolset.EntityToolset.FindEntities`
- `ValkyrieToolset.EntityToolset.GetComponentProperty`
- `ValkyrieToolset.EntityToolset.GetComponents`
- `ValkyrieToolset.EntityToolset.GetEntityTransform`
- `ValkyrieToolset.EntityToolset.ListComponentClasses`
- `ValkyrieToolset.EntityToolset.ListComponentProperties`
- `ValkyrieToolset.EntityToolset.ListEntityClasses`
- `ValkyrieToolset.EntityToolset.RemoveComponent`
- `ValkyrieToolset.EntityToolset.SetComponentProperty`
- `ValkyrieToolset.EntityToolset.SetEntityTransform`

### `ValkyrieToolset.SessionToolset`

- `ValkyrieToolset.SessionToolset.GetClientLogEntries`
- `ValkyrieToolset.SessionToolset.GetGameState`
- `ValkyrieToolset.SessionToolset.GetSessionStatus`
- `ValkyrieToolset.SessionToolset.PushChanges`
- `ValkyrieToolset.SessionToolset.StartGame`
- `ValkyrieToolset.SessionToolset.StartSession`
- `ValkyrieToolset.SessionToolset.StopGame`
- `ValkyrieToolset.SessionToolset.StopSession`

### `ValkyrieToolset.ValkyriePythonToolset`

- `ValkyrieToolset.ValkyriePythonToolset.EnablePythonInUEFN`
- `ValkyrieToolset.ValkyriePythonToolset.IsPythonEnabledInUEFN`

### `ValkyrieToolset.VerseToolset`

- `ValkyrieToolset.VerseToolset.BuildAll`
- `ValkyrieToolset.VerseToolset.Copy`
- `ValkyrieToolset.VerseToolset.CreateDirectory`
- `ValkyrieToolset.VerseToolset.Delete`
- `ValkyrieToolset.VerseToolset.Grep`
- `ValkyrieToolset.VerseToolset.ListFiles`
- `ValkyrieToolset.VerseToolset.Move`
- `ValkyrieToolset.VerseToolset.ReadFile`
- `ValkyrieToolset.VerseToolset.Replace`
- `ValkyrieToolset.VerseToolset.WriteFile`

### `VerseFieldsToolset.VerseFieldsToolset`

- `VerseFieldsToolset.VerseFieldsToolset.AddVerseField`
- `VerseFieldsToolset.VerseFieldsToolset.BindWidgetPropertyToVerseField`
- `VerseFieldsToolset.VerseFieldsToolset.DuplicateVerseField`
- `VerseFieldsToolset.VerseFieldsToolset.EditVerseField`
- `VerseFieldsToolset.VerseFieldsToolset.ListVerseFields`
- `VerseFieldsToolset.VerseFieldsToolset.RemoveVerseField`

### `WidgetAnimationToolset.WidgetAnimationToolset`

- `WidgetAnimationToolset.WidgetAnimationToolset.AddWidgetToAnimation`
- `WidgetAnimationToolset.WidgetAnimationToolset.CreateWidgetAnimation`
- `WidgetAnimationToolset.WidgetAnimationToolset.FindWidgetAnimation`
- `WidgetAnimationToolset.WidgetAnimationToolset.GetWidgetAnimationBindings`
- `WidgetAnimationToolset.WidgetAnimationToolset.ListWidgetAnimations`
- `WidgetAnimationToolset.WidgetAnimationToolset.RemoveWidgetAnimation`
- `WidgetAnimationToolset.WidgetAnimationToolset.RemoveWidgetBinding`
- `WidgetAnimationToolset.WidgetAnimationToolset.RenameWidgetAnimation`
- `WidgetAnimationToolset.WidgetAnimationToolset.SetWidgetAnimationDisplayLabel`
- `WidgetAnimationToolset.WidgetAnimationToolset.SetWidgetAnimationLength`
