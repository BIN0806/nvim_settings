# Your combined Neovim workflow

> Repository edition: examples assume a clone at `~/.config/nvim-billy`.
> Run it with `NVIM_APPNAME=nvim-billy nvim`; see README.md and PROFILES.md.

You do not need to have watched any of the videos. This guide explains the new
features as actions you can perform, with practice steps and a recap after each
part. [START-HERE.md](START-HERE.md) teaches modes, basic editing, completion,
building and C++ debugging. [MERGE-NOTES.md](MERGE-NOTES.md) explains the source
videos, transcript limitations, substitutions and optional tools.

**Kun automation:** the core agent tools are installed. Run `kun` inside any Git
project with a first commit, or press Space a k in Neovim. Codex is the default.
Read [the command guide](agentic/README.md) for first use, delivery modes, sessions
and approvals. The manual workflows below remain available independently.

## 1. Start in the right directory

Close and reopen Neovim to load the combined configuration. Open a terminal in
your project's main folder before running `nvim`. File search, build commands,
language servers and assistants all work best when they agree on the project.

For the supplied practice project:

```sh
cd ~/.config/nvim-billy/example
tmux new -A -s nvim-lab
nvim src/main.cpp
```

The first command chooses the folder. The second creates a tmux session named
`nvim-lab`, or reconnects to it if it already exists. The third opens the source.
You can also run Neovim directly without tmux.

Neovim's **leader is Space**. `Space g v` means three keys in sequence, starting
in Normal mode. `Ctrl+s` means hold Control and press s. Capital letters matter:
`Space S s` contains uppercase S. Start with Esc if you are unsure of the mode.

**You can now:** open the example in a persistent workspace and distinguish
Neovim's Space shortcuts from tmux's Ctrl+s prefix.

## 2. Find things and understand unfamiliar code

| Action | Keys |
| --- | --- |
| Find a file by part of its name | Space f f |
| Search text throughout the project | Space f w |
| Search within the current file | Space f z |
| Switch among open files | Space f b, or Tab / Shift+Tab |
| Browse the file tree | Ctrl+n |
| Focus the file tree | Space e |
| Read documentation for a symbol | K |
| Jump to a definition | g d |
| Find references | g r |
| Return from a jump | Ctrl+o |
| Rename a symbol through the language server | Space r a |
| Show available fixes/actions | Space c a |
| List diagnostics for this file | Space d s |
| Switch C++ source/header | Space s h |

Try Space f f, type `main`, and press Enter on `main.cpp`. Put the cursor over
`std::accumulate` and press K. Use g d to inspect its definition and Ctrl+o to
return. This works through the language server, so allow a moment for the server
to start when you first open a project.

Relative line numbers help you count movements. If your target is six lines
above, `6k` reaches it. `w` moves to the next word, `b` to the previous word,
`gg` to the beginning of a file, and `G` to the end. Search with `/word`, Enter;
`n` goes to the next match and `N` to the previous one. Search jumps and Ctrl+d/u
half-page scrolling now center the view. Esc clears search highlighting.

**You can now:** locate a file, find where something is used, read its meaning,
and return to your starting point without remembering every path.

## 3. Edit words and blocks with fewer keystrokes

Keep the basic verbs in mind: `d` deletes, `c` changes and starts typing, `y`
copies. `iw` means “inside this word.” Thus `ciw` changes a word and `diw` deletes
it. A number repeats a motion: `3dd` deletes three lines. `u` undoes the last edit.
Copying now briefly highlights the copied text so you can see what you selected.

Selected mini.nvim modules add surrounding edits, richer text objects and block
movement. These practice examples use a scratch file, so you can experiment freely:
`:enew`, Enter, then `i`, type `alpha`, then Esc.

