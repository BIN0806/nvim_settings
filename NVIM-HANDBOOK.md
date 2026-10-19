# Your complete Neovim coding handbook

> Repository edition: examples assume a clone at `~/.config/nvim-billy`.
> Run it with `NVIM_APPNAME=nvim-billy nvim`; see README.md and PROFILES.md.

**Updated setup snapshot: October 19, 2026.** This is the single reference for
what each tutorial contributes, how those ideas fit together, how to use the
combined environment, and exactly what your final stack contains. It assumes you
have not watched the tutorials. Tools are marked as installed, substituted or
optional so you can distinguish usable features from possible future additions.

## Contents

1. [What was reviewed](#what-was-reviewed)
2. [What each video contributes](#what-each-video-contributes)
3. [How the tools fit together](#how-the-tools-fit-together)
4. [Your integrated instruction set](#your-integrated-instruction-set)
5. [Practical workflow rules](#practical-workflow-rules)
6. [Verification and recovery](#verification-and-recovery)
7. [Your final installed stack](#your-final-installed-stack)

## What was reviewed

The original Dreams of Code transcript was extracted from YouTube's browser
panel and checked against the author's configuration. The additional videos were
reviewed through available chapters, descriptions, demonstration frames and
linked repositories. This was not uninterrupted playback of all five videos.

The Average Neovim Enjoyer video is a silent demonstration with no transcript
option. YouTube's other transcript requests were rate limited or remained on a
loading spinner. A [public archive of Kun Chen's auto-generated captions](https://github.com/chung-ta/youtube-transcripts/blob/main/l8-principals-agentic-engineering-workflow.md)
was retrieved and checked against his tool repositories. Full transcripts for
Rad Lectures, Mental Outlaw and Andrew Courter were not successfully retrieved.
Their feature descriptions below reflect the available evidence, not a claim
that every spoken instruction was transcribed.

Repositories can change after a video is recorded. Where newer source inspired
an addition, that distinction is identified below. Detailed research decisions
are also in [MERGE-NOTES.md](MERGE-NOTES.md); the original C++ timestamp checklist
is in [video-checklist.md](video-checklist.md).

## What each video contributes

### 1. Dreams of Code — The perfect Neovim setup for C++

[Video](https://www.youtube.com/watch?v=lsFoZIg-oDs) ·
[Author's configuration](https://github.com/dreamsofcode-io/neovim-cpp)

This supplies the main C/C++ development path: configure the editor, understand
code, format it, build a debug executable, then inspect it while running.

| Tool or feature in the tutorial | What it does for you | Result in your setup |
| --- | --- | --- |
| Neovim, Git and a Nerd Font | Editor, plugin downloads and readable interface icons | Existing Neovim/Git/font retained. |
| NvChad and Catppuccin | Ready-made editor interface and theme | Current NvChad v2.5 with Catppuccin. |
| Mason | Installs language tools and debugger executables | Installed; manages the selected tools. |
| clangd | C/C++ completion, navigation, diagnostics and code actions | Installed with indexing and clang-tidy enabled. |
| C/C++ treesitter grammars | Understands syntax for highlighting and structured features | Installed with current treesitter APIs. |
| clang-format and null-ls | Formats source using project style | clang-format retained; Conform replaces the old bridge. |
| Format-on-save and .clang-format | Keeps source layout consistent | One formatting hook; each project's style is respected. |
| nvim-dap and CodeLLDB | Pauses the running program at breakpoints | Installed and exercised with a real executable. |
| mason-nvim-dap and nvim-dap-ui | Configures the adapter and displays variables/calls | Installed with current nvim-nio dependency. |
| Integrated terminal and debug symbols | Builds code that the debugger can inspect | Terminal workflow and CMake Debug example supplied. |

**Useful landmarks:** clangd around 1:52–5:52, parser at 6:04, formatting at
7:03–10:28, debugger at 11:50–17:07. The old NvChad custom-directory layout and
old LSP setup calls were replaced with the current configuration structure.

**You gain:** the complete C++ loop: edit → save → build → run/debug → inspect.

### 2. Average Neovim Enjoyer — The Ultimate Neovim setup for C and C++

[Video](https://www.youtube.com/watch?v=w0WzxUPtKf0)

This silent demonstration reinforces the core C/C++ components rather than
introducing a second debugger or a fundamentally different development workflow.

| Demonstrated feature | Purpose | Result in your setup |
| --- | --- | --- |
| none-ls with clang-format | Runs a formatter from the editor | Existing Conform/clang-format provides this capability. |
| clangd configuration | Adds C/C++ language intelligence | Already installed; modern native LSP configuration retained. |
| C/C++ parsers | Adds syntax support | Already installed. |
| Formatting a C example | Demonstrates a consistent code style | Formatting works for both C and C++. |

The demo's unrelated formatter entries are not prerequisites for C/C++ and were
not copied as extra language stacks. Running both none-ls and Conform for the same
save operation would add duplicate configuration without adding a capability.

**You gain:** the same C/C++ conveniences through the formatter and language
server already integrated into the first setup.

### 3. The Rad Lectures — Minimal & Powerful: The Perfect NeoVim Setup for 2026

[Video](https://www.youtube.com/watch?v=lljs_7xB7Ps) ·
[Current linked source](https://github.com/radleylewis/nvim-lite)

This contributes modern Neovim configuration ideas and reusable editing tools.
Its independent foundation is translated into your existing NvChad foundation.

| Video chapter or linked-source feature | Benefit | Result in your setup |
| --- | --- | --- |
| Options/keymaps/autocommands, 5:52–26:13 | Better navigation and editing feedback | Centered search/scrolling, yank highlight, cursor restoration, useful defaults. |
| vim.pack, 26:13 | Manages plugins | Lazy remains the one plugin manager. |
| Explorer/search, 28:41 | Finds files and symbols | nvim-tree and Telescope retained. |
| mini.nvim, 31:13; selected modules from current source | Text objects, surrounding edits, movement and layouts | mini.ai, mini.surround, mini.move and mini.sessions enabled. |
| Git integration, 33:43 | Shows and works with changes | Gitsigns retained; hunk mappings, LazyGit and Diffview added. |
| Current treesitter, 35:38 | Uses modern parser configuration | Current API, extra parsers and native folds. |
| LSP/Mason, 38:58 | Installs and attaches language tools | Native LSP and Mason expanded to additional languages. |
| efm/format-on-save, 45:35–53:12 | Formatting and lint feedback | Conform plus language-specific diagnostics. |
| blink.cmp/LuaSnip, 53:12 | Completion and snippets | Existing nvim-cmp/LuaSnip stack retained. |
| Floating terminal/transparency, 57:22 onward | Terminal access and visual preferences | Existing terminals retained; Catppuccin stays active. Transparency is not enabled. |

The current source also contains later Rust/Obsidian and Linux notes-path choices.
Those are not treated as requirements from the recording. Personal vault paths
and extra SDKs were not guessed. Duplicate mini modules for pairs, icons,
notifications and comments were also left to the existing tools.

**You gain:** stronger editing primitives, saved layouts, modern language support
and navigation conveniences without learning a second set of competing defaults.

### 4. Mental Outlaw — NVChad: Turn Neovim Into An Awesome IDE

[Video, starting at your linked timestamp](https://www.youtube.com/watch?v=yW3ovyQCwpw&t=88s)

This explains the everyday IDE-like experience of NvChad: navigate a project,
switch files, arrange windows, and discover language and interface features.

| Feature shown or discussed in the walkthrough | What you can do | Your implementation |
| --- | --- | --- |
| NvChad interface and themes | Use a coherent editor UI and choose a theme | Current NvChad, Catppuccin and Space t h theme picker. |
| File tree | Browse project folders | Ctrl+n / Space e with nvim-tree. |
| Fuzzy file/text search | Find code without browsing every folder | Telescope: Space f f / Space f w. |
| Open buffers | Move between files already open | Tab / Shift+Tab and Space f b. |
| Splits and Ctrl+h/j/k/l navigation | Read related files together | Editor splits plus tmux-aware navigation. |
| Language/parsing tools | Get code feedback and highlighting | Your configured Mason/LSP/treesitter stack. |

The recording uses an older NvChad generation. Copying its old directory layout
over the current configuration would undo the migration. Rust source visible in
the demonstration does not mean that your Mac now has a configured Rust SDK/LSP.

**You gain:** a practical way to use the foundation you already have, with
documented equivalents for its current keys and configuration layout.

### 5. Andrew Courter — Configure Tmux and Vim As Your Dev Environment

[Video](https://www.youtube.com/watch?v=xUnXcVxcJho) ·
[Current dotfiles](https://github.com/exosyphon/dotfiles)

This contributes a keyboard-driven workspace surrounding the editor. Its Vim-era
plugin roles translate to the modern tools already installed.

| Video feature or current-source idea | Purpose | Your result |
| --- | --- | --- |
| tmux prefix, panes/windows and mouse | Arranges persistent terminal workspaces | Your Ctrl+s prefix retained; splits, navigation and mouse enabled. |
| Relative line numbers and Vim motions | Makes keyboard movement predictable | Enabled, with beginner examples below. |
| vim-tmux-navigator | Moves between editor windows and terminal panes | Installed on both sides. |
| Vim-Plug, CoC, NERDTree, fzf.vim, ALE | Plugin management, completion, exploration, search and diagnostics | Lazy, native LSP/nvim-cmp, nvim-tree, Telescope and language diagnostics. |
| Airline and gitgutter | Statusline and changed-line indicators | NvChad statusline and Gitsigns. |
| Comments and surround editing | Changes structured text quickly | Existing comments plus mini.surround. |
| Newer dotfiles: clipboard, layout persistence | Copies output and saves terminal layouts | macOS clipboard bindings, Resurrect and Continuum. |

**Landmarks:** tmux at 1:17–3:20 and 4:33–6:17; Vim from 6:17. The recording's
Ctrl+s/Nord-era setup resembles your original tmux file. The author's current
repository has changed; persistence improvements here come from newer source,
not a claim that every feature was in the 2022 recording. Your shell profile was
not replaced with his personal zsh configuration.

**You gain:** one workspace for editor, builds and assistants, with detach/reattach,
clipboard controls and recoverable layouts.

### 6. Kun Chen — L8 Principal's Agentic Engineering Workflow

[Video](https://www.youtube.com/watch?v=iQyg-KypKAA)

This is a broader engineering process: prepare context, define an outcome,
delegate implementation, validate behavior, and isolate independent tasks.

| Layer in the video | Your available implementation | Status / difference |
| --- | --- | --- |
| WezTerm + tmux + Neovim | Existing terminal + improved tmux + NvChad | Installed workflow; no terminal-emulator migration. |
| Claude Code, Codex, OpenCode, Pi | Assistant chooser and direct launch keys | First three CLIs resolve; Pi remains optional. |
| Global/project memory | Existing instructions preserved; project-context template supplied | Template is available; no global memory overwritten. |
| Skills | Existing instruction packs preserved; No Mistakes bundled skill installed | No bulk third-party skill installation. |
| OpenSuperWhisper | Typing, or existing macOS Dictation | Dedicated local voice tool remains optional. |
| AXI and Lavish planning | Tasks, Lavish, GitHub, Chrome DevTools and quota AXI installed privately | Available to Firstmate; browser tools still need a suitable browser session. |
| No Mistakes | v1.84.0 installed; per-project gate configured by kun | GitHub projects default to gated PR delivery; local projects use local-only. Merge approval required. |
| gnhf | Manually bounded assistant tasks | Unattended loops not enabled. |
| Treehouse | v3.1.4 installed for Firstmate workers | Reusable worktree leases; manual Space a w / Space a l also remain available. |
| Firstmate | Pinned private installation with kun project launcher | Codex primary and workers, tmux backend, separate state per project. |

**Landmarks:** terminal/tmux/editor 2:10–9:21; assistants and context 9:21–20:27;
voice/tool ergonomics 20:27–24:25; planning/validation 24:25–33:12; long-running
tasks/worktrees 33:12–40:23; Firstmate from 40:23.

Firstmate, Treehouse, No Mistakes and the AXI tools are now installed as a
project-scoped system. They coexist with the editor; the `kun` launcher supplies
the project environment. Codex is the selected default. [gnhf](https://github.com/kunchenguid/gnhf)
unattended loops and dedicated voice input remain optional.

**You gain:** a reusable supervisor/worker workflow with isolated worktrees,
persistent task context and optional gated PR delivery, alongside manual editing.

#### Do you have Kun's agentic setup yet?

**The core toolchain is installed.** You do not need to choose one project in
advance. Run this for any existing Git project with a first commit:

```sh
cd /path/to/your/project
kun
```

Replace the example path with your real project folder. In Neovim use **Space a k**
after restarting the editor. The default is **Codex for the primary, workers and
No Mistakes pipeline**. GitHub and Codex authentication were checked without a
model request. Normal first-use project/hook trust prompts may still appear.

On first run, `kun` registers your existing checkout, detects candidate commands,
creates separate project state and opens Firstmate in tmux. Subsequent runs reuse
that configuration/session. A GitHub origin selects No Mistakes PR delivery;
other projects select local-only delivery. Both require your approval for merges.
Existing project instructions and uncommitted files are preserved. Worker
worktrees begin from committed history, so commit the code they need first.

| Action | Command |
| --- | --- |
| Open/reopen the project supervisor | `kun` or Space a k |
| Prepare setup without a model conversation | `kun setup` |
| Inspect saved context/mode | `kun status` |
| Verify tools and login status | `kun doctor` |
| Preview the inferred test command | `kun check` |
| Actually run it | `kun check --run` |
| Run the inferred build | `kun check --kind build --run` |
| Choose local branches/worktrees | `kun setup --mode local-only` |
| Choose gated PR delivery | `kun setup --mode no-mistakes` |
| Inspect the project's gate | `kun exec -- no-mistakes status` |

The first assistant turn is onboarding only. After it explains the project, give
a focused task. A useful first request is:

> Inspect this project and propose one small improvement. Explain the plan and
> real validation commands first. Use one Codex worker in an isolated worktree.
> Stop with a reviewable local branch; do not publish or merge. Summarize what
> changed, what I can do, how to use it, and what you actually checked.

For PR delivery, explicitly ask it to prepare the validated result through No
Mistakes and wait for your merge decision. A gate submission can publish a branch
and open a PR. Setup itself pushes no code. Detected check commands are candidates;
verify them before relying on them. The launcher does not silently commit a CI
workflow or `.no-mistakes.yaml` into your project.

Ctrl+s then **w** chooses a tmux window, **s** chooses a session, and **d** detaches.
Detaching keeps work running. To stop, ask Firstmate to stop its workers and
confirm their state, then exit the primary. Codex's workspace sandbox and
on-request approvals remain enabled; a worker can pause for an approval prompt.

Twenty functional checks and four installed-tool checks passed without calling
a model. Your first bounded task will exercise the project-specific agent/PR
path. Pi, gnhf overnight loops, voice input and switching terminal emulators are
not prerequisites. The private installation also includes Lavish/AXI tools.

Read [the complete kun command guide](agentic/README.md) for step-by-step first
use, local/PR delivery, permissions, tool responsibilities, paths, side effects,
maintenance and recovery. No Mistakes initialization adds a local Git remote,
can install a per-project daemon/LaunchAgent, and refreshes its bundled user-level
skill; it does not replace global agent preferences. Firstmate has recorded
integration overlays for permission-adapter paths and preserving linked source
checkouts during startup.

Sources: [Firstmate](https://github.com/kunchenguid/firstmate),
[Treehouse](https://github.com/kunchenguid/treehouse),
[No Mistakes](https://github.com/kunchenguid/no-mistakes).

### Additional source — Magicalbat settings and cursor motion

[Magicalbat/Configs](https://github.com/Magicalbat/Configs) was reviewed on October
19, 2026. Its published config contains no cursor-animation settings. Your full
profile adds a terminal cursor-trail substitute with Space u c to toggle, plus
compatible Ctrl+Arrow resize, Visual J/K line movement, register-preserving paste,
Git-file/search keys, F2/F4 aliases and MATLAB syntax support. Restart Neovim to
load these additions. Native C++ debugging, help keys and tmux navigation remain.

Read [MAGICALBAT-MERGE.md](MAGICALBAT-MERGE.md) for every added action, exact source
revisions, conflicts and retained equivalents. The main conflicts are duplicate
pairing/LSP/theme setup, an older Treesitter API, a hidden-file shortcut that
would replace help, and tmux bindings that would interfere with current navigation.
The source's GUI font does not identify the animation used in a video.

**You gain:** an animated cursor in your existing terminal workflow, extra
selection/window controls, and a documented way to turn motion off.

## How the tools fit together

```text
Your macOS terminal
└── tmux: sessions → windows → panes
    ├── Neovim + NvChad: code, navigation and editor layouts
    │   ├── Lazy: loads editor plugins
    │   ├── Mason: installs selected language/debug executables
    │   ├── LSP + nvim-cmp + LuaSnip: understanding and completion
    │   ├── Treesitter + mini tools: structured reading and editing
    │   ├── Conform → formatter executable: formatting
    │   ├── DAP → CodeLLDB: C/C++ debugging
    │   └── Gitsigns / Diffview / LazyGit: change review
    ├── Shell: dependencies, build, run and tests
    └── Assistant CLI: planned tasks in this checkout or a separate worktree
```

Three distinctions prevent most confusion:

- **Editor tools versus project tools:** a language server can report errors; it
  does not install your application dependencies or run your app's tests.
- **Saving versus building:** saving writes and formats source; building creates
  the executable. Rebuild after C++ edits before running or debugging.
- **Layout versus process:** editor sessions remember files/splits; tmux keeps
  processes running while its server is alive. Saved layouts do not preserve a
  process's memory through a reboot.

The alternatives are mostly compatible in principle. Their overlapping roles
are why one plugin manager, completion engine, formatter path, explorer and
statusline were selected. Old keys were translated into your current key scheme:
Space s h keeps source/header switching, Space s s does horizontal splits, Space
r a renames, Space r n toggles relative numbers, and Git actions use Space g.

## Your integrated instruction set

### First: the minimum keyboard vocabulary

| What you mean | What to press |
| --- | --- |
| Return to command/navigation behavior | Esc; most shortcuts below start in Normal mode |
| Start typing / add a line below | i / o |
| Stop typing | Esc, or your existing jk shortcut |
| Save one file / all files | :w / :wa, then Enter |
| Close a window / quit all windows | :q / :qa; save when prompted |
| Undo / redo | u / Ctrl+r |
| Copy a line / paste below | yy / p |
| Select characters / whole lines | v / V, then move |
| Choose completion suggestions in Insert mode | Tab / Shift+Tab or Ctrl+n/p |
| Accept a suggestion / request suggestions | Enter / Ctrl+Space |
| Move through snippet fields | Tab / Shift+Tab when a snippet is active |
| Leave a terminal's input mode | Ctrl+x; press i to type into it again |
| Discover available shortcuts | Space, then pause; Space c h opens the cheatsheet |

Colon commands finish with Enter. Commands such as `cmake`, `git` and `npm`
belong in a terminal. Space shortcuts belong in Neovim's Normal mode. tmux uses
its separate Ctrl+s prefix. The same key can mean different things in different
programs, so check which pane and mode have focus.

### 1. Start in the right directory

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

### 2. Find things and understand unfamiliar code

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

### 3. Edit words and blocks with fewer keystrokes

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

### 4. Formatting, errors and language support

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

### 5. Keep the C++ build/debug loop clear

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

### 6. Review and organize Git changes

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

### 7. Arrange the editor and save layouts

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

### 8. Use tmux for persistent terminals and multiple tasks

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

### 9. Work with an assistant beside your code

| Action | Keys |
| --- | --- |
| Open the Kun project workflow (Codex) | Space a k |
| Toggle animated cursor trail | Space u c |
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

### 10. A repeatable agent workflow

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

### 11. Run a second task without mixing files

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

### 12. Keep the setup understandable

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

## Practical workflow rules

### A productive session from start to finish

1. **Choose one outcome.** State the behavior you want, the current problem and a
   concrete way to tell when the change works.
2. **Open the correct checkout.** Start from its project root. Check `git status`
   before working so you understand changes already present.
3. **Arrange three roles.** Keep code, commands/output and an assistant visible
   in editor splits or tmux panes. Use tmux for an assistant that should outlive
   an editor restart.
4. **Read before editing.** Use file/text search, K, definitions and references.
   For a bug, reproduce it and keep the steps or failing case.
5. **Plan the smallest useful change.** Record the plan and expected behavior in
   the task note. If working with an assistant, specify scope and relevant checks.
6. **Edit in short cycles.** Use completion and structured edits; save, inspect
   diagnostics, and run the most relevant feedback loop.
7. **Build/run/test.** Use the repository's documented commands. Reuse existing
   tests where appropriate and exercise the actual changed behavior.
8. **Review the entire change.** Inspect both the diff and the behavior. Stage
   coherent hunks, then create a clear commit through your usual Git workflow.
9. **Leave a useful handoff.** Record changed behavior, checks run, remaining
   limitations and the next step. Save useful editor layouts and detach tmux.

### Choose the feedback loop that matches the language

| Project | Fast feedback | Acceptance check |
| --- | --- | --- |
| C/C++ | clangd diagnostics → save/format → incremental build | Run the executable/relevant tests; use the debugger for runtime questions. |
| Python | Pyright/Ruff → save/format | Run tests and the changed behavior in the correct project environment. |
| JS/TS | Language diagnostics → save/format | Run declared typecheck/test/build scripts that apply to the change and use the app. |
| Shell | ShellCheck → save/shfmt | Test the script with representative inputs in the intended shell. |
| Configuration/docs | Syntax/schema/formatting where available | Check the consuming program or rendered output and verify links/examples. |

Your project's commands are the authority. Do not assume every Python project
uses pytest or every JS project has a script named `test`. A command that has no
tests to execute is different from evidence that a behavior works.

### Reduce friction without adding unnecessary tools

- Learn a small set of actions first: Esc, i, :w, search, definition, terminal and
  diff review. Add surround, hunk staging and layouts as they become useful.
- Run the narrow relevant check while editing; run the broader checks required
  by the project before accepting the result. Repeat checks when changes or
  failures justify it.
- Keep style in project files. Avoid making a personal editor preference rewrite
  unrelated files in a shared repository.
- Give parallel writers separate worktrees. Separate panes alone still point at
  the same files if both programs use the same checkout.
- Treat assistant memory as concise, verified project context. A task plan,
  project instructions, a reusable skill and model conversation history have
  different purposes.
- Require a clear stopping condition and evidence from an assistant. Starting
  additional agents is useful when tasks are independent and their results can
  be checked independently.
- Save important files and commit coherent work. Saved editor/tmux layouts are
  conveniences, not substitutes for source history or ordinary backups.

### When something looks wrong

| Symptom | First useful check |
| --- | --- |
| A shortcut inserts letters | Esc first; confirm the focused pane is Neovim. |
| Typing never reaches the assistant | Press i in its terminal buffer. |
| Ctrl+s does not save | It is the tmux prefix; use :w in Neovim. |
| C++ symbols/includes are missing | Check compile_commands.json and :checkhealth vim.lsp. |
| Python imports look missing | Confirm the project environment and installed dependencies. |
| Formatting fails or uses the wrong tool | :ConformInfo; check project style files and Space u f. |
| A breakpoint reflects old code | Save, rebuild with debug symbols, and restart debugging. |
| An assistant's changes do not appear | Check the checkout/path and :checktime; resolve unsaved edits deliberately. |
| Git history/review has no content | Check whether this repository has commits and changes. |
| A restored layout has shells instead of agents | Expected: process replay is disabled; start the desired programs manually. |

## Verification and recovery

The original installation passed 24 editor/tmux runtime checks: 10 C++, 11 merged
workflow and 3 tmux checks. Kun additionally passed 20 functional checks, four
installed-tool checks and its Neovim key/helper check. See
[verification/summary.md](verification/summary.md) for evidence and scope.

GitHub/Codex login status was verified on the original machine without a model
request. Logins and installation state are not copied by cloning this repository.
No paid worker pipeline, user-project PR or merge was run during installation.
The repository's packaging check parses Lua/Python and JSON without loading
plugins or calling a model: `python3 scripts/check.py`.

| Item | Location |
| --- | --- |
| Neovim configuration | Repository root: init.lua, lua/, lazy-lock.json |
| Optional tmux configuration | tmux.conf; installed separately |
| Kun installer and command guide | agentic/ |
| Project context starter | templates/PROJECT-CONTEXT.md |
| Practice C++ project | example/ |
| C++ profile | codex/profile-cpp / setup-2026-10-18-cpp |
| Combined pre-Kun milestone | setup-2026-10-18-merged |
| Full profile checkpoint | setup-2026-10-18-full |

Close Neovim before switching a clean checkout between profiles/checkpoints;
restore the selected plugin lock with `:Lazy restore`. Prefer separate
NVIM_APPNAME clones when comparing profiles. See [PROFILES.md](PROFILES.md) for
exact commands and the limits of a settings rollback. Local backups, caches,
credentials and private agent state are deliberately absent.

Every settings change should update CHANGELOG.md in the same commit: what
changed, why, how to use it, actual validation and restore notes. The optional
local pre-commit hook enforces a staged log update for settings edits.

## Your final installed stack

This is the usable stack after the merge, not a list of every tool mentioned in
the videos. Versions below are the recorded installation versions; the lockfile
contains exact plugin commits.

### Foundation and interface

| Layer | Selected tools / configuration | Purpose |
| --- | --- | --- |
| Editor | Neovim 0.12.6 | Editing engine and native LSP APIs. |
| Distribution | NvChad v2.5 | Coherent defaults, statusline, buffer line and terminal UI. |
| Theme | Catppuccin via NvChad/base46 | Editor colors; matching static tmux palette. |
| Font | Existing MesloLGS NF terminal font | Icons; other installed Nerd Fonts remain available. |
| Plugin management | lazy.nvim + lazy-lock.json | Plugin loading and recorded revisions. |
| Tool management | Mason | Selected external language/debug executables. |
| File navigation | nvim-tree, Telescope, ripgrep/fd | Explorer, file search, project text search and pickers. |
| Shortcut discovery | which-key and NvChad cheatsheet | Shows available commands. |
| Structured syntax | Current nvim-treesitter main API | Highlighting, syntax-aware folding and supporting structure. |

### Editing, completion and review

| Capability | Selected implementation |
| --- | --- |
| Language-client configuration | Native vim.lsp.config/enable + nvim-lspconfig definitions |
| Completion | nvim-cmp; LSP, snippets, buffer, Lua and async path sources |
| Snippets | LuaSnip + friendly-snippets |
| Automatic pairs | nvim-autopairs |
| Comments | Existing Neovim/NvChad comment workflow |
| Text objects | mini.ai |
| Surrounding edits | mini.surround |
| Line/block movement | mini.move |
| Named editor layouts | mini.sessions; manual save/read; terminal replay excluded |
| Formatting | Conform with the language-specific executables below |
| Git indicators/hunks | Gitsigns |
| Side-by-side review/history | Diffview |
| Full Git terminal interface | LazyGit |
| Focus view | zen-mode.nvim |
| Indent guides/icons | indent-blankline.nvim + nvim-web-devicons |
| Cursor motion | smear-cursor.nvim terminal trail; Space u c toggle; typing/tool panes quiet; Neovide skipped |
| Reading conveniences | Relative lines, centered movement, yank feedback, restored position, open-by-default folds, Markdown wrap/spell |
| External file changes | Guarded checktime with autoread for unmodified buffers |

### Installed language and debug tools

| Files | Understanding / diagnostics | Formatter | Debugging preset |
| --- | --- | --- | --- |
| C/C++ | clangd 23.1.0 with clang-tidy | clang-format 23.1.3 | CodeLLDB 1.12.3 via DAP |
| Lua | lua-language-server | StyLua | Not configured |
| Python | Pyright + Ruff | Ruff | Not configured |
| JS/TS/JSX/TSX | typescript-language-server | Prettier | Not configured |
| Bash/sh | bash-language-server + ShellCheck | shfmt | Not configured |
| JSON/JSONC | vscode-json-language-server | Prettier | Not configured |
| HTML/CSS/YAML/Markdown | Syntax parsers | Prettier | Not configured |
| TOML/CMake/MATLAB | Syntax parsers | No dedicated formatter configured | Not configured |

The C/C++ debugger stack is **nvim-dap + mason-nvim-dap + nvim-dap-ui + nvim-nio
and CodeLLDB**, with extra adapter startup allowance for macOS. CMake, Ninja and
Clang support the supplied C++23 practice project. Project dependencies and
language SDKs remain separate from these editor tools.

Configured parser inventory: **c, cpp, lua, luadoc, vim, vimdoc, query, cmake,
bash, json, markdown, markdown_inline, python, javascript, typescript, tsx, html,
css, yaml, toml, matlab**. Some related file types reuse a parser rather than having a
separately named grammar.

### Workspace and agent layer

| Layer | Installed / active selection |
| --- | --- |
| Terminal emulator | Your existing macOS terminal; no WezTerm migration |
| Terminal multiplexer | tmux 3.8; Ctrl+s prefix, vi copy mode, mouse, clipboard, splits and pane navigation |
| Cross-editor/pane navigation | vim-tmux-navigator in Neovim and tmux |
| tmux plugin manager | TPM |
| Terminal layout persistence | tmux-resurrect + tmux-continuum; periodic save, manual restore, process replay off |
| Assistant CLIs | Codex default; Claude Code 2.1.303 and OpenCode also available |
| Assistant selection | Space a a for manual use; Space a k / kun for Firstmate with Codex; Pi remains optional |
| Project planning | On-demand .agent-notes/task.md + a project-context starter |
| Parallel task isolation | Git worktree helper: create a new branch/checkout, list existing worktrees |
| Quality workflow | Define outcome → plan → implement → run relevant checks → inspect behavior/diff → approve integration |
| Project command | kun: detects project, creates/reopens its private Firstmate home and tmux session |
| Orchestrator | Firstmate pinned at 45dd50a5e12b; recorded worker-path/startup-sync integration overlays |
| Worktree pool | Treehouse v3.1.4 |
| Validation / PR gate | No Mistakes v1.84.0; initialized per GitHub project by kun, local-only mode available |
| Agent tool interfaces | gh-axi 0.1.43, chrome-devtools-axi 0.1.44, tasks-axi 0.2.6, quota-axi 0.1.64, lavish-axi 0.1.90 |
| Permission posture | Codex workspace-write / on-request; merge approval required; no unattended loop enabled |

**Optional and not activated:** Pi, WezTerm migration, gnhf unattended loops,
OpenSuperWhisper, Obsidian vault integration, additional language SDKs/framework
servers and additional debug adapters. The Kun core tools are installed;
registration/gate setup happens separately for each project when you run `kun`.
No paid worker pipeline has been run during installation.

### Complete locked editor-plugin inventory

The installation lockfile records the following plugins, including supporting
dependencies. Their exact commits remain in `lazy-lock.json`.

```text
LuaSnip, NvChad, base46, cmp-async-path, cmp-buffer, cmp-nvim-lsp, cmp-nvim-lua,
cmp_luasnip, conform.nvim, diffview.nvim, friendly-snippets, gitsigns.nvim,
indent-blankline.nvim, lazy.nvim, mason-nvim-dap.nvim, mason.nvim, menu, mini.nvim,
minty, nvim-autopairs, nvim-cmp, nvim-dap, nvim-dap-ui, nvim-lspconfig, nvim-nio,
nvim-tree.lua, nvim-treesitter, nvim-web-devicons, plenary.nvim, telescope.nvim, ui,
smear-cursor.nvim, vim-tmux-navigator, volt, which-key.nvim, zen-mode.nvim
```
