# Native UEFN Toolsets — 42.00

Extracted from UEFN 42.00 through `UToolsetRegistry` and Unreal reflection.

## Reproducing the dump

Run `dump_native_toolsets.py` from UEFN's Python console. The script first
loads the known Epic toolset modules for 42.00, then enumerates every production
`UToolsetDefinition` subclass visible to Unreal reflection.

The output is written under `FortniteGame/Saved/ToolsetDumps`:

- `registered-toolsets.json` contains the live registry schemas.
- `native-toolset-schemas.json` contains every discovered native class,
  including unregistered classes and classes without a valid schema.
- `module-load-report.json` records every attempted module load and any class
  that became visible after loading.

Rows without a schema are retained with `schemaAvailable: false`; load and
schema failures are reported instead of being silently omitted.

## Runtime registry

- Registered toolsets: 12
- Registered tools: 168
- Epic production `UToolsetDefinition` classes: 46
- Classes with a valid JSON schema: 45
- Tools across all discovered schemas: 456

| Registered toolset | Version | Tools |
|---|---:|---:|
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
| `VerseFieldsToolset.VerseFieldsToolset` | 1.0 | 6 |
| `WidgetAnimationToolset.WidgetAnimationToolset` | 1.0 | 10 |

## Registry filtering deltas

The native class schemas contain 11 tools that are filtered out of the live registry.

| Toolset | Registered | Class schema | Class-only tools |
|---|---:|---:|---:|
| `EditorToolset.EditorAppToolset` | 37 | 40 | 3 |
| `EditorToolset.LogsToolset` | 4 | 4 | 0 |
| `GameplayTagsToolset.GameplayTagsToolset` | 4 | 8 | 4 |
| `MVVMToolset.MVVMToolset` | 15 | 16 | 1 |
| `NiagaraToolsets.NiagaraToolset_Info` | 1 | 1 | 0 |
| `NiagaraToolsets.NiagaraToolset_Component` | 4 | 4 | 0 |
| `NiagaraToolsets.NiagaraToolset_System` | 46 | 46 | 0 |
| `NiagaraToolsets.NiagaraToolset_Assets` | 3 | 4 | 1 |
| `PhysicsToolsets.PhysicsAssetToolset` | 17 | 17 | 0 |
| `VerseFieldsToolset.VerseFieldsToolset` | 6 | 6 | 0 |
| `WidgetAnimationToolset.WidgetAnimationToolset` | 10 | 10 | 0 |
| `UMGToolSet.UMGToolSet` | 21 | 23 | 2 |

## Discovered native classes

`Registered` is the live registry state. An unregistered class may still expose a valid schema.

| Class | Registered | Schema | Tools |
|---|:---:|:---:|---:|
| `/Script/AIAssistant.AIAssistantToolset` | no | yes | 2 |
| `/Script/AutomationTestToolset.AutomationTestToolset` | no | yes | 7 |
| `/Script/CheatsToolset.CheatsToolset` | no | yes | 2 |
| `/Script/ConfigSettingsToolset.ConfigSettingsToolset` | no | yes | 8 |
| `/Script/DataRegistryToolset.DataRegistryTools` | no | yes | 7 |
| `/Script/DataflowAgent.DataflowAgentToolset` | no | yes | 22 |
| `/Script/DynamicUIToolset.DynamicUIToolset` | no | yes | 20 |
| `/Script/EditorToolset.EditorAppToolset` | yes | yes | 40 |
| `/Script/EditorToolset.LogsToolset` | yes | yes | 4 |
| `/Script/EditorToolset.SourceControlToolset` | no | yes | 4 |
| `/Script/EditorToolset.UserDefinedEnumToolset` | no | yes | 8 |
| `/Script/EditorToolset.UserDefinedStructToolset` | no | yes | 14 |
| `/Script/GASToolsets.AbilitySystemInspectorToolset` | no | yes | 4 |
| `/Script/GASToolsets.AttributeSetToolset` | no | yes | 2 |
| `/Script/GASToolsets.GameplayCueToolset` | no | yes | 8 |
| `/Script/GameFeaturesToolset.GameFeaturesToolset` | no | yes | 12 |
| `/Script/GameplayTagsToolset.GameplayTagsToolset` | yes | yes | 8 |
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
| `/Script/SemanticSearchToolset.SemanticSearchToolset` | no | yes | 2 |
| `/Script/SlateInspectorToolset.SlateInspectorToolset` | no | yes | 14 |
| `/Script/SpecialEventGameplayEditor.SpecialEventToolset` | no | yes | 2 |
| `/Script/StyleSheetsToolset.StyleSheetsToolset` | no | yes | 20 |
| `/Script/ToolsetRegistry.AgentSkillToolset` | no | yes | 4 |
| `/Script/UMGToolSet.UMGToolSet` | yes | yes | 23 |
| `/Script/ValkyrieToolset.DeviceToolset` | no | yes | 9 |
| `/Script/ValkyrieToolset.EntityToolset` | no | yes | 13 |
| `/Script/ValkyrieToolset.SessionToolset` | no | yes | 8 |
| `/Script/ValkyrieToolset.ValkyriePythonToolset` | no | yes | 2 |
| `/Script/ValkyrieToolset.VerseToolset` | no | yes | 10 |
| `/Script/VerseFieldsToolset.VerseFieldsToolset` | yes | yes | 6 |
| `/Script/WidgetAnimationToolset.WidgetAnimationToolset` | yes | yes | 10 |
| `/Script/WorldConditionsToolset.WorldConditionTools` | no | yes | 2 |

## Registered tools

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
- `EditorToolset.EditorAppToolset.GetCVarValue`
- `EditorToolset.EditorAppToolset.GetCameraTransform`
- `EditorToolset.EditorAppToolset.GetCollectionAssets`
- `EditorToolset.EditorAppToolset.GetContentBrowserPath`
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
- `EditorToolset.EditorAppToolset.SetCVarValue`
- `EditorToolset.EditorAppToolset.SetCameraTransform`
- `EditorToolset.EditorAppToolset.SetContentBrowserPath`
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
- `UMGToolSet.UMGToolSet.GetWidgetTreeDepth`
- `UMGToolSet.UMGToolSet.GetWidgets`
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
