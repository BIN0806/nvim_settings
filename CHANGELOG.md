# Settings change log

Each settings commit records what changed, why, usage changes, verification and
the checkpoint to restore. These initial commits package saved, tested milestones
from October 18, 2026; they are not an invented original development timeline.

## 2026-10-18 — full profile and project-scoped Codex workflow

- **Checkpoint:** `setup-2026-10-18-full`; maintained branch `main`.
- **Source:** the active Neovim files, including Space a k and the reviewed Kun
  launcher sources. All active init/Lua/lock/style files are preserved verbatim.
- **Added:** a reusable kun command for separate Firstmate project homes, Codex
  primary/workers, Treehouse leases, No Mistakes delivery and private AXI tools.
  The optional installer pins reviewed external versions; opening Neovim does
  not install the toolchain or start an agent.
- **Use:** install through agentic/install.py when wanted; run kun in an actual
  Git project or use Space a k. Both delivery modes require merge approval.
- **History:** add this log, descriptive commit template, profile metadata,
  opt-in pre-commit log enforcement, annotated checkpoints and PROFILES.md.
- **Documentation:** include all six video breakdowns, integrated beginner/daily
  guides, final stack, command instructions, C++ example and context template.
  Clone-relative test paths and public documentation replace original machine
  paths. Credentials, state, binaries, backups and transcripts are excluded.
- **Verification:** original core toolchain passed 20 functional and four
  installed-tool checks plus the Neovim helper check, with no model calls.
  Export checks: all Lua/Python/JSON parse; history hook rejects an unlogged
  settings edit and accepts it with a staged log; active config matches exactly;
  document links resolve; staged files/history checked for accidental local data.
- **Restore:** setup-2026-10-18-merged removes the Kun integration from the editor;
  codex/profile-cpp keeps the smaller C++ profile. Git rollback does not uninstall
  separately installed tools or restore private agent state.

## 2026-10-18 — combined editor and tmux

- **Checkpoint:** `setup-2026-10-18-merged`.
- **Source:** the combined profile, using the saved mappings/workspace helper
  immediately before the later Kun shortcut was added.
- **Added:** Python, JS/TS, shell and JSON tools; mini.ai/surround/move/sessions;
  Diffview, Zen Mode, Git hunk/LazyGit keys, guarded external-file refresh,
  manual assistant launchers and Git worktree helpers.
- **tmux:** preserve Ctrl+s; matching colors, clipboard/splits/navigation,
  Resurrect/Continuum layout saving, manual restore and process replay off.
- **Use:** Space a a chooses an assistant; Space a w creates a worktree;
  Space g v reviews a diff; Space S s / Space S r saves/restores editor layouts.
- **Why:** combine useful tutorial features without duplicate managers/engines.
- **Verification:** prior recorded results include 10 C++, 11 merged-workflow
  and 3 tmux checks. Credentials and live model requests are outside this import.
- **Restore:** `setup-2026-10-18-cpp` returns to the smaller profile;
  `setup-2026-10-18-merged` restores this combined pre-Kun milestone.

## 2026-10-18 — cpp foundation

- **Checkpoint:** `setup-2026-10-18-cpp`; profile branch `codex/profile-cpp`.
- **Source:** the saved working C++ configuration before the multi-video merge.
- **Added:** NvChad v2.5, Catppuccin, clangd/clang-tidy, clang-format on save,
  Mason-managed tools, CodeLLDB/DAP/UI, current Treesitter API and pinned plugins.
- **Use:** Space f f finds files; g d jumps to a definition; Space f m formats;
  Space d b sets a breakpoint; Space d r starts/continues debugging.
- **Why:** retain a smaller, usable C++ profile alongside the full setup.
- **Verification:** the saved milestone passed 10 real C++ runtime checks,
  including a CodeLLDB stop with `total = 100`. This import adds no runtime code.
- **Restore:** clone this tag/branch into a separate NVIM_APPNAME directory, or
  switch a clean checkout to this tag and restore its plugin lockfile.
