# Billy's Neovim settings

An installable NvChad configuration combining the C++ IDE, multi-language tools,
editing/Git/session helpers, matching tmux settings and an optional project-scoped
Firstmate/Codex workflow. **main is the full daily profile.**

The root `init.lua`, `lua/` and `lazy-lock.json` are the Neovim configuration.
Everything else documents, verifies or supports it. Opening Neovim never starts
a coding agent or installs the separate Kun toolchain.

## Install without replacing your existing editor

Tested with Neovim **0.12.6**, NvChad **v2.5**, macOS on Apple Silicon and a Nerd
Font. Git, a C/C++ compiler and language SDKs are separate prerequisites. tmux and
the agentic tools are optional. The tmux clipboard bindings use macOS `pbcopy`.

```sh
git clone https://github.com/BIN0806/nvim_settings.git ~/.config/nvim-billy
NVIM_APPNAME=nvim-billy nvim
```

`NVIM_APPNAME` gives this checkout separate configuration, plugins, data, cache
and state. Keep using the same prefix when opening it. For a single terminal
session, `export NVIM_APPNAME=nvim-billy` also applies it to subsequent `nvim`
commands; this does not change your shell startup files.

On first start, Lazy bootstraps the declared plugins. Then use `:Lazy restore`
to match the committed lockfile, `:MasonInstallAll` for language/debug tools,
and `:TSUpdate` / `:TSInstall` for the configured Treesitter parsers. Normal
plugin/tool installation needs network access. Project dependencies remain
project-specific. See the handbook for language coverage and C++ debug builds.

Already using a working `~/.config/nvim`? Leave it in place while trying this
separate profile. Once you decide to use this as your default, close Neovim,
back up that directory and deliberately replace it with a clone of this repo.
Do not copy a second `.git` directory into the existing NvChad starter checkout.

## Profiles and exact restore points

| Selection | What it contains |
| --- | --- |
| `main` | Full daily profile and current maintained documentation. |
| `codex/profile-cpp` | Smaller tested C++ profile: NvChad, clangd, formatting and CodeLLDB; no extra agentic layer. |
| `setup-2026-10-18-cpp` | Immutable C++ foundation checkpoint. |
| `setup-2026-10-18-merged` | Combined editor/tmux checkpoint before Kun integration. |
| `setup-2026-10-19-cursor` | Full profile with terminal cursor animation and compatible Magicalbat additions. |
| `setup-2026-10-18-full` | Full profile including optional Kun/Codex launcher sources and instructions. |

The initial commits package real saved milestones from the original setup.
Every milestone has a [CHANGELOG entry](CHANGELOG.md) and a descriptive commit
body explaining changes, usage, verification and restoration. The tags pin exact
snapshots; profile branches can receive later compatible fixes.

Try the smaller profile independently:

```sh
git clone --branch codex/profile-cpp --single-branch https://github.com/BIN0806/nvim_settings.git ~/.config/nvim-billy-cpp
NVIM_APPNAME=nvim-billy-cpp nvim
```

Read [PROFILES.md](PROFILES.md) for switching revisions, restoring old snapshots,
creating another profile and making future logged commits.

## Everyday actions

Press Esc first. Space shortcuts are typed in sequence.

| Keys | Action |
| --- | --- |
| Ctrl+n | Toggle the file explorer. |
| Space f f / Space f w | Find files / search project text. |
| g d / g r / K | Definition / references / documentation. |
| Space c a / Space r a | Code action / rename. |
| :w / Space f m | Save and format / format now. |
| Space d b / Space d r | Toggle breakpoint / start or continue C++ debugging. |
| Space g v / Space g g | Diff review / LazyGit. |
| Space S s / Space S r | Save / restore an editor layout. |
| Space a a | Open a manually chosen installed coding assistant. |
| Space a w / Space a l | Create / list independent Git worktrees. |
| Space a k | Open the project's Kun/Codex workflow, if separately installed. |
| Ctrl+h/j/k/l | Navigate editor windows and tmux panes. |

Your tmux prefix is **Ctrl+s**. Its optional `tmux.conf` is tracked separately;
back up your current file before installing it. Install TPM and the listed tmux
plugins through their normal setup, then reload the config. It saves layouts
periodically but requires manual restoration and never replays agent processes.

