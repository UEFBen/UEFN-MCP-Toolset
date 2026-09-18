# Native UEFN Toolsets — 42.20 (capture pending)

This directory is prepared for a **fresh UEFN 42.20 extraction**. It does not
contain 42.20 schemas or command indexes yet; the 42.10 data must not be used
as a substitute. The installed Epic manifest reports
`++Fortnite+Release-42.20-CL-58011042-Windows`, but the running editor and its
Toolset Registry still need to be queried.

## Capture

1. Open UEFN 42.20 with a project and enable its MCP Toolsets support.
2. In UEFN's Python console, run:

   ```text
   py "C:/Users/Shadow/Documents/FortniteTools/UEFN-MCP-Toolset/UEFN-42.20/NativeToolsets/dump_native_toolsets.py"
   ```

3. The script checks the running engine's `Release-42.20` string before
   extracting. It probes the known Epic toolset modules, records load failures,
   and enumerates all production `UToolsetDefinition` classes visible through
   reflection. It prints a summary and writes these six files to the current
   project's `Saved/ToolsetDumps/UEFN-42.20/`:

   - `registered-toolsets.json`
   - `native-toolset-schemas.json`
   - `module-load-report.json`
   - `agent-ready-tools.json`
   - `AGENT_READY.md`
   - `INDEX.md`

4. Review the engine build, module failures, registry counts, and schema
   errors. Copy the generated `INDEX.md`, `AGENT_READY.md`, and
   `agent-ready-tools.json` into this directory only after confirming they came
   from 42.20. Keep the three raw JSON files as capture evidence or archive
   them separately; previous version directories remain unchanged.

The `agent-ready-tools.json` index includes unregistered and registry-filtered
class tools for reference. Its `state` field distinguishes them from commands
actually callable through the live MCP registry.
