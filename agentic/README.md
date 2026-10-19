# Run Kun's workflow in any project

> Repository edition: examples assume a clone at `~/.config/nvim-billy`.
> Run it with `NVIM_APPNAME=nvim-billy nvim`; see README.md and PROFILES.md.

**Installed October 18, 2026. Default assistant: Codex.** Run this from a terminal:

```sh
cd /path/to/your/project
kun
```

Replace the example path with your real project folder. You can also run
`kun /path/to/your/project` from anywhere. In Neovim, **Space a k** opens the same
workflow for the current project. Restart Neovim to load that shortcut.

The folder must be a Git repository with at least one commit. `kun` does not
initialize Git, stage everything, or invent a first commit for you. If you are
starting a new project, initialize it and review/commit the intended files first.
For a project on GitHub, clone it locally before running `kun` there.

The command prepares a separate Firstmate home for the project, registers your
existing checkout, detects candidate checks, selects Codex for the primary and
workers, and opens a named tmux session. Running it again reuses that project's
configuration and live primary session. Each project gets its own state.

The initial Codex prompt asks Firstmate to inspect the project and explain the
workflow. It does not assign an invented feature. **Starting `kun` starts a real
assistant conversation and can use your account quota.** Installation and the
verification described below made no model requests.

## What each layer does

| Layer | Job | What you do |
| --- | --- | --- |
| Neovim + NvChad | Edit, navigate, format, debug and review code | Keep editing normally; use Space g v for a diff. |
| tmux | Keep the supervisor and worker terminals organized | Ctrl+s then w chooses a window; Ctrl+s then d detaches. |
| Firstmate | Turn an outcome into scoped tasks, supervise workers and report results | Explain the desired behavior, constraints and stopping point. |
| Codex | Reason about the project and implement assigned work | Approve required actions and inspect results. Your existing model settings apply. |
| Treehouse | Lease/reuse isolated Git worktrees for tasks | Workers can edit separate branches without sharing one working directory. |
| No Mistakes | Validate a committed branch, repair eligible issues and deliver a PR | Use the gate after agreeing on the checks and publication scope. |
| Tasks AXI | Keep durable task records across sessions | Ask Firstmate for queued, active, blocked and completed work. |
| Lavish AXI | Support interactive planning/presentation workflows | Ask for a concrete plan or preview when it helps. |
| GitHub / Chrome DevTools / quota AXI | Give agents structured GitHub, browser and usage tools | Browser inspection needs a suitable browser session; installation alone does not attach one. |

You do not need to learn each CLI before your first task. Firstmate orchestrates
the layers; the smaller commands below let you inspect and troubleshoot them.
The manual assistant, task-note and worktree keys still work independently.

## First use, step by step

1. Save your code. Commit the work that a new worker needs to see. Uncommitted
   changes are preserved, but isolated worktrees start from committed history.
2. Run `kun` from the project's original checkout. Complete any genuine first-use
   trust or sign-in prompt shown by Codex. Existing Codex and GitHub logins were
   verified during setup; no new account or API key was created.
3. Let the onboarding turn finish. Check that it identifies the project,
   instructions, delivery mode and plausible build/test commands correctly.
4. Give one small task with an observable result. Start with one worker until
   you have seen the complete plan → implementation → validation → review cycle.
5. Read the result and evidence. Review the branch or PR that actually contains
   the changes; your original checkout does not display a worker's unmerged diff.
6. Decide whether to merge. Merge autonomy is off in both supported modes.

A useful first prompt:

> Inspect this project and propose one small improvement. Explain the affected
> files and the exact validation commands before implementing it. Use one Codex
> worker in an isolated worktree. Preserve my unrelated edits. Stop with a
> reviewable local branch; do not publish or merge. Afterward explain what changed,
> what I can now do, how to use it, and what you actually checked.

For a task you already understand:

> Fix [specific behavior]. Success means [observable result]. Keep scope to
> [files or component]. Run [known checks] and demonstrate the behavior. Prepare
> a PR through No Mistakes after validation, then wait for my merge decision.

Replace bracketed phrases with real details. A request to prepare a PR includes
publishing the branch after checks; choose a local result when that is what you
want. Installing the workflow does not publish anything by itself.

**You can now:** open a project-specific supervisor, give it a bounded task,
inspect evidence and approve the final integration yourself.

## Useful commands

