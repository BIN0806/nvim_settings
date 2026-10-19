# How the six tutorials became one setup

> Repository edition: examples assume a clone at `~/.config/nvim-billy`.
> Run it with `NVIM_APPNAME=nvim-billy nvim`; see README.md and PROFILES.md.

The complete consolidated reference is [NVIM-HANDBOOK.md](NVIM-HANDBOOK.md), with
per-video feature tables, integrated usage instructions and the final stack at
the end.

This is a capabilities merge, built on your working NvChad installation. The
active files are in `~/.config/nvim-billy`; tmux uses
`~/.tmux.conf`. Restart Neovim to load the changes. Read
[START-HERE.md](START-HERE.md) for the basics, then
[MERGED-WORKFLOW.md](MERGED-WORKFLOW.md) for the new tools and practice exercises.

## What was reviewed, and transcript limitations

The first Dreams of Code tutorial's setup transcript was extracted from YouTube's
browser panel during the original installation and compared with its repository.
For the five additional videos, I inspected available descriptions, chapters,
on-screen demonstrations, linked configurations, and current tool documentation.
This was not an uninterrupted viewing of every minute of all five videos.

YouTube's caption requests were rate limited and the browser transcript panels
for the Rad Lectures, Mental Outlaw, Andrew Courter, and Kun Chen videos remained
on a loading spinner after retries. A public archive of Kun Chen's auto-generated
English transcript was successfully retrieved and reviewed. Its spelling of tool
names was checked against his repositories. I could not scrape full transcripts
for the other three narrated videos. The Average Neovim Enjoyer video is a silent
on-screen tutorial with music and no transcript option; its setup steps were read
from video frames. These limitations are recorded explicitly rather than claiming
that every transcript was successfully scraped.