## Optional Codex / Kun workflow

The repository includes the reviewed launcher, permission adapters and installer.
This is a separate toolchain, not a mandatory editor plugin. It needs Python
3.11+, Node/npm, tmux, Git, GitHub CLI and an authenticated Codex CLI. The current
installer supports macOS/Linux release platforms; this snapshot was tested on
Apple Silicon macOS. Your assistant model/account settings stay with its CLI.

From the clone, if you choose to install it:

```sh
python3 agentic/install.py
~/.local/bin/kun doctor
```

Keep `~/.local/bin` on PATH. From an application project with a Git commit:

```sh
cd /path/to/your/project
kun
```

It sets up/reopens a private Firstmate home, defaults to Codex for the primary
and workers, and uses Treehouse for isolated worktrees. GitHub projects default
to No Mistakes PR delivery; others use local branches. Merge approval is required.
Starting `kun` starts a real assistant conversation and can use account quota.
Use `kun setup` to configure a project without a model conversation.

[The complete command guide](agentic/README.md) explains setup side effects,
permissions, candidate checks, local/PR delivery, stopping work and maintenance.
Machine paths, logins, task state, project checkouts and installed binaries are
not versioned. [toolchain-lock.json](agentic/toolchain-lock.json) records the
reviewed versions and release checksums without local installation paths.

## Maintain a log in every settings commit

Inside this clone, enable the supplied local checks and commit template:

```sh
git config core.hooksPath .githooks
git config commit.template .gitmessage
```

The pre-commit hook requires a staged CHANGELOG.md update whenever Neovim,
tmux, profile metadata, plugin locks or agentic settings change. It runs no
model request and makes no network call. It is opt-in per clone; Git does not
activate repository hooks automatically.

Before a settings commit, document what changed, why, shortcuts/usage, checks
actually run and restore notes. Then:

```sh
python3 scripts/check.py
git diff
git add lua/mappings.lua CHANGELOG.md   # choose the actual intended files
git diff --cached
git commit                            # opens the supplied template
git push origin HEAD
```

Use a `codex/<purpose>` branch for experimental changes. Add an annotated tag
when a working milestone is worth restoring. Avoid force pushes and keep
published checkpoint tags immutable. See PROFILES.md for examples.

## Maintenance and recovery

The lockfile pins editor plugin commits. `:Lazy update` changes that lockfile;
review and commit it with the related settings changes. `:Lazy restore` restores
the selected revision's locked plugin versions. Mason packages, language SDKs,
tmux plugins, account settings and private Kun state have separate lifecycles;
switching a Git tag does not roll those back automatically.

Close Neovim before switching a checkout's branch/tag. Keep local edits by
committing them on a work branch or deliberately stashing them first. No reset,
force checkout, clean or automatic deletion is needed for ordinary version hops.

Recorded runtime evidence is in [verification/summary.md](verification/summary.md).
The repository packaging checks run without bootstrapping plugins or invoking a
model. Real first-use agent/PR behavior still needs a bounded task in your project.

## Guides and credits

- [Complete handbook: each video, integrated instructions and final stack](NVIM-HANDBOOK.md)
- [Beginner guide](START-HERE.md)
- [Combined editing/tmux/agent workflow](MERGED-WORKFLOW.md)
- [Video compatibility decisions and transcript limits](MERGE-NOTES.md)
- [Original C++ video comparison](video-checklist.md)
- [Profiles, checkpoints and future changes](PROFILES.md)
- [Kun command guide](agentic/README.md)

The NvChad starter's original public-domain license is retained. Plugin and
external-tool licenses remain with their projects; installed dependencies are
not vendored here. Tutorial authors and source repositories are linked in the
handbook. Captions, personal transcripts and local backups are not uploaded.

## Magicalbat cursor and settings merge

October 19: the full profile now has a terminal cursor trail (Space u c), compatible
resize/selection/search/LSP shortcuts and MATLAB syntax. Restart Neovim to load it.
[The merge guide](MAGICALBAT-MERGE.md) explains additions, source limitations and
conflicts. The previous full setup remains at setup-2026-10-18-full.