Run project commands from inside that project, or add `--project /path/to/project`
before other arguments. `kun doctor` is independent of the current folder.

| Command | Behavior |
| --- | --- |
| `kun` | Prepare/reopen the project and attach to Firstmate. |
| `kun setup` | Prepare project configuration without starting a model. In PR mode it also initializes the local gate/daemon. |
| `kun start --print` | Perform setup and print the launch details without starting a model. This is a setup preview, not a read-only command. |
| `kun status` | Show saved project path, assistant, mode and candidate checks. |
| `kun status --json` | Show the full saved profile, including its home directory. |
| `kun doctor` | Check installed tools and read-only GitHub/Codex login status. |
| `kun check` | Preview the detected test command. |
| `kun check --run` | Actually execute the detected test command and record its exit code. |
| `kun check --kind build --run` | Execute the detected build command. Other kinds: lint, typecheck, check, format. |
| `kun setup --mode local-only` | Select local branch/worktree delivery for this project. |
| `kun setup --mode no-mistakes` | Select validation/PR delivery; requires an origin remote. |
| `kun setup --agent claude` | Explicitly switch this project's primary, default workers and pipeline to Claude Code. Codex is the default. |
| `kun exec -- no-mistakes status` | Inspect the project's gate using its private environment. |
| `kun exec -- no-mistakes doctor` | Diagnose the gate's requirements and configuration. |
| `kun exec -- no-mistakes` | Open the gate's interactive interface. Its wizard can offer to commit/push; read the prompts. |
| `kun exec -- tasks-axi list` | Inspect task records in this project's Firstmate environment. |

After changing the selected assistant, exit the old primary normally and run
`kun` again. Reopening a live session intentionally does not kill it or replace
the conversation. Existing workers keep the assistant they were launched with.

`kun check --run` runs actual project code, including any package-script lifecycle
hooks. A detected command is a candidate, not proof of correctness. CMake's
candidate assumes an already configured `build/` directory. Dependencies,
services, environment variables and SDKs still belong to the project. Run
`kun setup` again after changing its manifests to refresh detection.

## Local delivery and PR delivery

With a GitHub `origin`, the first setup selects **no-mistakes**. Otherwise it
selects **local-only**. You can choose explicitly with `--mode`; that selection
persists. An existing native Firstmate registry mode is preserved on reopening.

**Local-only:** Firstmate works with local branches/worktrees. It does not need a
GitHub repository. Ask it for a reviewable branch, inspect that branch and the
checks, then approve any merge into your source checkout.

**No Mistakes:** Setup adds a local Git remote named `no-mistakes` and initializes
its gate under this project's private state. Ordinary `git push origin` still
bypasses this tool; Firstmate should use the gate for its selected PR workflow.
When you explicitly push a committed branch through the gate, its pipeline can
perform review, tests, documentation/lint checks, publish the validated branch,
open a PR and watch CI. Its AI stages use your assistant account.

For manual submission after reviewing and committing your task branch:

```sh
git push no-mistakes HEAD
kun exec -- no-mistakes status
```

This submission can publish the validated result. A completed pipeline is not a
merge approval. Your repository's existing CI and branch-protection rules still
apply. If you contribute through a fork or lack write access to `origin`, keep
local-only mode until the correct push target is configured.

The launcher records likely check commands in `data/project-context.md`. It does
not silently commit a `.no-mistakes.yaml` or a new CI workflow. The onboarding
agent must verify the real commands and use any existing repository policy.
For a reproducible team policy, ask it to propose a `.no-mistakes.yaml`, review
it, and merge it through the project's normal process. No Mistakes reads trusted
default-branch policy for sensitive settings. A generic detector cannot infer a
project's intended behavior, secrets or deployment rules.

**You can now:** choose local review or gated PR delivery per project, while
keeping validation commands and merge decisions explicit.

## Sessions, permissions and practical workflow tips

- Your tmux prefix remains **Ctrl+s**. Then press **w** for windows, **s** for
  sessions, or **d** to detach. Detaching leaves agents working. Run `kun` again
  to return to that project's session.
- The supervisor window is named `helm`; workers may appear in other windows.
  Give steering instructions to the supervisor. If a worker is waiting for an
  approval, open its window and answer the actual prompt.
- To stop work, ask Firstmate to stop its workers and confirm their state, then
  exit the primary. Closing a terminal or detaching is not a reliable stop action.