| Goal | Keys | Example result |
| --- | --- | --- |
| Put double quotes around the word | `s a i w "` | alpha → "alpha" |
| Remove nearby double quotes | `s d "` | "alpha" → alpha |
| Replace double quotes with single quotes | `s r " '` | "alpha" → 'alpha' |
| Change text inside nearby quotes | `c i q`, type replacement, Esc | Keeps the surrounding quotes |
| Change text inside brackets/parentheses | `c i b`, type replacement, Esc | Keeps the surrounding brackets |
| Move the current line down/up | Space m j / Space m k | Reorders lines |
| Shift the current line left/right | Space m h / Space m l | Adjusts indentation |
| Move a block | V, extend selection with j/k, then Space m j/k | Moves the selected lines together |
| Comment the line or selection | Space / | Toggles comments for the file type |

Surround uses `s` as a prefix; use `cl` if you want the old one-character
substitute action. Alt+h/v/i retain their existing terminal shortcuts, which is
why block movement uses Space m instead of the video's Alt keys.

Try this sequence: add quotes to alpha, replace the quotes, undo, remove the
quotes, add two lines, and move one line down. You are learning reusable actions,
not memorizing a separate command for every programming language.

**You can now:** change the contents of words or quoted expressions, add/remove
surroundings, reorder code blocks, and undo mistakes.

## 4. Formatting, errors and language support

Saving with `:w` runs the configured formatter for supported file types. Space f m
formats immediately. Space u f turns automatic formatting off/on for the current
buffer. Project style files such as `.clang-format`, `.prettierrc` and
`pyproject.toml` remain the place to define the project's style.

| Files | Understanding and diagnostics | Formatting |
| --- | --- | --- |
| C/C++ | clangd, including clang-tidy | clang-format |
| Lua | Lua language server | StyLua |
| Python | Pyright type information + Ruff lint/fixes | Ruff |
| JS/TS/JSX/TSX | TypeScript language server | Prettier |
| Bash/sh | Bash language server + ShellCheck | shfmt |
| JSON/JSONC | JSON language server | Prettier |
| HTML/CSS/YAML/Markdown | Syntax highlighting; framework/server additions are separate | Prettier |

A diagnostic is a tool's warning or error. It is feedback before a build or test,
not proof that your application is correct. K, g d, g r, Space r a and Space c a
work when the relevant language server supports the operation. Ruff's hover is
disabled so Pyright supplies the Python hover text consistently.

For Python, create/select your project's environment and install its dependencies
as usual. For TypeScript, install the application's dependencies and provide its
tsconfig. Editor tools do not replace those project steps. Some projects will need
framework-specific tools; Go/Rust/C#/Godot SDKs and Obsidian vault configuration
were not guessed from somebody else's personal setup.

Markdown/text files use readable wrapping and spell checking. If a code-heavy
document becomes distracting, `:setlocal nospell` disables spelling in that buffer.
Spelling suggestions are available with `z=` over a flagged word.

Inspect `:ConformInfo` for formatter selection and `:checkhealth vim.lsp` for
language servers. C/C++ has the supplied debugger preset; the additional language
servers do not automatically add debug adapters for those languages.

**You can now:** get early feedback and consistent formatting across several
languages, while keeping project dependencies and editor tooling separate.

## 5. Keep the C++ build/debug loop clear

From the example's terminal:

```sh
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build build
./build/app
```

The configure step creates build rules and a compilation database. The build
step compiles the source; running prints `Total: 100`. Repeat the build after
editing C++ before running or debugging the executable again.

| Debugging action | Keys |
| --- | --- |
| Add/remove breakpoint at the cursor | Space d b |
| Start/continue | Space d r, or F5 |
| Step over a line | Space d o, or F10 |
| Step into a function | Space d i, or F11 |
| Step out of the current function | Space d O, or F12 |
| Evaluate a variable/expression | Space d e |
| Toggle debugger panels | Space d u |
| Stop | Space d q |

In `main.cpp`, put a breakpoint on the `std::cout` line and start debugging.
Choose LLDB: Launch if prompted and give the path to `example/build/app`. At the
breakpoint, the value of `total` should be 100. Step over, continue, or stop.

**You can now:** use diagnostics to spot a problem, then pause the running program
to inspect the actual values that caused it. Saving, building and debugging are
three distinct actions.

## 6. Review and organize Git changes

A **hunk** is a nearby group of changed lines. The gutter marks changed regions;
the following keys turn those marks into a review workflow.

