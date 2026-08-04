# OneBot Expand Upstream Sync Design

## Goal

Synchronize `onebot_expand` with the current NapCat, SnowLuma, and LLBot
OneBot action registries, implement only verified compatibility changes, update
the plugin and documentation site, and publish the next patch release after all
validation gates pass.

## Scope

The synchronization covers:

- NapCat actions registered in `packages/napcat-onebot/action/router.ts`.
- SnowLuma actions registered through `packages/onebot/src/actions/index.ts`,
  including `.handle_quick_operation` from `api-handler.ts`.
- LLBot actions declared by `src/onebot11/action/types.ts`.
- The canonical plugin at `E:\plugins\onebot_expand`.
- The runtime copy at
  `E:\Neo-mofox-instance\bot-3693525299\neo-mofox\plugins\onebot_expand`.
- The VitePress site at `E:\onebot-expand-docs` when API, alias, Service, or
  version documentation changes.

The synchronization does not introduce a code generator, split existing
functional domains, or refactor unrelated plugin behavior.

## Source Of Truth

Each upstream source registry is authoritative for action presence. Repository
root action text files are secondary cross-checks only because they can be
untracked or stale. Deprecated and test-only NapCat actions listed in
`SKILL.md` are excluded before comparison.

The plugin action model is `ALL_APIS` plus each `APIDef.aliases`. A protocol
alias must resolve to one primary action and share the same Tool, Service
handler, and configuration switch. Chinese WebUI display names are never
protocol aliases.

## Synchronization Flow

1. Record the current commit of all three upstream repositories and update each
   `main` branch with a fast-forward pull.
2. Extract and normalize registered actions from each authoritative source.
3. Compare the normalized upstream union with plugin primary actions and
   aliases, producing missing, extra, alias, and deprecation sets.
4. Inspect the upstream implementation and payload schema for every actionable
   difference.
5. Add a focused failing contract test for each behavior or metadata change.
6. Apply the smallest implementation that makes the contract pass.
7. Update plugin documentation, documentation-site pages, and the runtime copy.
8. Increase the patch version only when repository content changes.
9. Run all validation gates and publish only after they pass.

## Implementation Rules

Every new primary action is added to the existing action constant class and
`ALL_APIS`, with source, category, compatibility flags, parameters, and aliases
derived from upstream code. It receives exactly one Tool class, one default
`false` action switch, and a method on the existing Service for its functional
domain. A new Service is allowed only for a genuinely new domain.

`enable_all_tools` and every `enable_<action>` remain `false` by default.
Services continue to call the shared API client directly and are not gated by
Tool switches. `manifest.json` continues to list Service components only.

The current uncommitted README dependency section is user work. Documentation
updates must preserve it and must not revert unrelated changes. The three
untracked upstream action snapshots are left untouched.

## Validation

Static and unit validation must prove:

- The API, Tool, and action-switch counts are equal.
- Every primary action has one Tool and no action is registered twice.
- Aliases are unique and resolve to their declared primary action.
- All Tool switches and the master switch default to disabled.
- The disabled master switch registers no Tools while Services and the inbound
  event handler remain available.
- README and `ACTION_INDEX.md` counts match runtime metadata.
- Plugin version values in `manifest.json`, `README.md`, and `plugin.py` match.
- The canonical plugin and runtime copy contain the same synchronized files.
- Python syntax, Pylance diagnostics, focused tests, and the complete plugin
  test suite have no synchronization regressions.
- The VitePress documentation build succeeds and detects no dead links.

For every new or changed protocol action, the NapCat WebSocket test adapter
calls the action with the smallest safe legal payload when
`ws://127.0.0.1:5326` is available. SnowLuma is tested when its endpoint is
available. Destructive actions require an explicitly identified test target and
are not invoked with production identifiers. Protocol unavailability is
reported as unverified and blocks publication of untested new action behavior.

## Version And Publication

If synchronization produces code or documentation changes, the patch version
moves from `1.0.11` to `1.0.12` in all three required plugin locations. After
fresh validation succeeds, publication runs:

```powershell
mpdt market package-update E:/plugins/onebot_expand
```

This command is authorized to build the package, create the GitHub Release, and
submit the market update. Publication is not attempted when there is no
upstream-driven release content or when any required validation gate fails.

## Failure Handling

No repository is reset, cleaned, or force-updated. A non-fast-forward pull,
unexpected local modification, failed test, documentation build failure,
Release failure, or market submission failure stops the workflow at that
stage. The final report identifies completed stages, exact upstream commit
ranges, test evidence, publication results, and remaining work without
claiming success for unverified stages.