- A Codex primary uses the upstream foreground watcher workflow. It has different
  waiting/resume ergonomics from a Claude primary; do not assume the video's
  Claude-specific background behavior is identical.
- Codex launches use `workspace-write` with `on-request` approvals. Permission
  adapters remove Firstmate's default bypass flags. Required approvals can pause
  workers; this is an interactive supervised setup.
- Firstmate's private home is added as a writable control directory. Workers
  have their own checkout. Startup fleet fetch/fast-forward is disabled for
  registered source checkouts, and startup branch pruning is disabled.
- Native Firstmate disables Codex worker lifecycle hooks while retaining its
  turn-end notification. The primary keeps the normal trust flow for its hooks.
- Use one writing task per worktree. Different terminal panes alone do not
  isolate edits. Ask for more workers only when the tasks are independent.
- Keep the final handoff concrete: changed behavior, files/branch/PR, commands
  actually run, observed results, limitations and the next action for you.

## Installed files, side effects and maintenance

| Item | Location / behavior |
| --- | --- |
| Global command | `~/.local/bin/kun` |
| Shared private tools | `~/.local/share/kun/toolchain` |
| Pinned Firstmate source | `~/.local/share/kun/firstmate` |
| Per-project Firstmate homes | `~/.local/share/kun/projects/<name>-<path-hash>` |
| Per-project No Mistakes state | `~/.local/share/kun/nm/<path-hash>` |
| Auditable launcher/install sources | This directory: kun.py, agent_guard.py, overlay.py, install.py. |
| Reviewed versions/checksums | toolchain-lock.json; installation.json is generated privately on install |

Project registration is a symlink to your original checkout, not a copied
application. The home contains its own preferences, task records and detected
context. Your project's existing `AGENTS.md`/`CLAUDE.md` are preserved. No global
agent preferences or shell profile were replaced.

No Mistakes init installs/refreshes its bundled user-level skill in
`~/.agents/skills/no-mistakes/SKILL.md` and
`~/.claude/skills/no-mistakes/SKILL.md`. Existing copies encountered by this
launcher are backed up under `~/.local/share/kun/backups/skills`. Its per-project
daemon can register a macOS LaunchAgent. These are native tool side effects.
The AXI packages' optional global hook installers were not run.

The private Firstmate checkout has two recorded integration overlays: worker
launch templates use absolute permission-adapter paths, and bootstrap skips
fleet sync for linked source projects. Hashes are recorded in installation.json.
This avoids relying on shell PATH order or silently fast-forwarding your source
checkout at startup. Unexpected edits to these vendor files are preserved and
cause installation to stop rather than overwrite them.

The installer pins reviewed versions. Re-running it reinstalls this reviewed
snapshot; it is not a rolling upgrade. Review upstream changes before updating
the pins/overlays. Do not blindly self-update the private Firstmate checkout over
its integration changes. Dedicated Python/Node launch paths keep project virtual
environments from accidentally selecting incompatible runtimes for the launcher
and AXI tools.

To reinstall this snapshot:

```sh
python3 ~/.config/nvim-billy/agentic/install.py
kun doctor
```

Before removing a project gate, stop its tasks and use
`kun exec -- no-mistakes eject --help` to inspect the native removal procedure.
For just stopping its service: `kun exec -- no-mistakes daemon stop`. Do not
delete active worktrees, project state or daemon files while they are in use.

## What was verified and what remains optional

Twenty functional checks cover project discovery, preserving existing work,
mode persistence, command detection/execution, real tmux startup/reuse and
permission adapters, including native worker templates after PATH changes.
Four installed-tool checks cover Firstmate dependency/bootstrap detection, a
real Treehouse lease, No Mistakes gate/daemon initialization, and Codex launch
flag acceptance. Neovim's new key/helper is checked without launching a model.

No model-driven worker task, paid validation pipeline, user-project push, PR or
merge was run. Your first bounded task exercises that final project-dependent
path. Tools are installed now; per-project setup happens when you run `kun`.

Pi, gnhf overnight loops, OpenSuperWhisper and a terminal-emulator migration
remain optional. They are not required for this Codex-based core workflow.

References: [Firstmate](https://github.com/kunchenguid/firstmate),
[Treehouse](https://github.com/kunchenguid/treehouse),
[No Mistakes](https://github.com/kunchenguid/no-mistakes),
[Codex security controls](https://developers.openai.com/codex/security/).