| Action | Keys |
| --- | --- |
| Next/previous changed hunk | ] h / [ h |
| Preview the hunk | Space g p |
| Stage a hunk; toggle it back when on its staged signs | Space g s |
| Unstage the current file, preserving its contents | Space g u |
| Show who last changed the current line | Space g b |
| Open the full terminal Git interface | Space g g |
| Open side-by-side diff review | Space g v |
| Close diff review | Space g q |
| Show current file history | Space g H |

Stage means “include this change in the next commit.” It does not upload anything.
Unstage removes it from that selection and leaves your edited file intact. Use
Space g g for LazyGit, which offers status, staging, commits, branches and history.
Its `?` help lists the current screen's commands; `q` exits its interface.

Space g v opens Diffview. Choose a file in its panel to compare earlier and current
contents. Use `:DiffviewOpen --cached` when you specifically want the staged diff.
Space g q returns to normal editing. Git history/review features work best in a
repository with at least one commit; the supplied C++ example is inside your HATE
workspace, so its Git view follows that repository's actual history.

Review the same way whether you wrote the code or an assistant did. Check the
intended behavior, changed files and relevant tests. A tidy diff is useful, but
running the program is what tests its behavior.

**You can now:** inspect exactly what changed, choose what enters a commit, and
review an assistant's work before accepting it.

## 7. Arrange the editor and save layouts

| Action | Keys |
| --- | --- |
| Split into left/right editor windows | Space s v |
| Split into top/bottom editor windows | Space s s |
| Move between editor windows and tmux panes | Ctrl+h/j/k/l in Normal mode |
| Close the current editor window | :q |
| Save a named editor layout | Space S s |
| Choose a saved layout to restore | Space S r |
| Delete a saved layout | Space S d |
| Toggle a focused, centered editing view | Space z |
| Close/open a fold | z c / z o |
| Toggle fold under cursor | z a |
| Open all folds | z R |

Folds collapse code sections recognized by the syntax parser. Files start with
folds open, so the setup does not hide unfamiliar code on first use. Last cursor
positions are restored when possible.

An editor session saves open files, splits and layout. Save your files with `:wa`
before saving or restoring a layout; a session is not a backup of unsaved edits.
Use a simple name such as `cpp-lab` or `project-review` (letters, numbers, hyphens,
underscores or dots). Sessions are saved only on request. Restoring a session does
not relaunch terminal programs or coding agents.

Practice opening two files in a split, saving a session, closing one window, then
restoring the session. Space z is useful when you want to read or write one file
without rearranging the whole workspace permanently.

**You can now:** keep related code visible, hide details temporarily, and return
to a named editor layout later.

## 8. Use tmux for persistent terminals and multiple tasks

tmux's prefix is **Ctrl+s**. Press it, release it, then press the next key. This
is independent of Space shortcuts inside Neovim. Use `:w` to save in Neovim
because tmux consumes Ctrl+s as its prefix.

| After pressing Ctrl+s | What happens |
| --- | --- |
| `\|` | Split left/right, starting in the current pane's folder |
| `-` | Split top/bottom, in the current folder |
| `c` | New tmux window, in the current folder |
| `n` / `p` | Next/previous tmux window |
| `1`, `2`, ... | Select a numbered window |
| `,` | Rename the current window |
| `h/j/k/l` | Move between panes |
| `H/J/K/L` | Resize panes |
| `z` | Zoom/unzoom one pane |
| `d` | Detach; keep the session running |
| `s` | Choose a session |
| `Esc` | Enter scroll/copy mode |
| `P` | Paste tmux's copied buffer |
| `r` | Reload ~/.tmux.conf |
| `Ctrl+s` | Save layout with tmux-resurrect |
| `Ctrl+r` | Restore the saved tmux layout |
| `b` | Send a literal Ctrl+s to the program |

For copying output: prefix, Esc; move with Vim keys, press `v` to start selecting,
move to the end, then `y` to copy to the macOS clipboard. Press Esc/q to leave copy
mode if needed. Mouse selection and scrolling are also enabled.

Detach with prefix d. Later, run `tmux attach -t nvim-lab` to return. Detaching
keeps processes alive while this computer and tmux server are running. Rebooting
ends those processes. Resurrect/Continuum save layouts and directories; they do
not freeze and resurrect the memory of a compiler, debugger or assistant. Layouts
are saved about every 15 minutes when Continuum is active; restoration is manual,
and this configuration restores shells rather than automatically restarting jobs.

A Neovim session remembers editor windows/files. A tmux session contains terminal
panes and running processes. Their saved layouts solve different parts of the
same workspace problem. Save important editor layouts explicitly, and keep your
actual source files under version control.

**You can now:** detach and reconnect, keep editor/assistant/build terminals
together, copy terminal output, and recover terminal layouts after a restart.

## 9. Work with an assistant beside your code

| Action | Keys |
| --- | --- |
| Open the Kun project workflow (Codex) | Space a k |
| Choose an installed coding assistant | Space a a |
| Open Codex | Space a c |
| Open Claude Code | Space a C |
| Open OpenCode | Space a o |
| Open/create the project's task note | Space a t |
| Create an isolated worktree for another task | Space a w |
| List Git worktrees | Space a l |

Launchers open a vertical terminal in the detected project root. They use the
installed CLI's account/provider configuration. Codex is launched with the
workspace-write sandbox. Claude and OpenCode keep their normal configurations;
no permission-bypass flags are added. If a CLI asks you to sign in or select a
provider, complete that in its own interface. No paid model requests were made
to test these launchers.

Inside a terminal, keys go to that program. Press **Ctrl+x** to return to Neovim's
Terminal-Normal mode, then Ctrl+h/j/k/l to move away. Press `i` to resume typing in
the terminal. Closing an agent terminal can end its job; use a separate tmux pane
when you want its lifetime to be independent of the editor. Exiting an assistant
normally returns you to a shell in that terminal.

Begin with a specific, observable request:

> Explain how this project is built and tested. Identify the files involved in
> calculating the total. Propose a small change that prints the average too.
> Show the approach and expected output before editing. After implementing it,
> build and run the program, compare output to the expectation, and summarize
> changed files and commands run. Leave the result for my review.

Space a t creates `.agent-notes/task.md` only when you request it. It contains
sections for outcome, context, constraints, plan, validation and handoff. Fill in
the real commands; the note is a coordination file, not an automatic test runner
or a memory file that every harness necessarily reads. Tell the assistant to read
it. It is a normal project file, so decide whether to commit it or ignore it.

When an assistant edits files on disk, Neovim checks saved buffers on focus,
buffer entry and idle events. Unmodified buffers can refresh automatically.
Unsaved buffer edits are kept, so save or deliberately resolve your version
before asking the assistant to edit the same file. If you need to inspect an
external update manually, `:checktime` checks for it.

**You can now:** ask for a focused change, keep its plan next to the code, watch
changes appear, run the program and review the diff.

## 10. A repeatable agent workflow

1. **Define the outcome.** Describe what the user should see, how to reproduce the
   problem, and what successful output/behavior looks like.
2. **Get a concrete plan.** Ask for affected files and tradeoffs. For a UI change,
   ask for a preview or mockup before implementation. A Markdown plan works for
   simple changes; Firstmate can also use the installed Lavish planning tool.
3. **Record real project context.** Keep build/test commands, architecture facts
   and non-obvious conventions in the project's context file. A starter is in
   `templates/PROJECT-CONTEXT.md`. Copy and adapt it deliberately; no global agent
   memory has been overwritten. Different harnesses have different instruction
   loading rules, so consult their documentation before assuming one file works
   for all of them.
4. **Implement one task.** Let the assistant work in its assigned checkout. Keep
   the task small enough to test and explain.
5. **Validate behavior.** Require exact checks and evidence. A passing type checker
   is different from a working user flow. Use the app, build output, screenshots
   or relevant integration tests as appropriate.
6. **Review the result.** Use Space g v and Space g g. Look for unrelated edits,
   missing error handling and changes to dependencies/configuration.
7. **Commit deliberately.** Commit a coherent change once you understand its
   behavior and checks. Publishing and merging are separate decisions.
8. **Write a handoff.** Record what changed, how it was tested and what remains.
   This helps your next assistant session resume without guessing.

You can perform this sequence manually, or use `kun` / Space a k to have
Firstmate coordinate Codex workers and the selected delivery mode. Start with
one scoped task. In PR mode, inspect the branch/PR that contains the worker's
changes; your original checkout does not display an unmerged worker diff.
No Mistakes supplies the gate, while gnhf overnight loops remain optional.
See [the kun guide](agentic/README.md) for the automated path and its controls.

**You can now:** evaluate an assistant's output by the intended behavior and
evidence, rather than treating “done” as the only acceptance criterion.

## 11. Run a second task without mixing files

A Git worktree is another checkout connected to the same repository, usually on
a different branch. It shares Git history while giving the task its own files.
It does not copy your current uncommitted edits. It requires a repository with
at least one commit.

Use Space a w in the first project. Enter a new branch name such as
`codex/fix-output`, then choose the suggested sibling `.worktrees` folder or a
different unused location. A terminal opens in the new checkout. Start `nvim .`
there, or create a separate tmux window, change to that checkout and start an
assistant. Install that checkout's project dependencies if needed.

Keep one writing task per checkout. Rename tmux windows after their task, such
as `output-fix` and `tests`, and keep a task note in each checkout. Space a l
lists locations; `git worktree list` does the same in a terminal.

After reviewing and committing a task, stop its running jobs before removing its
worktree. From a different checkout, `git worktree remove /path/to/worktree`
removes a clean worktree; do not add `--force` just to get past unsaved changes.
Removing a worktree does not merge its branch. Review/merge the branch through
your project's usual Git workflow.

Start with one assistant. Add a second only when the first task's outcome is
clear and its checks can run independently. More assistants help when tasks can
be separated; they also create more results that need your attention.

**You can now:** give independent tasks independent files, locate each checkout,
and finish a task without losing track of its branch or running process.

## 12. Keep the setup understandable

| Tool command | Purpose |
| --- | --- |
| :Lazy | Editor plugins and their versions |
| :Mason | Language executables and debugger packages |
| :TSUpdate | Update installed syntax parsers |
| :ConformInfo | Which formatter will run for this buffer |
| :checkhealth vim.lsp | Language-server health |
| :messages | Previous warnings/messages |
| Space c h | NvChad shortcut reference |
| Space, then pause | Discover available shortcuts |

Update intentionally and try your normal edit/build/debug workflow afterward.
The lockfile records editor plugin revisions; it does not pin every future
Mason package release. Keep project formatter settings in the project, and keep
your configuration under version control when you are ready to manage it that way.

The C++ milestone is preserved at `setup-2026-10-18-cpp` and the combined
pre-Kun milestone at `setup-2026-10-18-merged`. See [PROFILES.md](PROFILES.md)
for restoring them without deleting local work. The verification report records
what was actually checked. Local machine backups are not part of this repository.

For your first week, learn these in order:

1. Esc, i, :w, u, Space f f and Space f w.
2. K, g d, g r, Ctrl+o, Space c a and completion.
3. Build/run, then Space d b/r/o for C++ debugging.
4. Space g v for diff review, Space g g for LazyGit, and hunk actions.
5. Surround/movement, sessions and tmux detach/reattach.
6. One assistant, then task notes and isolated worktrees.

**Your complete capability recap:** you can navigate and understand projects,
edit structured text, get language feedback, format consistently, build/run/debug
C++, inspect and stage Git changes, save editor layouts, keep persistent terminal
workspaces, collaborate with several installed coding assistants, and isolate
parallel tasks. The detailed compatibility guide explains which optional systems
have deliberately not been activated and the substitutes available now.

## Cursor motion and Magicalbat additions

Restart Neovim, then try Normal-mode jumps such as gg/G or a search. Space u c
toggles the cursor trail. Ctrl+Arrow resizes splits; Visual J/K moves selected
lines; Visual p preserves copied text. Space f g finds Git files, Space f r
searches text, and F2/F4 provide rename/code-action aliases. MATLAB has syntax
support. [Read the complete conflict and usage guide](MAGICALBAT-MERGE.md).
