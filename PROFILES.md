# Profiles, history and restoration

Use **main** for the full daily setup. Use **codex/profile-cpp** for the smaller
working C++ profile. Each branch contains an installable config at its root.
The tags listed in README are immutable checkpoints, while profile branches can
advance with intentional updates. `profile.json` identifies the current profile.

## Inspect history

```sh
git log --graph --decorate --oneline --all
git log --format=fuller -- CHANGELOG.md
git show setup-2026-10-18-full
git diff setup-2026-10-18-cpp..setup-2026-10-18-full -- lua lazy-lock.json
```

The commit bodies and CHANGELOG.md describe features, key changes, validation and
restore points. Saved setup milestones were packaged in order on October 18,
2026; their commit times are packaging times, not the original edit times.

## Try two profiles without disturbing either

```sh
git clone https://github.com/BIN0806/nvim_settings.git ~/.config/nvim-billy
git clone --branch codex/profile-cpp --single-branch https://github.com/BIN0806/nvim_settings.git ~/.config/nvim-billy-cpp
NVIM_APPNAME=nvim-billy nvim
NVIM_APPNAME=nvim-billy-cpp nvim
```

Run one launch command at a time in the desired terminal. NVIM_APPNAME keeps
Neovim's configuration, plugins, cache, sessions and other data separate. Global
tools such as tmux, compilers and Kun remain shared unless configured separately.
Use unused clone destinations; do not delete a working setup to make room.

## Hop to an exact checkpoint in an existing clone

Close Neovim, then inspect the checkout first:

```sh
cd ~/.config/nvim-billy
git status
git fetch origin --tags
git switch --detach setup-2026-10-18-merged
NVIM_APPNAME=nvim-billy nvim
```

If `git status` shows changes, commit them on a work branch or intentionally
stash them before switching. Git will refuse an overwrite rather than silently
discarding work. A detached tag is good for trying an old snapshot. If you want
to edit it, create a work branch first with `git switch -c codex/try-old-layout`.

After opening that revision, run `:Lazy restore`. Tool versions outside Lazy
are not reverted by switching the config. Keep separate NVIM_APPNAME clones when
you frequently compare very different configurations.

Return to the latest full branch:

```sh
git switch main
git pull --ff-only origin main
NVIM_APPNAME=nvim-billy nvim
```

Then run `:Lazy restore` for main's plugin lockfile. Fetch/pull commands need
network access. No force checkout, hard reset or `git clean` is required.

## Maintain a profile

Create a work branch from the profile you actually intend to change:

```sh
git switch main
git switch -c codex/improve-search
git config core.hooksPath .githooks
git config commit.template .gitmessage
```

Edit the config in this clone. Add a dated CHANGELOG.md entry with:

1. What changed and why.
2. Affected profile and any key bindings or new usage.
3. Commands/checks actually run and observed results.
4. Compatibility or migration notes, and the previous checkpoint to restore.

Run `python3 scripts/check.py`, review the diff and commit only the intended
files. The hook requires a staged change-log update for settings changes. It
does not judge the prose or run a model. Hooks must be enabled per clone and
are only present on revisions that include them; older checkpoints still use
the documented manual convention.

Push the work branch with `git push -u origin HEAD`, then review/merge it into
the intended profile through normal Git/GitHub flow. Keep each profile's change
log accurate. A shared fix can be cherry-picked to the other profile after
checking that its dependencies and key bindings still fit. Do not automatically
merge full-profile features into the intentionally smaller C++ profile.

## Create another profile only when it has a real purpose

For example, a distinctly minimal writing/review setup could start from the
closest existing profile:

```sh
git switch main
git switch -c codex/profile-writing
```

Remove/change the relevant features, update profile.json and CHANGELOG.md, check
it, commit, and push with `git push -u origin HEAD`. Use a separate clone and
NVIM_APPNAME such as `nvim-billy-writing` to try it. A different color choice
alone usually does not need a permanent branch; a checkpoint tag can be enough.

## Name a stable checkpoint

After checks pass and the intended changes are committed:

```sh
git tag -a setup-2026-10-19-full -m 'Full profile: describe the verified changes and usage'
git push origin setup-2026-10-19-full
```

That date/name is an example for a future milestone. Use its actual date and a
unique name. Never move a published checkpoint tag to a different commit.

## Scope of a restore

Git restores this repository's config, documentation, scripts and plugin lock.
It does not restore unsaved buffers, project files, credentials, model quotas,
Mason package versions, external compiler SDKs, tmux plugin revisions, private
Firstmate homes, daemon state or other machine files. Those were intentionally
not uploaded. The optional installer pins its reviewed toolchain; check the
appropriate release/compatibility notes before reinstalling an old tool version.
