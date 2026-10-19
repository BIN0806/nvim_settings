# Billy's Neovim settings — C++ profile

The repository root is an installable NvChad configuration, saved from the
working C++ milestone on October 18, 2026. It contains language navigation,
completion/snippets, formatting, fuzzy search, Git signs and CodeLLDB debugging.

## Use this profile separately

Requires Neovim 0.12 (tested with 0.12.6), Git, a compiler and normal NvChad
prerequisites. MesloLGS or another Nerd Font supplies the icons.

```sh
git clone --branch codex/profile-cpp --single-branch https://github.com/BIN0806/nvim_settings.git ~/.config/nvim-billy-cpp
NVIM_APPNAME=nvim-billy-cpp nvim
```

In Neovim, restore the pinned plugins with `:Lazy restore`, install the declared
tools with `:MasonInstallAll`, and install/update the configured syntax parsers.
Neovim will bootstrap its plugin manager on first start. No coding agent is
started by opening the editor.

Use `:w` to save/format, Space f f to find files, g d for definitions, Space d b
for breakpoints and Space d r to start debugging. Build C++ with debug symbols
and a compile_commands.json database first.

## History

Read [CHANGELOG.md](CHANGELOG.md). Checkpoint: `setup-2026-10-18-cpp`.
The smaller profile is also preserved at `codex/profile-cpp`; main advances to
the full daily profile. Close Neovim before switching versions and restore the
selected revision's plugin lockfile afterward. NVIM_APPNAME keeps each profile's
plugin/data/state directories separate.

For future commits: update CHANGELOG.md and use the supplied commit template:
`git config commit.template .gitmessage`. Never force-push a profile or move a
published checkpoint tag.

Based on the NvChad starter; its original public-domain license is retained.
