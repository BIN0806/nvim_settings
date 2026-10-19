# Billy's Neovim settings — combined profile

main now contains the combined Neovim/tmux daily setup: the C++ IDE plus Python,
JS/TS, shell/JSON tools, editing helpers, sessions, Git review, focus mode, manual
coding-assistant terminals and independent worktrees. The repository root is the
actual installable Neovim config; tmux.conf is optional and installed separately.

```sh
git clone https://github.com/BIN0806/nvim_settings.git ~/.config/nvim-billy
NVIM_APPNAME=nvim-billy nvim
```

Requires Neovim 0.12 (tested 0.12.6), Git, language SDKs as needed, and a Nerd Font.
Use `:Lazy restore`, `:MasonInstallAll` and the configured Treesitter parsers.
Choose `codex/profile-cpp` when cloning for the smaller C++-only profile; use a
different NVIM_APPNAME to keep its data/state separate. No agents start on launch.

Read [CHANGELOG.md](CHANGELOG.md) for changes, usage, verification and restore
points. The annotated tags `setup-2026-10-18-cpp` and
`setup-2026-10-18-merged` preserve exact snapshots. Future settings commits must
update that file and describe checks actually run. Enable the commit template
with `git config commit.template .gitmessage`.

Space a a chooses an assistant, Space a w creates a worktree, Space g v opens
diff review, Space S s saves an editor layout, and Space S r restores one.
tmux's prefix is Ctrl+s. Layout restoration does not restart coding agents.

The NvChad starter's original public-domain license is retained.
