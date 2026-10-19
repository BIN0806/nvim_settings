# Verification results

Checked on October 18, 2026 with the installed configuration at
`~/.config/nvim-billy` and tmux 3.8.

Neovim 0.12.6; Mason clangd 23.1.0, clang-format 23.1.3, CodeLLDB 1.12.3.
CMake Debug build succeeded and the example printed `Total: 100`.

**All 24 original editor/tmux checks passed.** The Kun project command also
passed 20 functional checks, four installed-tool integration checks and a
Neovim key/helper check.

## C++ regression

- PASS: clangd attachment — ~/.local/share/nvim/mason/bin/clangd
- PASS: C++ hover — clangd resolves local symbols
- PASS: C++ completion — 26 vector member suggestions
- PASS: C++ diagnostics — unknown function detected
- PASS: completion menu — nvim-cmp LSP source loaded
- PASS: C++ syntax highlighting — C++ tree-sitter parser loaded
- PASS: format on save — clang-format reformatted a C++ buffer when written
- PASS: C++ breakpoint — CodeLLDB stopped at main.cpp:8
- PASS: debugger variables — total = 100
- PASS: debugger exit — Program resumed and exited

## Merged workflow

- PASS: surround and moving lines — Actual mapped keystrokes add/remove quotes and move a line
- PASS: external agent edits — Saved buffers refresh; unsaved edits survive
- PASS: editor sessions — Saved and restored two editor windows; terminal replay excluded
- PASS: Python language tools — Pyright type error, Ruff attachment and real formatting
- PASS: TypeScript language tools — TypeScript type error and Prettier formatting on save
- PASS: JSON language tools — JSON language server and Prettier work
- PASS: shell diagnostics — Bash language server reports ShellCheck quoting warning
- PASS: Git hunks — A real fixture change was detected, staged, and unstaged
- PASS: side-by-side Git review — Diffview opened and closed a real working-tree diff
- PASS: parallel-task isolation — Created a real independent Git worktree and branch
- PASS: agent launchers — Three installed CLIs resolve; no model calls made during verification

## tmux isolated server

- PASS: tmux configuration loads with preserved prefix and truecolor terminal
- PASS: split, clipboard, navigation and persistence bindings are loaded
- PASS: real two-pane layout saved; automatic process restoration disabled

## Scope and practical limits

Runtime checks use real Neovim buffers, language-server requests, formatting, a
compiled C++ program, CodeLLDB, temporary Git repositories and a dedicated tmux
server. Diffview verification waits until both old and new file contents are
displayed in editor windows before closing its asynchronous view.

Agent command resolution was checked without sending model requests. Codex
CLI help, updated Claude Code 2.1.303 version, and OpenCode help start successfully.
GitHub and Codex login status were verified read-only. A paid agent conversation
was not exercised. No user project was pushed or changed by the fixtures.

Syntax parsing passed for every configuration Lua file. Mason packages and all
configured syntax parsers installed successfully. Plugin revisions are recorded
in lazy-lock.json. Tests were run headlessly; an interactive iTerm GUI
session was not controlled. The guides list optional language SDKs, debug adapters
that are not part of the active setup. Core Kun orchestration tools are now
installed privately, with project setup deferred until the user invokes `kun`.

## Kun project workflow

- PASS: 20 functional checks in `agentic/test_kun.py`. These cover nested project
  discovery, preserving instructions/dirty files, separate project state,
  official registry mode/prefix parsing, native mode changes, redacting remote
  credentials, candidate command detection, an actual project test command,
  no-model launch preview, harness selection, actionable Git errors, real tmux
  startup/session reuse, permission adapters, native worker-template execution
  after PATH reordering, and disabling startup sync for linked source checkouts.
- PASS: Firstmate's installed bootstrap/dependency detection accepts the real
  tool versions and generated project home.
- PASS: Treehouse leases a real isolated worktree/branch and releases it.
- PASS: No Mistakes initializes a local gate/daemon against a disposable bare
  origin; repeat setup preserves it. Fixture daemon/LaunchAgent cleaned up.
- PASS: Native Codex accepts the selected sandbox/approval/add-directory flags
  without a model request.
- PASS: Installed Neovim Space a k callback resolves the launcher, finds the
  project and quotes a path containing spaces without starting an assistant.
- PASS: All Lua configuration files parse after the new mapping/helper.
- PASS: The installed launcher and Tasks AXI work with a minimal PATH that lacks
  Homebrew Python/Node entries, using their recorded runtime paths.

Sources: `agentic/test_kun.py`, `agentic/integration.py`, `kun-nvim.lua`.
Logs: `kun-tests.log`, `kun-integration.log`, `kun-nvim.log`, `kun-doctor.log`.
The tests deliberately do not submit a paid agent task, push a user project,
create a PR or merge. The first bounded real task remains the project-specific
end-to-end check. See [the command guide](../agentic/README.md).

Machine-readable results/logs are local ignored files beside this report.

## Repository export — October 18, 2026

The exported init.lua, Lua settings, style config and plugin lockfile match the
active configuration byte for byte. Local filesystem paths were normalized only
in copied documentation/test helpers; the editor settings were preserved.

Packaging verification passed:

- All 12 Neovim settings Lua files parse without loading plugins or agents.
- Python helper sources and JSON profile/toolchain/plugin records parse.
- A real disposable Git repository demonstrated that the opt-in pre-commit hook
  rejects a settings commit without CHANGELOG.md and accepts one with a staged
  log update.
- Repository Markdown file links resolve; the final stack remains the handbook's
  last section.
- The packaged files were checked for the original user-specific paths, private
  author email and common credential/private-key patterns. Machine installation
  records, local state, backups, binaries and transcript downloads are excluded.

The C++ and merged checkpoints come from saved milestones, as explained in
CHANGELOG.md. They are not represented as newly rerun full runtime suites. The
export introduced documentation/history tooling and preserved the active runtime
settings, so no additional paid agent call was made for packaging.
