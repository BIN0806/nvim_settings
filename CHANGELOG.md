# Settings change log

Each settings commit records what changed, why, usage changes, verification and
the checkpoint to restore. These initial commits package saved, tested milestones
from October 18, 2026; they are not an invented original development timeline.

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