Archived caption reference: [Kun Chen transcript mirror](https://github.com/chung-ta/youtube-transcripts/blob/main/l8-principals-agentic-engineering-workflow.md).
It is a third-party copy, not an official publication. Full scraped material is
kept as ignored research data; this guide paraphrases the relevant setup decisions.

## Tutorial-by-tutorial outcome

| Tutorial | Useful parts | Your result |
| --- | --- | --- |
| [Dreams of Code: C++](https://www.youtube.com/watch?v=lsFoZIg-oDs) | NvChad, clangd, clang-format, Mason, CodeLLDB and DAP panels | Kept the working C/C++ foundation; modern APIs and Conform replace obsolete setup code. |
| [The Ultimate Neovim setup for C and C++](https://www.youtube.com/watch?v=w0WzxUPtKf0) | clang-format through none-ls, clangd, C/C++ parsers | Same capabilities already present. Existing Conform owns formatting; no second formatting bridge. |
| [Minimal & Powerful: The Perfect NeoVim Setup for 2026](https://www.youtube.com/watch?v=lljs_7xB7Ps) | mini.nvim editing/session tools, navigation conveniences, current LSP and treesitter, language tooling, terminals | Added selected mini modules, sessions, centered navigation, yank feedback, position restoration, folding, Markdown conveniences and more languages. Existing NvChad tools cover the overlapping interface. |
| [NVChad — Turn Neovim Into An Awesome IDE](https://www.youtube.com/watch?v=yW3ovyQCwpw&t=88s) | Explorer, fuzzy search, themes, buffers, splits and language tools | Already provided by current NvChad. Added beginner instructions connecting each feature to a real workflow. |
| [Configure Tmux and Vim As Your Dev Environment](https://www.youtube.com/watch?v=xUnXcVxcJho) | Keyboard navigation, relative lines, tmux panes, prefix, mouse, copy workflow | Preserved your Ctrl+s prefix and navigation; improved splits, copy mode, colors and persistence. Native Neovim tools substitute for his Vim-era plugins. |
| [L8 Principal's Agentic Engineering Workflow](https://www.youtube.com/watch?v=iQyg-KypKAA) | Terminal assistants, concise project context, planning, validation, isolated worktrees | Added manual Codex/Claude/OpenCode launchers, a task-note template, worktree creation/listing, Git review and a documented plan → implement → validate → review routine. Specialized orchestration remains optional; see below. |

## Why the independent foundations were not stacked

Most of these tools can technically coexist. The problem is overlapping ownership:
multiple tools can load the same plugin, claim the same shortcut, attach duplicate
language clients, or format the same file twice. A dependable setup assigns each
job to one tool. These are deliberate substitutions, not missing installations.

| Video tool or choice | Selected tool | Reason |
| --- | --- | --- |
| Vim-Plug / vim.pack | lazy.nvim | NvChad already uses Lazy; keeping one manager also preserves one lockfile. |
| CoC | Native LSP + nvim-cmp + LuaSnip | Already supplies completion, definitions, references, rename and actions. |
| blink.cmp | nvim-cmp | Keep NvChad's integrated completion stack; running both would duplicate menus and mappings. |
| null-ls / none-ls / efm formatting | Conform + formatter executables | One formatter path, project configuration support, format on save. Ruff and language servers handle the selected diagnostics. |
| NERDTree | nvim-tree | One file explorer. |
| fzf.vim / fzf-lua | Telescope | Same file/text/buffer/history search workflows with existing keys. LazyGit handles broader Git operations. |
| ALE | clangd, Pyright, Ruff, TypeScript, Bash/ShellCheck | Diagnostics come from language-specific tools without another overlapping client. This is not a claim to support every ALE linter. |
| Airline / custom statusline / lualine | NvChad statusline | One statusline and one theme owner. |
| gitgutter / mini.diff | Gitsigns + Diffview | Changed-line indicators and hunk operations plus full diff review. |
| vim-surround | mini.surround | Surround editing with a single mapping set. |
| mini.pairs / mini.comment / mini.icons / mini.notify | Existing pairs, comments, icons and notifications | Avoid replacing working NvChad defaults for duplicate features. |
| Nord / Melange / Rose Pine / multiple tmux themes | Catppuccin in Neovim, matching tmux palette | Visual coherence; one active theme at a time. Use Space t h to explore editor themes later. |
| WezTerm | Your existing terminal + tmux | The editor/pane/agent workflow works in your current terminal. WezTerm remains an optional terminal-emulator alternative. |

Radley's [current source](https://github.com/radleylewis/nvim-lite) has evolved
since his recording. It includes later Rust/Obsidian additions and notes paths
that error on macOS. Those personal paths were not copied. Courter's
[current dotfiles](https://github.com/exosyphon/dotfiles) have also evolved: the
2022 video shows the Ctrl+s/Nord-era setup much like your original configuration,
while the current repository includes later plugins and different choices.
Persistence improvements here borrow from that newer source, not a claim that
every feature appears in his 2022 recording.

## Language coverage

| Language | Installed support | What still belongs to each project |
| --- | --- | --- |
| C/C++ | clangd, clang-format, syntax parsers, CodeLLDB/DAP | Compiler, CMake/build rules, compile_commands.json, application tests |
| Lua | lua-language-server, StyLua, syntax parser | Your Lua application/runtime if needed |
| Python | Pyright type information, Ruff lint/fixes/formatting, syntax parser | Python environment, dependencies and a project test command |
| JavaScript/TypeScript/JSX/TSX | TypeScript language server, Prettier, syntax parsers | package.json, dependencies, tsconfig and test/build scripts |
| Bash/sh | Bash language server, ShellCheck, shfmt, parser | Shell dialect and script-specific commands; this is not zsh LSP support |
| JSON/JSONC | JSON language server, Prettier, parser | Relevant schemas if the project needs them |
| HTML/CSS/YAML/Markdown | Syntax parsers and Prettier formatting | Framework-specific language servers when needed |
| TOML/CMake | Syntax parsers | Additional language servers when needed |
| Go/Rust/C#/Godot/Obsidian | Not automatically added | Their SDKs, project needs or vault paths should drive the configuration. |

The debugger preset remains C/C++. Adding Python or TypeScript language servers
does not install Python/Node debug configurations. App dependencies also remain
separate from editor tooling. Mason does not create your project's virtualenv or
run npm install for your application.

## Agent-workflow tools: compatible, optional, and substituted

The agent video is a wider engineering workflow, not a single Neovim plugin pack.
The core orchestration tools are now installed privately. `kun` prepares a
separate home for each Git project on demand, with Codex as the default. Project
commands must still be verified against the real repository. See
[the complete command guide](agentic/README.md).

| Tool/layer | Status and reason | Available workflow |
| --- | --- | --- |
| Codex / Claude Code / OpenCode | Existing CLIs integrated into Neovim terminals. Claude updated from broken 2.0.9 to working 2.1.303. | Space a a selects an installed assistant. Account/provider configuration stays with that CLI. |
| Pi | Optional alternative harness; not installed | Launcher supports it if you later install its CLI. Three usable harnesses are already present. |
| Global and project memory | Existing files preserved; starter template supplied | Put real project facts and verified commands in the project's own context file. No global preferences copied from a stranger's setup. |
| Skills | Existing packs preserved; No Mistakes bundled skill installed/refreshed | No bulk third-party instruction-pack installation or global preference replacement. |
| [Treehouse](https://github.com/kunchenguid/treehouse) | v3.1.4 installed privately, real worktree lease verified | Firstmate workers can use the reusable pool. Space a w / Space a l remain available for manual worktrees. |
| [No Mistakes](https://github.com/kunchenguid/no-mistakes) | v1.84.0 installed privately; gate/daemon initialization verified | kun configures a per-project local gate for GitHub PR delivery. Real check commands need verification; setup itself does not publish code. |
| [gnhf](https://github.com/kunchenguid/gnhf) | Not enabled; inspected source defaults use permission-bypass flags, and unattended loops spend account quota | Start one bounded task manually, require a clear stopping condition and inspect its results. This setup does not run overnight loops. |
| [Firstmate](https://github.com/kunchenguid/firstmate) | Pinned private installation with recorded integration overlays | kun / Space a k opens the project with Codex primary/workers, tmux backend, private state and required merge approval. |
| Lavish/AXI | Lavish, Tasks, GitHub, Chrome DevTools and quota AXI installed privately | Firstmate can use structured planning/task/tool interfaces. Browser use still requires a suitable browser session; global hook installers were not run. |
| OpenSuperWhisper | Optional voice-input app, not installed or granted OS permissions | Type prompts, or use macOS Dictation if already enabled. Dedicated local transcription can be added separately. |

No model requests, user-project pushes, PRs or merges were made during setup.
Disposable integration repositories exercised local gate remotes and a temporary
daemon. On a real project, `kun` in PR mode adds a local `no-mistakes` remote and
can register its daemon; starting the assistant then uses the user's account.
Bundled No Mistakes user-level skills are installed by its native initializer.
Project preferences, instructions and unrelated changes are preserved.

## Important shortcut choices

Space is your leader. Existing useful keys were preserved. Radley's horizontal
split shortcut would collide with your C++ source/header switch, so horizontal
split is **Space s s**, vertical split is **Space s v**, and source/header remains
**Space s h**. Rename remains **Space r a**; **Space r n** still toggles relative
numbers. Git hunk actions use **Space g ...**, because **Space h** already opens
a terminal. Moving lines uses **Space m h/j/k/l**, preserving Alt+h/v/i terminal
shortcuts. Sessions use uppercase **Space S ...**, avoiding NvChad's buffer keys.

## Checkpoints and verification

The saved C++ profile is at `setup-2026-10-18-cpp` / `codex/profile-cpp`;
the combined pre-Kun checkpoint is `setup-2026-10-18-merged`; the full profile
is `setup-2026-10-18-full`. See [PROFILES.md](PROFILES.md) for exact restore
instructions. Local machine backups and research downloads are not uploaded.

Tests and evidence are described in [verification/summary.md](verification/summary.md).
Original runtime checks used disposable fixtures and did not push a user project
or use model quota. Repository packaging preserves the selected configuration
files and normalizes documentation/test paths for use from a clone.

## Magicalbat/Configs integration — October 19, 2026

The published source has no cursor-animation plugin. The full profile adds a
terminal cursor-trail substitute and compatible mappings, while preserving the
working theme, pair engine, LSP/Treesitter APIs and tmux navigation. MATLAB syntax
is additive. [The detailed guide](MAGICALBAT-MERGE.md) records all conflicts,
existing equivalents, usage and pinned source revisions.
