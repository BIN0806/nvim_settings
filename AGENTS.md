# Working on these settings

The repository root is an installable NvChad configuration. Keep the current
profile in profile.json accurate. main is the full daily setup; codex/profile-cpp
preserves the smaller C++ setup. Use codex/ for new work branches.

For every settings commit, update CHANGELOG.md with the date, concrete changes,
reason, affected profile, shortcuts/usage, checks actually run, and restore or
compatibility notes. Use the .gitmessage structure for substantial commits.
Never claim a check passed unless it ran or clearly label prior recorded results.

Preserve lazy-lock.json for reproducible plugin revisions. Do not mix competing
plugin managers, completion engines or duplicate key bindings. Keep future
changes on their intended profile; cherry-pick shared fixes where appropriate.

Keep secrets, machine installation records, private task state, source-project
checkouts, binaries, generated caches and local backups out of this repository.
The agentic installer is optional; editing Neovim must not start a model request.
No force pushes or moving published checkpoint tags. Preserve remote history.
