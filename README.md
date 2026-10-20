# Documentation

**Billy's Neovim, tmux and Codex setup — updated October 20, 2026.**

This is the single user guide and change log for the setup. Start with the quick
reference, then read the category you need. It assumes you have not watched the
tutorials. Feature descriptions, exact commands, source decisions, verification
and restore points are kept together here.

**Current profile:** `main` is the full daily setup. `codex/profile-cpp` is the
smaller C++ profile. **Editor leader:** Space. **tmux prefix:** Ctrl+s.
**Assistant default:** Codex. **Cursor effect:** Space u c toggles it.

## Contents

| If you want to… | Read |
| --- | --- |
| Start working or find a common shortcut | [Quick start](#quick-start) |
| Open the home screen | [Home dashboard](#home-dashboard) |
| Practice ThePrimeagen’s course with your actual shortcuts | [Learn Vim with this setup](#learn-vim-with-this-setup) |
| Learn modes, navigation and editing | [Editing and navigation](#editing-and-navigation) |
| Use completion, formatting, builds and the debugger | [Languages, formatting and debugging](#languages-formatting-and-debugging) |
| Review changes, arrange windows or use tmux | [Git review, layouts and tmux](#git-review-layouts-and-tmux) |
| Control the flying cursor and extra shortcuts | [Cursor effects and extra controls](#cursor-effects-and-extra-controls) |
| Work with an assistant or initialize a project harness | [Coding with Codex and Kun](#coding-with-codex-and-kun) |
| Decide whether Herdr or Lotus adds anything to Firstmate | [Firstmate, Herdr and Lotus](#firstmate-herdr-and-lotus) |
| Check Kun’s advanced and full-stack workflows | [Kun workflow coverage and everyday commands](#kun-workflow-coverage-and-everyday-commands) |
| Inspect or customize automatic editor actions | [Autocommands you can control](#autocommands-you-can-control) |
| Install a profile, switch versions or restore a checkpoint | [Profiles, installation and restore points](#profiles-installation-and-restore-points) |
| See what each video/source contributed and why choices differ | [Tutorial sources and merge decisions](#tutorial-sources-and-merge-decisions) |
| Update settings, solve a problem or inspect test evidence | [Maintenance, troubleshooting and verification](#maintenance-troubleshooting-and-verification) |
| See the dated settings changes | [Change log](#change-log) |
| Copy a starter for your project's facts and commands | [Project context template](#project-context-template) |
| See the complete installed stack | [Final installed stack](#final-installed-stack) |
| Find the people behind the setup | [Sources and credits](#sources-and-credits) |

## Quick start

### Home dashboard

Your setup uses **NvChad**, with **lazy.nvim** managing its plugins. LazyVim is a
separate distribution; installing the Lazy plugin manager alone does not add
LazyVim's home screen. NvChad's own dashboard was previously left at its default
`load_on_startup = false`. It is now enabled in `lua/chadrc.lua`.

Start `nvim` or `nvim .` to see the home screen. Opening a specific file with
`nvim path/to/file` still opens that file directly. From an existing editor
window, press **Space u d** or run `:Nvdash` to open the dashboard.

| On the dashboard | Action |
| --- | --- |
| ff | Find a file. |
| fo | Open the recent-files picker. |
| fw | Search project text. |
| th | Open the theme picker. |
| ch | Open the mapping cheatsheet. |
| j / k, then Enter | Select and run a menu action. |

These are dashboard-local keys without Space; your usual Space f f / Space f w
shortcuts still work while editing. Use `:q` to quit. The dashboard starts no
coding agent. To disable automatic display, set `load_on_startup = false` in
`lua/chadrc.lua` and restart Neovim; the manual shortcut remains available.

### Open a project

On the configured Mac, save any work and restart Neovim after settings changes.
From a terminal, change into the application's main directory, then open it:

```sh
cd /path/to/your/project
nvim .
```

Replace the example path with your real project folder. For a separate clone at
`~/.config/nvim-billy`, launch it with `NVIM_APPNAME=nvim-billy nvim .` instead.
The [installation section](#profiles-installation-and-restore-points) explains
that isolated profile. The original working editor uses `~/.config/nvim`.

Start with **edit → save → build → run or debug → review**. Saving writes and
formats source; it does not build an executable or run your application's tests.

### Everyday shortcuts

Press Esc first. `Space f f` means three keys in sequence. `Ctrl+n` means hold
Control and press n. Uppercase letters require Shift.

| Goal | Keys |
| --- | --- |
| Start typing / stop typing | i / Esc (or jk) |
| Save / quit a window | :w / :q, then Enter |
| Open the home dashboard | Space u d or :Nvdash |
| Find a file / search project text | Space f f / Space f w |
| Browse files / switch open buffers | Ctrl+n / Tab or Shift+Tab |
| Definition / references / documentation | g d / g r / K |
| Rename / code action | Space r a or F2 / Space c a or F4 |
| Format now / toggle format on save | Space f m / Space u f |
| Open a shell below / beside the code | Space h / Space v |
| Breakpoint / start or continue debugger | Space d b / Space d r or F5 |
| Review a diff / open LazyGit | Space g v / Space g g |
| Save / restore editor layout | Space S s / Space S r |
| Move between editor windows and tmux panes | Ctrl+h/j/k/l |
| Toggle the animated cursor | Space u c |
| Open a manual assistant / Kun workflow | Space a a / Space a k |
| Leave a Neovim terminal's input mode | Ctrl+x; i resumes input |
| Discover shortcuts / find help | Space, then pause / Space f h |

### A productive session

1. Open the project root and find the relevant file.
2. Read unfamiliar code with K, g d and g r; Ctrl+o returns from a jump.
3. Edit with completion, save, and address relevant diagnostics.
4. Build/run the application or use a breakpoint to investigate behavior.
5. Run the project's real checks and inspect the intended behavior.
6. Review the diff, commit a coherent result and record the handoff.

For the first week, learn Esc, i, :w, Space f f and Space h first. Add language
navigation, debugging, Git review, sessions and one assistant as they become
useful. Each detailed category below ends with what you can now do.

### How the layers fit

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

[Back to contents](#contents)

## Editing and navigation

### Modes and command vocabulary

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

### Learn Vim with this setup

ThePrimeagen’s [vim-fundamentals](https://github.com/ThePrimeagen/vim-fundamentals)
is cloned locally as **vim**, inside **vim learning**:

```sh
cd "/Users/billy/Documents/ChatGPT/HATE/vim learning/vim"
./learn
```

Use your normal `nvim` configuration. Start with `./learn lesson basic-usage`,
then `./learn 0`; progress through exercises 1–6 as the readings introduce them.
`./learn list` shows all 31 lessons in course order. The course README has the
full index and adaptation notes. There is no website build to install.

| From the course folder | What you can do |
| --- | --- |
| `./learn 0` through `./learn 6` | Work on a writable copy and keep your progress between sessions. |
| `./learn reset 0` | Reset that exercise after backing up your previous copy in .practice/backups/. |
| `./learn js` | Practice on the JavaScript example; `./learn reset js` also backs up edits. |
| `./learn lesson NAME` | Read a named reference lesson; use `./learn list` to find names. |
| `./learn nav` | Open the prepared vim-nav-playground project for explorer, marks and quickfix lessons. |
| `./learn plugin` | Edit a local Lua demo; `:luafile %` loads it and `:CourseHello` runs it. |

The launcher makes practice copies under `.practice/`. It keeps Markdown/ASCII
exercises literal by disabling format-on-save, wrap, spell display, concealment
and folding in course buffers. Reference lessons are read-only; the copies are
writable. These overrides belong to the launched Neovim process. Opening course
files directly with `nvim` does not load that course helper automatically.

Both lesson trees teach your actual tools: **nvim-tree** instead of NetRW,
**Lazy/Telescope** instead of Vim-Plug/FZF, and Lua modules instead of replacing
an init.vim. The course’s Ctrl+j/k quickfix maps would replace window navigation;
use the following installed aliases throughout your normal editor instead:

| Action, in Normal mode | Keys |
| --- | --- |
| Repeat the last f/F/t/T character search | `Space ;` repeats; comma reverses the search. |
| Next / previous quickfix entry | ]q / [q |
| Open / close the quickfix window | Space q o / Space q c |

Your existing semicolon still opens command mode, Ctrl+h/j/k/l still navigates
windows/tmux, and Visual p preserves the copied register. Those differences are
explained in the relevant lessons. Quickfix needs results first; `./learn nav`
and `:vimgrep /SOCKET_OPEN/gj src/*.c` supply a working example. Use `:cfirst`
if you want to start at the first result before trying ]q.

**Practice workflow:** read one short lesson, do its exercise, use u to retry a
change, and save with :w. Add one motion at a time to real coding. Learn operators
with motions (`dw`, `ciw`, `di{`) before memorizing more plugins. Use `:help` for
the command under study, and check mode/case before assuming a key is broken.
Save and restart existing Neovim sessions to load the five new global mappings.

The pinned completion plugin also needed a compatibility guard: its InsertEnter
callback injected keys even when completion was disabled for a recording macro,
which could lose inserted text from the macro register. `lua/configs/completion.lua`
wraps that one callback to skip recording/replay and leaves ordinary completion
initialization intact. No completion shortcuts changed. Re-run the course’s
Insert-mode macro regression when updating nvim-cmp; the guard explicitly checks
that the reviewed callback still exists.

The course now marks differences directly before the affected instructions:
**CHANGED FOR YOUR SETUP** explains the original action and replacement;
**ALREADY BOUND** identifies installed mappings; **BINDING NEEDED** identifies
an optional shortcut that has not been assigned. The underlying colon command
still works. Each optional recipe is commented Lua with its config location,
mode, keys, prerequisites and save/restart instructions. Native Vim motions and
commands are explicitly distinguished from custom mappings.

The optional examples use Space l r to reload a saved Lua experiment and
Space l h to run CourseHello after loading the demo. They are not installed;
choose them only if you want those extra shortcuts. The course README includes
a linked original-versus-current comparison and the comment legend. Keep this
annotation style when adding future instructions that need a new binding.
Existing exercise-0 annotations were merged with a backup and no reset of progress.

The course is published separately in
[BIN0806/nvim_learning](https://github.com/BIN0806/nvim_learning) on main, with
`codex/billy-keybindings` retaining the working branch. Its README includes
fresh-clone instructions and source credits at the bottom. Original source is
preserved at `source-vim-fundamentals-aed0a14`; the published course checkpoint is
`course-2026-10-20-published`. The navigation fixtures remain a separate ignored
clone at `7d58a0d`. Personal practice files and backups stay local. Restoring a
settings tag does not reset course progress or switch that repository’s branch.

### Autocommands you can control

An autocommand runs a small action when an editor event occurs. A named group
keeps related actions together; `clear = true` lets that group reload without
adding a second copy of each action. Your local rules live in `lua/autocmds.lua`.

| Event / group | What your setup does |
| --- | --- |
| FileType / CppIndent | Use two-space indentation for C/C++. |
| TextYankPost / WorkspaceComfort | Briefly highlight copied text. |
| BufReadPost / WorkspaceComfort | Restore the last valid cursor position. |
| FileType / WorkspaceComfort | Enable wrap, line breaks and spelling for prose. |
| FocusGained, BufEnter, CursorHold / WorkspaceComfort | Refresh external changes in unmodified Normal-mode file buffers. |
| TermOpen / WorkspaceComfort | Keep a newly opened NvChad horizontal terminal's height when you split the code above it. |

**New from Courter's autocommand example:** open a bottom terminal with Space h,
then return to the code and use Space s s. The terminal keeps its height. Inside
the terminal, Ctrl+x leaves input mode; `:setlocal nowinfixheight` lets Neovim
resize that window normally again. `:resize 12` sets its height explicitly.
NvChad already enters terminal input mode for its own terminals. The new rule
only adjusts its `NvTerm_sp` windows; generic debug/test terminals and vertical
terminals keep their existing behavior.

Use these commands in Neovim to inspect the rules:

```vim
:autocmd WorkspaceComfort
:autocmd CppIndent
:verbose autocmd TermOpen
:lua vim.print(vim.api.nvim_get_autocmds({ group = "WorkspaceComfort" }))
```

Descriptions identify each rule in the output. To disable the terminal-height
rule for future terminals in the current editor session:

```vim
:lua vim.api.nvim_clear_autocmds({ group = "WorkspaceComfort", event = "TermOpen" })
```

This does not change an already open window's `winfixheight`; use the local
option above there. To restore the configured rules after a temporary change:

```vim
:lua dofile(vim.fn.stdpath("config") .. "/lua/autocmds.lua")
```

For your own rule, add a separately named group to `lua/autocmds.lua`, for example:

```lua
local group = vim.api.nvim_create_augroup("MyWorkspaceDemo", { clear = true })
vim.api.nvim_create_autocmd("BufEnter", {
  group = group,
  pattern = "*.txt",
  desc = "Announce a text file for learning autocommands",
  callback = function()
    vim.notify("Text file opened")
  end,
})
```

Reload that file and enter a `.txt` buffer to try it. Run
`:lua vim.api.nvim_del_augroup_by_name("MyWorkspaceDemo")` to remove the demo for
this session; remove its source block too if it should stay removed. Clear your
own group when experimenting, rather than all plugin autocommands. The modern
Lua API supports callbacks and groups directly; see `:help nvim_create_autocmd()`.

**You can now:** understand which automatic actions run, find their source,
experiment without stacking duplicate callbacks, and undo a local rule.

### Find files and understand unfamiliar code

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

### Edit words, blocks and surrounding characters

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

### Buffers, windows and terminals

A **buffer** holds an open file in memory. A **window** displays a buffer; two
windows can show the same file. A **tmux pane** is a terminal area outside Neovim.
A language server understands code, while the completion menu presents its
suggestions. A formatter changes layout; it does not fix the program's logic.

In Insert mode, Tab/Shift+Tab choose completion entries, Enter accepts and
Ctrl+e closes the menu. Ctrl+Space requests completion if macOS/your terminal
delivers that shortcut. Tab also moves through active snippet fields. Snippets
and automatic brackets reduce repeated typing.

**You can now:** distinguish the focused program and mode, navigate files and
symbols, and make structured edits without confusing a buffer with a terminal.

[Back to contents](#contents)

## Languages, formatting and debugging

### Language feedback and formatting

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
| TOML/CMake/MATLAB | Syntax highlighting/structure | No dedicated formatter configured |

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

### Build and run C++

First open the supplied `example/` directory or the root of your own project.
For the isolated clone, use `cd ~/.config/nvim-billy/example` before launching
`NVIM_APPNAME=nvim-billy nvim src/main.cpp`.

Press `Esc`, then `Space h` to open a terminal below your code. The terminal starts
in the current working directory. Type the following commands there:

```sh
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build build
./build/app
```

The first command configures the project. `-S .` means the source directory is
the current directory; `-B build` puts generated files in a directory named
`build`. Ninja is the build tool. `Debug` requests debug information suitable for
breakpoints and inspecting variables. `CMAKE_EXPORT_COMPILE_COMMANDS=ON` generates
the compilation database that helps clangd understand the project.

The second command compiles the program. The third runs it, and this example
prints `Total: 100`.

Configure when creating the build directory or changing configuration options.
After ordinary source changes, usually run just `cmake --build build` again, then
run or debug the updated executable. The example enables C++23 in CMake; a different
project chooses its own standard and executable name.

The terminal has its own input mode: keys go to the shell while it is active.
Ctrl+x returns to Neovim's Normal mode. You can then move to another window or
use `:q` to close the terminal window. Press `i` while focused in a terminal window
to send input to the terminal again. `Space v` opens a vertical terminal instead.

For a single C++ file, you can also use this simpler build from the example's
directory:

```sh
mkdir -p build
clang++ -std=c++23 -g -O0 src/main.cpp -o build/main
./build/main
```

`-g` includes debug information, `-O0` disables optimizations for easier stepping,
and `-o build/main` names the resulting executable. This direct command is useful
for small exercises; CMake records how larger projects should be built.

You can now compile and execute your programs without leaving Neovim.

### Debug C++ step by step

A breakpoint tells the debugger to pause before executing a particular line.
While paused, you can inspect variables and run one line at a time. This helps
answer questions such as “Why did this value change?” or “Which function called
this code?”

First follow the build commands above. Return to the code with Ctrl+x and window
navigation. In `src/main.cpp`, put your cursor on the `std::cout` line. Press
`Space d b` to place a breakpoint; a marker appears beside the line.

Press `Space d r` to begin. If a configuration picker appears, choose
**LLDB: Launch**. **LLDB: Launch (args)** is available when your program needs
command-line arguments. At the executable prompt, enter:

```text
~/.config/nvim-billy/example/build/app
```

That is the built program, rather than its `.cpp` source file. If you used the
direct compiler command instead, choose the executable ending in `build/main`.

When the breakpoint is hit, the highlighted line is generally the line about to
execute. Debugger panels open automatically. In this example, the `total`
variable is already `100` at the `std::cout` line.

| Action while debugging | Shortcut | Meaning |
| --- | --- | --- |
| Toggle a breakpoint | `Space d b` | Add or remove the stop on the cursor's line. |
| Start / continue | `Space d r` or F5 | Start a session, or run until another stop or program exit. |
| Step over | `Space d o` or F10 | Execute the next line without stepping through a called function's internals. |
| Step into | `Space d i` or F11 | Enter a called function when its code is available. |
| Step out | `Space d O` or F12 | Continue until the current function returns. |
| Evaluate | `Space d e` | Inspect the expression under the cursor, or selected text in Visual mode. |
| Show/hide debugger panels | `Space d u` | Change panel visibility while keeping the session. |
| Stop the debug session | `Space d q` | Terminate the current debugging run. |

Use the Space shortcuts if your Mac uses function keys for media controls.
Step over is a useful first choice while learning; step into can take you
into standard-library implementation code.

The **Scopes** panel shows variables in the current context. Enter expands a
structured value. **Stacks** shows the chain of function calls that led here.
**Watches** lets you track expressions across pauses; focus that panel and enter
Insert mode to add an expression. **Breakpoints** lists your stops. The console
and REPL provide program output and debugger interaction.

Keep inspections simple while learning. Evaluating a function call can execute
code and change program state. A variable's value is meaningful only where that
variable exists and while the program is paused in a suitable frame.

The panels close automatically when the program finishes or the session ends.
After changing source code, save and rebuild before starting another session.

You can now reproduce a bug, pause where it happens, inspect values, and follow
the program's execution instead of guessing from output alone.

### Project prerequisites and language limits

Editor packages do not install application dependencies, create a Python virtual
environment or run npm install. Python needs its project environment; TypeScript
needs dependencies and tsconfig; C/C++ needs a compiler/build configuration and
compile_commands.json. Shell diagnostics target Bash/sh, not a zsh language
server. Framework-specific servers remain project choices.

C/C++ has the supplied debugger preset. Python/TypeScript language support does
not install their debug adapters. MATLAB has syntax support only. Extra Go,
Rust, C#, Godot or Obsidian SDK/vault settings were not inferred from tutorials.

[Back to contents](#contents)

## Git review, layouts and tmux

### Review and organize Git changes

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

### Arrange editor windows and save layouts

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

### Use tmux for persistent terminals

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

### Give independent tasks separate worktrees

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

### Optional tmux installation

The tracked `tmux.conf` is installed separately from Neovim. Back up an existing
`~/.tmux.conf`, install TPM and the listed tmux plugins through their normal
setup, then reload the configuration. Clipboard bindings use macOS `pbcopy`.
Layout saving is periodic; restoring is deliberate. Restoring layouts does not
replay agent processes or reconstruct a running program's memory after reboot.

[Back to contents](#contents)

## Cursor effects and extra controls

### The flying cursor

His published files contain no cursor-animation plugin or Neovide animation
settings. The repository alone cannot identify the exact effect you saw. It
does set a GUI font, which does not establish which GUI or animation he uses.

Your terminal now uses [smear-cursor.nvim](https://github.com/sphamba/smear-cursor.nvim),
a terminal cursor-trail implementation inspired by Neovide. Its reviewed revision
is pinned in lazy-lock.json. This is a substitute for the requested visual effect,
not an animation copied from his repository.

Restart Neovim. In Normal mode, try `gg`, `G`, a search jump or movement across a
line. The cursor leaves a short trail as it travels. **Space u c** or
`:SmearCursorToggle` turns it off/on for the current session. The options are in
`lua/configs/cursor.lua`; set `enabled = false` there to start with it disabled.
It uses a Catppuccin-compatible color, ordinary block glyphs and a moderate frame
rate. It stays quiet while typing, in terminal mode, on the command line and in
the configured help/finder/tree/debugger tool buffers. Cross-buffer smearing is
off. The plugin skips Neovide so that a future GUI launch uses its native cursor
animation rather than two renderers. Neovide is a separate optional application.

The effect draws temporary floating cells; it does not animate the OS mouse or
change buffer text. Terminal rendering and font support affect how smooth it
looks. The toggle is useful when screen sharing or when you prefer less motion.

**You can now:** get the flying/trailing cursor in your current terminal/tmux
workflow and turn it off immediately without switching profiles.

### Additional shortcuts and MATLAB syntax

Start in Normal mode unless the table says Visual mode.

| Keys / feature | What you can do |
| --- | --- |
| Space u c | Toggle cursor animation for this session. |
| Ctrl+Up / Ctrl+Down | Increase/decrease the current split's height by one row. |
| Ctrl+Left / Ctrl+Right | Decrease/increase the current split's width by one column. |
| Visual J / K | Move selected lines down/up and keep the selection. Normal J and K keep their existing meanings. |
| Visual p | Replace selected text while preserving the copied register for repeated pastes. |
| Space f g | Find Git-tracked files through Telescope. |
| Space f r | Search project text; Space f w still works. |
| F2 | Rename the LSP symbol. Space r a still works. |
| F4 | Open LSP code actions. Space c a still works. |
| MATLAB parser | Syntax highlighting/structure for MATLAB buffers; no MATLAB SDK, language server, formatter or debugger is added. |

For selection moves, press `V`, extend the selection with j/k, then use J/K.
For repeated replacement, yank a word, select another word with `viw`, then p.
For resizing, create a split with Space s v or Space s s first. macOS Mission
Control or terminal settings may intercept Ctrl+Arrow before Neovim sees it;
`:resize +1` and `:vertical resize +1` are direct command alternatives.

[Back to contents](#contents)

## Coding with Codex and Kun

### Choose a manual assistant

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

### Use a repeatable task workflow

1. **Define the outcome.** Describe what the user should see, how to reproduce the
   problem, and what successful output/behavior looks like.
2. **Get a concrete plan.** Ask for affected files and tradeoffs. For a UI change,
   ask for a preview or mockup before implementation. A Markdown plan works for
   simple changes; Firstmate can also use the installed Lavish planning tool.
3. **Record real project context.** Keep build/test commands, architecture facts
   and non-obvious conventions in the project's context file. A starter is in
   [Project context template](#project-context-template). Copy and adapt it deliberately; no global agent
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

**You can now:** evaluate an assistant's output by the intended behavior and
evidence, rather than treating “done” as the only acceptance criterion.

### Install or reopen the Kun workflow

The core toolchain is installed on the original configured Mac. A fresh clone
contains its installer and sources, not account logins or installed binaries.
Opening Neovim does not install this toolchain or start a model conversation.

If you choose to install it on a machine, use Python 3.11+, Node/npm, Git, tmux,
GitHub CLI and an authenticated Codex CLI. The installer has macOS/Linux release
platform support; this snapshot was tested on Apple Silicon macOS. From the
settings clone:

```sh
python3 agentic/install.py
~/.local/bin/kun doctor
```

Keep `~/.local/bin` on PATH. To start in an application project:

```sh
cd /path/to/your/project
kun
```

You can also run `kun /path/to/your/project` from elsewhere, or use Space a k in
Neovim. The project needs Git and a first commit; the command does not stage
files or invent that commit. Clone a GitHub project locally before using it.

Kun prepares/reopens a separate Firstmate home, registers the existing checkout,
detects candidate checks and starts Codex as primary with Codex workers. Each
project has private state and a named tmux session. Reopening reuses a live
session. The first turn is onboarding, not an invented coding task. Starting
`kun` is a real assistant conversation and can use account quota; `kun setup`
configures without a model conversation.

### What each agentic layer does

| Layer | Job | What you do |
| --- | --- | --- |
| Neovim + NvChad | Edit, navigate, format, debug and review code | Keep editing normally; use Space g v for a diff. |
| tmux | Keep the supervisor and worker terminals organized | Ctrl+s then w chooses a window; Ctrl+s then d detaches. |
| Firstmate | Turn an outcome into scoped tasks, supervise workers and report results | Explain the desired behavior, constraints and stopping point. |
| Codex | Reason about the project and implement assigned work | Approve required actions and inspect results. Your existing model settings apply. |
| Treehouse | Lease/reuse isolated Git worktrees for tasks | Workers can edit separate branches without sharing one working directory. |
| No Mistakes | Validate a committed branch, repair eligible issues and deliver a PR | Use the gate after agreeing on the checks and publication scope. |
| Tasks AXI | Keep durable task records across sessions | Ask Firstmate for queued, active, blocked and completed work. |
| Lavish AXI | Support interactive planning/presentation workflows | Ask for a concrete plan or preview when it helps. |
| GitHub / Chrome DevTools / quota AXI | Give agents structured GitHub, browser and usage tools | Browser inspection needs a suitable browser session; installation alone does not attach one. |

You do not need to learn each CLI before your first task. Firstmate orchestrates
the layers; the smaller commands below let you inspect and troubleshoot them.
The manual assistant, task-note and worktree keys still work independently.

### First task and example prompts

1. Save your code. Commit the work that a new worker needs to see. Uncommitted
   changes are preserved, but isolated worktrees start from committed history.
2. Run `kun` from the project's original checkout. Complete any genuine first-use
   trust or sign-in prompt shown by Codex. Existing Codex and GitHub logins were
   verified during setup; no new account or API key was created.
3. Let the onboarding turn finish. Check that it identifies the project,
   instructions, delivery mode and plausible build/test commands correctly.
4. Give one small task with an observable result. Start with one worker until
   you have seen the complete plan → implementation → validation → review cycle.
5. Read the result and evidence. Review the branch or PR that actually contains
   the changes; your original checkout does not display a worker's unmerged diff.
6. Decide whether to merge. Merge autonomy is off in both supported modes.

A useful first prompt:

> Inspect this project and propose one small improvement. Explain the affected
> files and the exact validation commands before implementing it. Use one Codex
> worker in an isolated worktree. Preserve my unrelated edits. Stop with a
> reviewable local branch; do not publish or merge. Afterward explain what changed,
> what I can now do, how to use it, and what you actually checked.

For a task you already understand:

> Fix [specific behavior]. Success means [observable result]. Keep scope to
> [files or component]. Run [known checks] and demonstrate the behavior. Prepare
> a PR through No Mistakes after validation, then wait for my merge decision.

Replace bracketed phrases with real details. A request to prepare a PR includes
publishing the branch after checks; choose a local result when that is what you
want. Installing the workflow does not publish anything by itself.

**You can now:** open a project-specific supervisor, give it a bounded task,
inspect evidence and approve the final integration yourself.

### Kun command reference

Run project commands from inside that project, or add `--project /path/to/project`
before other arguments. `kun doctor` is independent of the current folder.

| Command | Behavior |
| --- | --- |
| `kun` | Prepare/reopen the project and attach to Firstmate. |
| `kun setup` | Prepare project configuration without starting a model. In PR mode it also initializes the local gate/daemon. |
| `kun start --print` | Perform setup and print the launch details without starting a model. This is a setup preview, not a read-only command. |
| `kun status` | Show saved project path, assistant, mode and candidate checks. |
| `kun status --json` | Show the full saved profile, including its home directory. |
| `kun doctor` | Check installed tools and read-only GitHub/Codex login status. |
| `kun check` | Preview the detected test command. |
| `kun check --run` | Actually execute the detected test command and record its exit code. |
| `kun check --kind build --run` | Execute the detected build command. Other kinds: lint, typecheck, check, format. |
| `kun setup --mode local-only` | Select local branch/worktree delivery for this project. |
| `kun setup --mode no-mistakes` | Select validation/PR delivery; requires an origin remote. |
| `kun setup --agent claude` | Explicitly switch this project's primary, default workers and pipeline to Claude Code. Codex is the default. |
| `kun exec -- no-mistakes status` | Inspect the project's gate using its private environment. |
| `kun exec -- no-mistakes doctor` | Diagnose the gate's requirements and configuration. |
| `kun exec -- no-mistakes` | Open the gate's interactive interface. Its wizard can offer to commit/push; read the prompts. |
| `kun exec -- tasks-axi list` | Inspect task records in this project's Firstmate environment. |

An explicit `--agent` also resets the fallback worker profile to that harness
while preserving task-specific routing rules. Ordinary reopening preserves custom
routing. See [routing preferences](#routing-preferences-that-survive-reopening).

After changing the selected assistant, exit the old primary normally and run
`kun` again. Reopening a live session intentionally does not kill it or replace
the conversation. Existing workers keep the assistant they were launched with.

`kun check --run` runs actual project code, including any package-script lifecycle
hooks. A detected command is a candidate, not proof of correctness. CMake's
candidate assumes an already configured `build/` directory. Dependencies,
services, environment variables and SDKs still belong to the project. Run
`kun setup` again after changing its manifests to refresh detection.

### Local branches versus gated PR delivery

With a GitHub `origin`, the first setup selects **no-mistakes**. Otherwise it
selects **local-only**. You can choose explicitly with `--mode`; that selection
persists. An existing native Firstmate registry mode is preserved on reopening.

**Local-only:** Firstmate works with local branches/worktrees. It does not need a
GitHub repository. Ask it for a reviewable branch, inspect that branch and the
checks, then approve any merge into your source checkout.

**No Mistakes:** Setup adds a local Git remote named `no-mistakes` and initializes
its gate under this project's private state. Ordinary `git push origin` still
bypasses this tool; Firstmate should use the gate for its selected PR workflow.
When you explicitly push a committed branch through the gate, its pipeline can
perform review, tests, documentation/lint checks, publish the validated branch,
open a PR and watch CI. Its AI stages use your assistant account.

For manual submission after reviewing and committing your task branch:

```sh
git push no-mistakes HEAD
kun exec -- no-mistakes status
```

This submission can publish the validated result. A completed pipeline is not a
merge approval. Your repository's existing CI and branch-protection rules still
apply. If you contribute through a fork or lack write access to `origin`, keep
local-only mode until the correct push target is configured.

The launcher records likely check commands in `data/project-context.md`. It does
not silently commit a `.no-mistakes.yaml` or a new CI workflow. The onboarding
agent must verify the real commands and use any existing repository policy.
For a reproducible team policy, ask it to propose a `.no-mistakes.yaml`, review
it, and merge it through the project's normal process. No Mistakes reads trusted
default-branch policy for sensitive settings. A generic detector cannot infer a
project's intended behavior, secrets or deployment rules.

**You can now:** choose local review or gated PR delivery per project, while
keeping validation commands and merge decisions explicit.

### Sessions, permissions and stopping work

- Your tmux prefix remains **Ctrl+s**. Then press **w** for windows, **s** for
  sessions, or **d** to detach. Detaching leaves agents working. Run `kun` again
  to return to that project's session.
- The supervisor window is named `helm`; workers may appear in other windows.
  Give steering instructions to the supervisor. If a worker is waiting for an
  approval, open its window and answer the actual prompt.
- To stop work, ask Firstmate to stop its workers and confirm their state, then
  exit the primary. Closing a terminal or detaching is not a reliable stop action.
- A Codex primary uses the upstream foreground watcher workflow. It has different
  waiting/resume ergonomics from a Claude primary; do not assume the video's
  Claude-specific background behavior is identical.
- Codex launches use `workspace-write` with `on-request` approvals. Permission
  adapters remove Firstmate's default bypass flags. Required approvals can pause
  workers; this is an interactive supervised setup.
- Firstmate's private home is added as a writable control directory. Workers
  have their own checkout. Startup fleet fetch/fast-forward is disabled for
  registered source checkouts, and startup branch pruning is disabled.
- Native Firstmate disables Codex worker lifecycle hooks while retaining its
  turn-end notification. The primary keeps the normal trust flow for its hooks.
- Use one writing task per worktree. Different terminal panes alone do not
  isolate edits. Ask for more workers only when the tasks are independent.
- Keep the final handoff concrete: changed behavior, files/branch/PR, commands
  actually run, observed results, limitations and the next action for you.

### Private files, side effects and tool maintenance

| Item | Location / behavior |
| --- | --- |
| Global command | `~/.local/bin/kun` |
| Shared private tools | `~/.local/share/kun/toolchain` |
| Pinned Firstmate source | `~/.local/share/kun/firstmate` |
| Per-project Firstmate homes | `~/.local/share/kun/projects/<name>-<path-hash>` |
| Per-project No Mistakes state | `~/.local/share/kun/nm/<path-hash>` |
| Auditable launcher/install sources | `agentic/`: kun.py, agent_guard.py, overlay.py, install.py. |
| Reviewed versions/checksums | agentic/toolchain-lock.json; installation.json is generated privately on install |

Project registration is a symlink to your original checkout, not a copied
application. The home contains its own preferences, task records and detected
context. Your project's existing `AGENTS.md`/`CLAUDE.md` are preserved. No global
agent preferences or shell profile were replaced.

No Mistakes init installs/refreshes its bundled user-level skill in
`~/.agents/skills/no-mistakes/SKILL.md` and
`~/.claude/skills/no-mistakes/SKILL.md`. Existing copies encountered by this
launcher are backed up under `~/.local/share/kun/backups/skills`. Its per-project
daemon can register a macOS LaunchAgent. These are native tool side effects.
The AXI packages' optional global hook installers were not run.

The private Firstmate checkout has two recorded integration overlays: worker
launch templates use absolute permission-adapter paths, and bootstrap skips
fleet sync for linked source projects. Hashes are recorded in installation.json.
This avoids relying on shell PATH order or silently fast-forwarding your source
checkout at startup. Unexpected edits to these vendor files are preserved and
cause installation to stop rather than overwrite them.

The installer pins reviewed versions. Re-running it reinstalls this reviewed
snapshot; it is not a rolling upgrade. Review upstream changes before updating
the pins/overlays. Do not blindly self-update the private Firstmate checkout over
its integration changes. Dedicated Python/Node launch paths keep project virtual
environments from accidentally selecting incompatible runtimes for the launcher
and AXI tools.

To reinstall this snapshot:

```sh
python3 ~/.config/nvim-billy/agentic/install.py
kun doctor
```

Before removing a project gate, stop its tasks and use
`kun exec -- no-mistakes eject --help` to inspect the native removal procedure.
For just stopping its service: `kun exec -- no-mistakes daemon stop`. Do not
delete active worktrees, project state or daemon files while they are in use.

[Back to contents](#contents)

### Kun workflow coverage and everyday commands

The three Kun videos describe the same family of tools at different levels:
[the original workflow](https://www.youtube.com/watch?v=iQyg-KypKAA),
[high-throughput orchestration](https://www.youtube.com/watch?v=MSbacZ99E14), and
[a full-stack build](https://www.youtube.com/watch?v=kPN564Kol14&t=5038s).
You have the core infrastructure. That is different from having every optional
account, fleet topology, UI customization and app deployment in his demos.

| Capability | Your current status |
| --- | --- |
| Firstmate + Codex, isolated worktrees, task records, tmux, No Mistakes and AXI tools | Installed; `kun doctor` verified the tools and GitHub/Codex logins on October 19. |
| Planning, implementation and interactive review | Tools available; request an artifact with acceptance criteria, variants and decisions when useful. |
| Task-specific worker routing | Supported in config/crew-dispatch.json; Kun now preserves it when reopening. Fresh homes still default to Codex. |
| Quota tool / automatic provider choice | quota-axi installed; actual quota-aware choices need valid profiles and authenticated providers. Extra subscriptions are not configured by this setup. |
| Fleet recap and decision catch-up | Firstmate ships Bearings and Ahoy; invocation examples below. |
| Second mates / remote fleet | Upstream supports them; no persistent secondmate or remote host was provisioned here. |
| One supervisor across many projects | Possible in native Firstmate; Kun normally creates a separate home/session for each project, so there is no single combined fleet by default. |
| Herdr, Pi and Calm presentation | Optional. Herdr/Pi remain uninstalled; pinned Calm support is for Pi and gated Claude Code support, not Codex. |
| Discord/X relay and unattended merging | Not enabled. These add external channels or different merge authority; they are not requirements for coding. |
| A running full-stack/iOS application | Project-specific; this editor setup is not a deployed app or a configured Apple developer environment. |

The [pinned Firstmate configuration guide](https://github.com/kunchenguid/firstmate/blob/45dd50a5e12bc3f5e009a4e18fa35ce7f7a71681/docs/configuration.md)
owns dispatch and backend settings. Its [Calm guide](https://github.com/kunchenguid/firstmate/blob/45dd50a5e12bc3f5e009a4e18fa35ce7f7a71681/docs/calm.md)
describes the harness-specific presentation. These are source-supported features,
not a claim that every optional workflow was exercised with real workers here.

#### Catch up without inspecting every worker

Inside the **Firstmate conversation started by kun**, ask in plain language or
invoke its bundled skills. These are agent messages, not shell commands:

| Message to Firstmate in Codex | Purpose |
| --- | --- |
| `$bearings` | Get a fresh overview of current fleet work and decisions. |
| `$bearings file` | Also write today's status report in the private home. |
| `$bearings include PRs` | Include live GitHub PR checks in that overview. |
| `$ahoy` | Recap visible session events and unanswered decisions since your prior message. |
| `$stow` | Ask for a durable knowledge/task handoff before ending a session. |

If the skill picker does not expose a name, ask Firstmate to read and follow its
bundled skill of that name. These are Firstmate-internal skills; do not install
copies globally into unrelated projects. The `$` invocation is Codex-specific;
other harnesses use their own skill conventions.

Try this workflow prompt after the project's onboarding:

> Propose a small task queue for this outcome. Separate research from code
> changes, identify dependencies, and use at most two Codex workers for independent
> tasks. Keep each writing task in its own worktree. Present one review artifact
> with the result, checks, limitations and decisions I need to make. Keep merge
> approval with me. Explain what I can now do when each task completes.

Start with one worker for your first real task. The prompt above is an example
of requesting parallel work, not a background fleet started by this installation.

#### Routing preferences that survive reopening

Each private Firstmate home has `config/crew-dispatch.json`. Ask Firstmate to
show the relevant file and propose a change before saving it. Natural-language
`rules` select task profiles; `default` is the fallback profile or profile array.
A model and effort can be specified when verified for that assistant, or omitted
to retain its defaults. Do not copy dated model IDs or provider credentials from
a video. [Upstream dispatch documentation](https://github.com/kunchenguid/firstmate/blob/45dd50a5e12bc3f5e009a4e18fa35ce7f7a71681/docs/configuration.md#crew-dispatch-profiles-configcrew-dispatchjson)
describes the schema and quota selection.

- Normal `kun`, `kun setup` and `kun start --print` preserve an existing routing
  file byte for byte. A missing file is initialized with Codex as the default.
- An explicit `kun setup --agent claude` changes the primary/pipeline and replaces
  the routing fallback with Claude. Existing task rules are retained; a model or
  effort tied to the old fallback is removed. An explicit `--agent codex` likewise
  selects Codex as the fallback.
- Invalid JSON or a non-object routing file stops setup with an error, preserving
  the file and previous project profile. Firstmate bootstrap owns validation of
  the detailed routing schema. This update does not reconstruct preferences that
  an older launcher may already have overwritten.

This makes the routing feature usable without forcing extra assistants or
inventing account access. Your default remains Codex unless you choose otherwise.

#### Full-stack acceptance workflow

The linked **1:23:58** is inside the E2E integration chapter (starting 1:20:33).
The nearby visible frame at 1:24:02 describes a final acceptance gate across the
client, backend, identity/permissions and persistence. The reusable lesson is
to prove connected behavior after the pieces build successfully.

1. Define a small observable outcome, roles and data flow before creating tasks.
2. Have a scout inspect the existing application, dependencies and actual commands.
3. Review a plan or interactive prototype, then implement independent pieces in
   isolated worktrees using agreed interfaces.
4. Integrate them and exercise a real user path in the intended browser/simulator.
5. Verify authorization failures, error states and persistence/restart behavior
   where those are relevant to the application.
6. Record observed results, skipped scenarios and evidence. Run the project's
   agreed validation gate, then review the branch/PR and decide on integration.

For a web app, configure its runtime, services and browser session. A native iOS
app additionally needs the appropriate Xcode SDK/simulator, signing/account setup
when required, and app-specific backend configuration. Browser-tool installation
alone does not attach a browser or test your product. No Apple sign-in, hosting,
domain, database or external secrets were provisioned by this settings audit.

**You can now:** use the core Kun workflow, recover fleet context, keep custom
routing, and apply the video's plan → build → integrate → verify loop. Optional
fleet/UI features are clearly separated from the tools already ready to use.

### Firstmate, Herdr and Lotus

**Recommendation for your current setup:** keep Firstmate + Codex + tmux.
Neither comparison video adds a prerequisite. Herdr is an optional workspace
upgrade; Lotus is an optional separate assistant, useful mainly if you want
local model inference or its Mac-specific conveniences.

| Tool | Main role | What you already have / what it adds |
| --- | --- | --- |
| Neovim | Edit, navigate, format and debug code | Your current editor. |
| tmux | Host terminal sessions, windows and panes | Your installed Firstmate backend. |
| Firstmate | Delegate tasks, supervise workers, use isolated worktrees and coordinate delivery | Your installed Kun/Codex workflow. |
| Herdr | Host agent terminals with a mouse-friendly workspace and agent-state display | An alternative to tmux that Firstmate supports. |
| Lotus | Chat with an assistant and run Mac/file/shell tools, with an optional local model | An alternative manual assistant; not a verified Firstmate worker in this setup. |

#### Jilles — Herdr in about 6 minutes

[Video](https://www.youtube.com/watch?v=qnIu-Xu64H0) ·
[Official docs](https://herdr.dev/docs/) ·
[Firstmate's pinned Herdr backend guide](https://github.com/kunchenguid/firstmate/blob/45dd50a5e12bc3f5e009a4e18fa35ce7f7a71681/docs/herdr-backend.md)

The video covers integrations/agent skill at 0:20, workspaces at 1:08, agent
states at 2:28, tabs/panes at 3:13, session recovery at 3:58, and agent-driven
sub-agents at 4:50. Native working/blocked/idle indicators and clickable workspace
management are its clearest additions. Session detach/rejoin already exists in
your tmux setup. The demo of spawning sub-agents overlaps with Firstmate's crew,
but terminal controls alone do not supply your task intake, supervision and
delivery policy. [Herdr's agent guide](https://herdr.dev/docs/agents/) describes
its state detection and integrations.

**Can they combine? Yes:** Firstmate can run workers in Herdr instead of tmux.
The pinned Firstmate source already includes that adapter. Treehouse still owns
task worktrees; Herdr owns the terminal endpoints. However, your custom `kun`
launcher explicitly sets `FM_BACKEND=tmux`, writes `config/backend` as tmux and
uses tmux to launch/attach. Setting `FM_BACKEND=herdr kun` alone will not switch
it. A supported change needs a Kun backend option plus matching launch, doctor,
attach and stop behavior, verified in a separate Firstmate home first.

**Decision:** documented as optional, left uninstalled. Consider it when status
visibility and mouse controls solve an actual problem. A migration should use a
compatible Herdr protocol/version and avoid nesting tmux in Herdr by accident.
The installed adapter requires protocol 14 or newer; that floor alone is not a
guarantee that every newer release was tested. Recovery restores layouts or
resumes supported agents; a reboot cannot preserve a running process's memory.
See [Herdr's session-state guide](https://herdr.dev/docs/session-state/).

**You gain from this review:** a clear upgrade path for terminal usability while
retaining Firstmate's orchestration. You do not need a second supervisor.

#### Fanxy — Lotus 2.6

[Video](https://www.youtube.com/watch?v=WZ9SPo_rnVU) ·
[Official source and commands](https://github.com/Fanxy13/homebrew-lotus)

The video presents local AI at 0:15, file/command actions at 0:25, web search and
memory at 0:43, permissions/pets at 0:58, and optional features/background removal
at 1:15. Current source also supports a browser chat; that is a later/current
capability, not an extra Neovim requirement.

**Overlap:** coding chat, file edits and command execution overlap with your
manual Codex/Claude/OpenCode launchers. **Distinct benefit:** MLX inference on
Apple Silicon, plus Mac conveniences such as pets and image background removal.
Firstmate does not supply a local model engine. Lotus does not replace your
Firstmate task/worktree/delivery setup, and no Lotus worker adapter was verified.

**Decision:** documented as optional, left uninstalled. Use it separately if you
want those features. Local weights require disk space and enough unified memory;
cloud providers and web search still involve network requests. Local inference
is not a promise that every Lotus feature stays offline. Your current default
assistant remains Codex; no startup hooks or model downloads were added.

**You gain from this review:** a choice of local assistant features without
confusing them with the system that coordinates your coding workers.

[Back to contents](#contents)

## Profiles, installation and restore points

### Install a separate full profile

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

### Choose a profile or exact snapshot

| Selection | What it contains |
| --- | --- |
| `main` | Full daily profile and current maintained documentation. |
| `codex/profile-cpp` | Smaller tested C++ profile: NvChad, clangd, formatting and CodeLLDB; no extra agentic layer. |
| `setup-2026-10-18-cpp` | Immutable C++ foundation checkpoint. |
| `setup-2026-10-18-merged` | Combined editor/tmux checkpoint before Kun integration. |
| `setup-2026-10-19-cursor` | Full profile with terminal cursor animation and compatible Magicalbat additions. |
| `setup-2026-10-18-full` | Full profile including optional Kun/Codex launcher sources and instructions. |
| `setup-2026-10-19-documentation` | The full profile with the unified guide named Documentation.md and migrated history checks. |
| `setup-2026-10-19-readme` | Full profile with the unified guide displayed as README.md on GitHub. |
| `setup-2026-10-19-videos` | Full profile with scoped terminal-height behavior, inspectable autocommands and the additional video comparisons. |
| `setup-2026-10-19-kun-routing` | Full profile with persistent worker-routing preferences and the Kun follow-up audit. |
| `setup-2026-10-19-dashboard` | Full profile with the startup dashboard and Space u d home shortcut enabled. |
| `setup-2026-10-20-vim-learning` | Current full profile with course-compatible shortcuts and Insert-mode macro protection. |

The initial commits package saved, tested milestones in order. Tags pin exact
snapshots; profile branches can receive compatible updates. The smaller C++
branch and old tags retain their historical files, including earlier guide names.
The current main profile uses this one README.md.

### Inspect settings history

```sh
git log --graph --decorate --oneline --all
git log --follow --format=fuller -- README.md
# Older entries before consolidation:
git log --format=fuller -- CHANGELOG.md
git show setup-2026-10-18-full
git diff setup-2026-10-18-cpp..setup-2026-10-18-full -- lua lazy-lock.json
```

The commit bodies and README.md describe features, key changes, validation and
restore points. Saved setup milestones were packaged in order on October 18,
2026; their commit times are packaging times, not the original edit times.

### Try profiles side by side

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

### Restore an exact checkpoint

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

### Create another profile

For example, a distinctly minimal writing/review setup could start from the
closest existing profile:

```sh
git switch main
git switch -c codex/profile-writing
```

Remove/change the relevant features, update profile.json and README.md, check
it, commit, and push with `git push -u origin HEAD`. Use a separate clone and
NVIM_APPNAME such as `nvim-billy-writing` to try it. A different color choice
alone usually does not need a permanent branch; a checkpoint tag can be enough.

### Name a stable checkpoint

After checks pass and the intended changes are committed:

```sh
git tag -a setup-2026-10-19-full -m 'Full profile: describe the verified changes and usage'
git push origin setup-2026-10-19-full
```

That date/name is an example for a future milestone. Use its actual date and a
unique name. Never move a published checkpoint tag to a different commit.

### What a settings restore includes

Git restores this repository's config, documentation, scripts and plugin lock.
It does not restore unsaved buffers, project files, credentials, model quotas,
Mason package versions, external compiler SDKs, tmux plugin revisions, private
Firstmate homes, daemon state or other machine files. Those were intentionally
not uploaded. The optional installer pins its reviewed toolchain; check the
appropriate release/compatibility notes before reinstalling an old tool version.

[Back to contents](#contents)

## Tutorial sources and merge decisions

### What was reviewed and transcript limits

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
appear in the [foundation conflicts](#why-overlapping-foundations-were-combined-selectively)
and the [timestamped C++ comparison](#original-tutorial-timeline) below.

### Additional video review — October 19, 2026

Your new batch contains three previously reviewed videos and four new ones.
The repeated videos were checked against the installed choices; their detailed
breakdowns remain below, rather than duplicating their configuration.

| Video in this batch | Outcome |
| --- | --- |
| typecraft — J9yqSdvAKXY | Existing editor already supplies the demonstrated components; retain one plugin manager/theme/statusline. See video 7 below. |
| Andrew Courter — xUnXcVxcJho | Already integrated tmux/navigation workflow; current dotfiles reviewed again at d0aa24654906. See video 5. |
| Dreams of Code — lsFoZIg-oDs | Existing C++/format/debug path retained; no second LSP/formatter/debugger added. See video 1. |
| The Rad Lectures — lljs_7xB7Ps | Existing mini tools, sessions, Git review and language setup retained. See video 3. |
| Andrew Courter — qN6BuJpsFbQ | Add scoped horizontal-terminal height behavior and readable rule descriptions; document rule management. See video 8. |
| Jilles — qnIu-Xu64H0 | Comparison only: Herdr can replace tmux beneath Firstmate. [Assessment](#jilles--herdr-in-about-6-minutes). |
| Fanxy — WZ9SPo_rnVU | Comparison only: Lotus is a separate assistant/local-model option. [Assessment](#fanxy--lotus-26). |

**Evidence limits for this batch:** titles, authors, descriptions and chapters
were retrieved for all four new videos. Their advertised English caption tracks
returned empty bodies; public transcript requests failed, and the browser
transcript panels inspected for typecraft/Courter stayed loading. Courter's
example code at 6:19 was visually checked: TermOpen with startinsert/winfixheight,
plus TextYankPost highlighting. Linked repositories, installed NvChad code and
Firstmate's pinned backend documentation were inspected. No complete new
transcript was recovered, and this review is not claimed as uninterrupted
playback of all seven links. Raw local research is not uploaded to this repo.

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

### 7. typecraft — How to Configure Neovim to make it Amazing

[Video](https://www.youtube.com/watch?v=J9yqSdvAKXY) ·
[Author's current configuration](https://github.com/cpow/cpow-dotfiles)

The video teaches a small Lua-based editor from scratch. Its current linked
configuration was reviewed at `b3cc17c402a5cb9b3b7bcaee8dfdd2b9f29d41c0`;
the old neovim-config-lua URL resolves to that same configuration.

| Tutorial idea | Your equivalent / decision |
| --- | --- |
| init.lua and modular require calls, 1:00–2:10 | Already split across init.lua, options.lua, mappings.lua, autocmds.lua and configs/. |
| Packer, 3:00 | Keep Lazy. [Packer's own notice](https://github.com/wbthomason/packer.nvim) says it is unmaintained; the author's current config also uses Lazy. |
| Theme, powerline/statusline and file tree, 4:10 | Catppuccin + NvChad statusline + nvim-tree already serve these roles. |
| Separate plugin configuration, 5:05 | lua/plugins/init.lua declares plugins; lua/configs/ holds their settings. |
| Treesitter and Telescope, 6:55 | Already enabled; Space f f finds files and Space f w searches project text. |
| Clear search highlighting | Your Esc mapping; Space h stays the horizontal terminal. |

Gruvbox and lualine are valid alternatives, but changing the theme or statusline
would be a preference swap. Loading two statusline configurations or Packer next
to Lazy would create overlapping ownership. Later tools in the current dotfiles
(Copilot, Oil, Swagger/Markdown previews and more) are not treated as requirements
of this nine-minute tutorial. No extra plugin/account was added from them.

**You can now:** locate the file that controls each part of your editor, change
one module at a time, and understand why the existing plugins cover this video.

### 8. Andrew Courter — Autocommands in Neovim

[Video](https://www.youtube.com/watch?v=qN6BuJpsFbQ) ·
[Companion article](https://levelup.gitconnected.com/create-autocommands-in-neovim-7199af02a85e)

The chapter sequence teaches command-line creation (0:39), Lua callbacks (1:48),
listing (4:26), removal/disabling (5:22), then examples (6:14). Only the public
preview of the companion article was available; no paywall was bypassed.

| Demonstrated behavior | Integration |
| --- | --- |
| Named groups and Lua callbacks | Existing CppIndent and WorkspaceComfort groups clear their own previous registrations. |
| Listing and disabling rules | Every local rule now has a description; commands are in [Autocommands you can control](#autocommands-you-can-control). |
| TermOpen → startinsert | NvChad already starts its own terminals in input mode; avoid a blanket callback that also grabs test/debug terminals. |
| Terminal winfixheight | Added for NvChad horizontal terminals only; you can turn it off per window. |
| TextYankPost feedback | Existing vim.hl.on_yank provides this; keep one callback. |

**You can now:** inspect, create, reload and remove a small event rule, and keep
a bottom shell steady while rearranging code. This adds no plugin or paid API.

### 9. Kun Chen — High Throughput Agentic Engineering with Kun

[Video](https://www.youtube.com/watch?v=MSbacZ99E14) ·
[Firstmate source](https://github.com/kunchenguid/firstmate)

This extends the original workflow rather than introducing another Neovim
configuration. The following comparison uses the author's chapters and the
installed Firstmate source, not a recovered full transcript.

| Chapter / idea | Your setup / decision |
| --- | --- |
| Firstmate and crewmates, 0:50 / 6:34 | Already installed with Codex workers and Treehouse isolation. |
| Remove distractions, 4:58 | Calm is harness-specific; keep Codex and use concise handoffs/recaps. |
| Model routing, 7:12 | Upstream profile support and quota tool are present; fixed Kun so it no longer overwrites custom profiles on every open. |
| Tracking / catching up, 15:56 / 43:40 | Built-in Bearings/Ahoy available; guide now includes their use. |
| Second mates, 22:07 | Source support exists; optional topology, not provisioned or live-tested here. |
| Interactive prototypes / feedback, 25:31 / 40:58 | Lavish tool installed; request an artifact with options and a decision rather than only a prose dump. |
| Discord and X relay, 29:26 | Optional external integration; not activated. |
| Context management, 32:49 | Use concise durable context and the harness's own compaction behavior; no copied environment tuning. |
| Yolo versus No Mistakes, 37:51 / 51:08 | Keep the installed gate and explicit merge decisions; unattended merge mode remains off. |

One Kun project home normally covers one registered project; manually added
native registry entries are preserved, but separate Kun homes do not become a
shared global fleet. Herdr/remote hosts and additional subscriptions are optional
extensions, not missing editor plugins. Existing launch protections are retained.

**You can now:** keep task-specific routing across sessions and use fleet recaps
and review artifacts, with a clear list of optional scale-up features.

### 10. Kun Chen — L8 Principal Building a Full Stack App with Agentic Engineering

[Video at your timestamp](https://www.youtube.com/watch?v=kPN564Kol14&t=5038s)

This is an application-building demonstration of the same agentic process. Its
value is how research, prototypes and verification connect, rather than a second
plugin stack. Your 1:23:58 link falls inside the 1:20:33 E2E chapter.

| Chapter / phase | Your available workflow |
| --- | --- |
| Herdr + Firstmate, 0:26; Calm, 3:40 | Firstmate is installed; tmux/Codex is your current alternative presentation/backend. |
| Product ideation, 5:41 | Define the user outcome, constraints and acceptance criteria with the primary. |
| Market / technical research, 16:53 / 19:06 | Use bounded scout tasks and source-backed findings before implementation. |
| Parallelize, 23:43 | Independent workers use worktrees; agree on shared interfaces first. |
| Interactive planning / UX prototypes, 29:56 / 42:29 | Lavish tool available for a plan or comparison artifact; review it before building. |
| Secrets, 59:41 | Project-specific configuration and account setup; keep private values out of this settings repo. |
| Frontend, 1:13:52; browser automation, 1:18:08 | Existing editor/agent/browser tooling; the project still needs its runtime and a browser session. |
| E2E, 1:20:33; architecture review, 1:33:46 | Prove the integrated behavior, inspect evidence and review the design; a successful build alone is insufficient. |

The visible frame near the linked timestamp was checked at 1:24:02. It outlines
backend/client acceptance conditions and external deployment inputs. A generic
Neovim configuration cannot supply that app's Apple identity, signing, servers
or database. Use the [full-stack acceptance workflow](#full-stack-acceptance-workflow)
for your own application's actual requirements.

**You can now:** follow the process with the tools already installed, while
knowing which services and SDKs must be configured in the target project.

### Kun follow-up audit evidence — October 19, 2026

The original iQyg-KypKAA is already covered in video 6, with the previously
retrieved archived auto-caption transcript and its limitations. For MSbacZ99E14
and kPN564Kol14, public page metadata and chapter lists were retrieved; English
caption bodies were empty and public transcript requests returned HTTP 400.
The known transcript archive contained only the original video, not these two.
The linked full-stack segment was inspected visually, and installed Firstmate
code/docs were audited for the capabilities above. No full transcript or
uninterrupted viewing of the two new recordings is claimed. Third-party search
summaries were not treated as authoritative implementation instructions.

### Original tutorial timeline

| Video time | Tutorial step | Installed equivalent |
| --- | --- | --- |
| 0:16–0:45 | Install current Neovim, a Nerd Font, and Git | Neovim 0.12.6, Git, and Nerd Fonts already installed. Existing terminal font is MesloLGS NF; JetBrainsMono Nerd Font is also installed. |
| 0:59–1:36 | Back up existing configuration and install NvChad | Full backup including Git state; current NvChad starter retained. Old v2.0 custom modules replaced with current `lua/plugins/` and `lua/configs/` layout. |
| 1:37–1:50 | Select Catppuccin | `base46.theme = "catppuccin"`; Space t h opens the theme picker. |
| 1:52–4:16 | Install clangd through Mason | `clangd` is declared in Mason `ensure_installed`; Mason binary is preferred. |
| 4:19–5:52 | Configure clangd with NvChad capabilities | Current NvChad defaults plus `vim.lsp.config` / `vim.lsp.enable`. The old signature-help bug workaround is omitted. |
| 6:04–6:18 | Install C++ tree-sitter grammar | C and C++ parsers installed using the current tree-sitter API. |
| 6:20–7:01 | Test completion, automatic includes, diagnostics | nvim-cmp LSP completion; clangd background index and clang-tidy enabled; actual completion and diagnostics checked. |
| 7:03–8:42 | Install clang-format through Mason and configure formatter | Mason `clang-format`; Conform replaces the archived null-ls bridge. |
| 8:45–9:31 | Format with Space f m and use project `.clang-format` | Same shortcut; formatter resolves configuration relative to the file. |
| 9:33–10:28 | Format on save; demonstrate Google style | One Conform format-on-save hook; example uses Google style. Existing projects keep their own style. |
| 11:50–12:34 | Add nvim-dap and Mason CodeLLDB | Same debugger and package manager. |
| 12:36–13:21 | Configure mason-nvim-dap with default handlers | Same plugin and default adapter setup, with longer connection timeouts for macOS. |
| 13:23–13:51 | Add nvim-dap-ui and automatically open/close panels | Same UI and session listeners; current required nvim-nio dependency included. |
| 13:56–15:41 | Add Space d b / Space d r mappings | Same bindings, plus optional step/evaluate/stop shortcuts. |
| 15:45–16:28 | Build with debug symbols in an NvChad terminal | Space h opens terminal; example builds with CMake Debug. The direct clang++ example in the C++ build section follows his terminal workflow. |
| 16:30–17:07 | Set a breakpoint, select executable, inspect and control execution | CodeLLDB launch prompt and UI; actual breakpoint, variable evaluation, resume and exit checked. |

Modernization references: [NvChad](https://nvchad.com/docs/quickstart/install/),
[LSP configuration](https://github.com/neovim/nvim-lspconfig),
[Conform](https://github.com/stevearc/conform.nvim),
[mason-nvim-dap](https://github.com/jay-babu/mason-nvim-dap.nvim),
[nvim-dap-ui](https://github.com/rcarriga/nvim-dap-ui).

### Why overlapping foundations were combined selectively

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

### Magicalbat conflicts

Reviewed [Magicalbat/Configs](https://github.com/Magicalbat/Configs) at
`14e1f6c5821f9c15e1805f1dc929c227c484d9ae`. All published Neovim Lua and tmux
settings were examined. The repo contains no cursor-animation setup; the terminal
substitute is explained in [Cursor effects](#cursor-effects-and-extra-controls).
The exact effect in an unidentified video/GUI cannot be established from it.

| His setting | Merge decision and reason |
| --- | --- |
| Separate Lazy bootstrap/config tree | Retain the existing NvChad/Lazy bootstrap; running two setups would replace plugin imports and defaults. |
| Tokyo Night via a separate colorscheme plugin | Retain Catppuccin and Base46. Space t h can select NvChad's built-in tokyonight palette; it is a palette alternative, not the exact standalone theme implementation. |
| ultimate-autopair.nvim | Retain nvim-autopairs. Two pairing engines can insert/delete the same brackets twice. |
| Mason/LSP handler-based setup | Retain the configured vim.lsp.config/enable setup and current Mason packages; his older handlers would duplicate configuration and weaken your explicit language setup. |
| Completion with only an LSP source | Retain your LSP, snippets, paths and buffer sources; replacing cmp.setup would discard these capabilities. |
| nvim-treesitter.configs setup | Adapt to your current Treesitter API. Add MATLAB to the controlled parser list; retain all 20 existing parsers. |
| Telescope 0.1.8 and separate nvim-tree setup | Retain your locked working versions and NvChad integrations; add the compatible Git-files/search keys. |
| Space f h for hidden files | Preserve Space f h for help. Space f a already finds hidden/ignored files. |
| Space e toggles the tree | Preserve Space e to focus the tree and Ctrl+n to toggle it. |
| Shift+H/L cycles buffers | Preserve native H/L viewport motions. Tab/Shift+Tab already cycle NvChad buffers. |
| Ctrl+d/u centered scrolling | Already present; keep one mapping for each. |
| Global tmux Ctrl+h/j/k/l bindings | Preserve vim-tmux-navigator, which routes these keys between editor windows and tmux panes. Unconditional tmux bindings would intercept the editor navigation. |
| Ctrl+w tmux prefix | Preserve your Ctrl+s prefix; Ctrl+w remains available for Neovim window commands. |
| Terminal Ctrl+h/j/k/l leave terminal mode | Preserve assistant/readline input. Use Ctrl+x to leave Neovim terminal input, then the existing navigation keys. |
| Alt+j/k selection moves | Use the added Visual J/K and existing Space m j/k; they avoid macOS Option-key encoding differences. |
| Four-space default indentation | Preserve project style, existing C++ two-space formatting and formatter/editorconfig rules. |
| Disable relative numbers/cursor line | Preserve current visibility settings; existing toggles remain available. |
| JetBrains Mono GUI font | Preserve the installed Nerd Font setup. A guifont option does not configure a terminal's font. |
| Disable backup/writebackup, force editable buffers, comment-continuation changes | Retain the current buffer/file safety and language behavior; these personal preferences are unrelated to the cursor effect. |
| Disable Q | Preserve Neovim's existing macro behavior. |

**You can now:** use the useful additions with your established C++ debugger,
completion, formatting, tmux and Codex workflow. The table identifies actual
collisions and the equivalent actions already available.

### Shortcut conflicts resolved in the combined setup

Space is your leader. Existing useful keys were preserved. Radley's horizontal
split shortcut would collide with your C++ source/header switch, so horizontal
split is **Space s s**, vertical split is **Space s v**, and source/header remains
**Space s h**. Rename remains **Space r a**; **Space r n** still toggles relative
numbers. Git hunk actions use **Space g ...**, because **Space h** already opens
a terminal. Moving lines uses **Space m h/j/k/l**, preserving Alt+h/v/i terminal
shortcuts. Sessions use uppercase **Space S ...**, avoiding NvChad's buffer keys.

[Back to contents](#contents)

## Maintenance, troubleshooting and verification

### Daily workflow tips

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

### Choose the right feedback loop

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

### Maintenance commands

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
Mason package release. Keep project formatter settings in the project and commit
intentional settings changes with a dated log entry below.

### Keeping settings changes documented

Every settings commit updates this file's [Change log](#change-log). Record the
date, concrete changes, reason, affected profile, shortcuts/usage, checks actually
run, and restore/compatibility notes. Use `.gitmessage` for substantial commit
bodies. Historical results should be labeled as prior recorded checks.

Enable the repository-local hook and template in each clone:

```sh
git config core.hooksPath .githooks
git config commit.template .gitmessage
```

The pre-commit hook requires a staged README.md update when Neovim, tmux,
plugin locks, profile metadata or agentic settings change. Git does not enable
hooks automatically in a fresh clone. The hook checks that this file is staged;
you still need to write a useful dated log entry. It makes no model/network call.

For an experimental change:

```sh
git switch main
git switch -c codex/improve-search
# Edit the intended settings and add a dated Change log entry in README.md.
python3 scripts/check.py
git diff
git add lua/mappings.lua README.md
git diff --cached
git commit
git push -u origin HEAD
```

Choose the actual files for your change. Review/merge into the intended profile.
Cherry-pick shared fixes to the other profile only after checking its dependencies
and keys. Keep the smaller C++ profile intentionally smaller. Do not force-push
profiles or move published checkpoint tags.

### Updating and recovering

The lockfile pins editor plugin commits. `:Lazy update` changes that lockfile;
review and commit it with the related settings changes. `:Lazy restore` restores
the selected revision's locked plugin versions. Mason packages, language SDKs,
tmux plugins, account settings and private Kun state have separate lifecycles;
switching a Git tag does not roll those back automatically.

Close Neovim before switching a checkout's branch/tag. Keep local edits by
committing them on a work branch or deliberately stashing them first. No reset,
force checkout, clean or automatic deletion is needed for ordinary version hops.

Recorded runtime evidence is in [the Verification section](#verification-results-and-practical-limits).
The repository packaging checks run without bootstrapping plugins or invoking a
model. Real first-use agent/PR behavior still needs a bounded task in your project.

### Troubleshooting by symptom

| Symptom | First useful check |
| --- | --- |
| Shortcut inserts letters | Press Esc and confirm Neovim has focus. |
| Shell command fails after a colon | Run cmake/git/npm in a terminal, not the Neovim command line. |
| Ctrl+s does not save | Ctrl+s is tmux's prefix; use :w. |
| Terminal ignores editor shortcuts | Ctrl+x leaves terminal input; i resumes it. |
| Ctrl+Arrow does not resize | macOS/terminal shortcuts may intercept it; use :resize or :vertical resize. |
| C++ headers or symbols are missing | Check compile_commands.json and :checkhealth vim.lsp. |
| Python imports look missing | Confirm the project environment and dependencies. |
| Completion is absent | Wait for the server, check filetype and :checkhealth vim.lsp. |
| Formatting fails | :ConformInfo, project style files and Space u f. |
| Breakpoint shows old code | Save, rebuild with Debug information and restart debugging. |
| Debugger cannot find the program | Build first, then choose the actual executable path. |
| First debug startup is slow | The configured macOS CodeLLDB startup allowance covers a longer first launch. |
| External edits do not appear | Check the checkout/path and :checktime; resolve unsaved edits deliberately. |
| Diff/history is empty | Check for Git commits, changes and the correct worker checkout. |
| Cursor trail is distracting | Space u c toggles it; enabled = false in configs/cursor.lua changes startup. |
| Restored layout contains shells | Expected: process replay is off; start the desired programs. |
| Kun is unavailable | Check ~/.local/bin on PATH and the installer, then kun doctor. |
| Worker is waiting | Open its tmux window for a real approval/trust prompt. |
| Need a previous warning | :messages. |

The workspace's install-time backups remain on the original machine. Git tags
are the portable restore points; account state, active processes and SDK/tool
versions have separate lifecycles.

### Verification results and practical limits

| Recorded group | Scope |
| --- | --- |
| Original C++ / merged editor / tmux | 10 + 11 + 3 checks on October 18 |
| Kun | 20 functional + 4 installed-tool checks, key/path and runtime checks |
| Cursor merge | 5 terminal checks, MATLAB parsing and Neovide-mode compatibility on October 19 |
| Documentation consolidation | Link/anchor policy, syntax and updated history-hook checks |
| Additional videos / autocommands | 5 real Neovim checks: reload, yank, fixed shell height, scope and opt-out |

The original Mac used Neovim 0.12.6 and tmux 3.8. Runtime and login observations
below are dated setup results, not promises that cloning reproduces account
authentication. No paid agent task/pipeline was used for installation checks.

#### C++ regression

- PASS: clangd attachment — ~/.local/share/nvim/mason/bin/clangd
- PASS: C++ hover — clangd resolves local symbols
- PASS: C++ completion — 26 vector member suggestions
- PASS: C++ diagnostics — unknown function detected
- PASS: completion menu — nvim-cmp LSP source loaded
- PASS: C++ syntax highlighting — C++ tree-sitter parser loaded
- PASS: format on save — clang-format reformatted a C++ buffer when written
- PASS: C++ breakpoint — CodeLLDB stopped at main.cpp:8
- PASS: debugger variables — total = 100
- PASS: debugger exit — Program resumed and exited

#### Merged workflow

- PASS: surround and moving lines — Actual mapped keystrokes add/remove quotes and move a line
- PASS: external agent edits — Saved buffers refresh; unsaved edits survive
- PASS: editor sessions — Saved and restored two editor windows; terminal replay excluded
- PASS: Python language tools — Pyright type error, Ruff attachment and real formatting
- PASS: TypeScript language tools — TypeScript type error and Prettier formatting on save
- PASS: JSON language tools — JSON language server and Prettier work
- PASS: shell diagnostics — Bash language server reports ShellCheck quoting warning
- PASS: Git hunks — A real fixture change was detected, staged, and unstaged
- PASS: side-by-side Git review — Diffview opened and closed a real working-tree diff
- PASS: parallel-task isolation — Created a real independent Git worktree and branch
- PASS: agent launchers — Three installed CLIs resolve; no model calls made during verification

#### tmux isolated server

- PASS: tmux configuration loads with preserved prefix and truecolor terminal
- PASS: split, clipboard, navigation and persistence bindings are loaded
- PASS: real two-pane layout saved; automatic process restoration disabled

#### Scope and practical limits

Runtime checks use real Neovim buffers, language-server requests, formatting, a
compiled C++ program, CodeLLDB, temporary Git repositories and a dedicated tmux
server. Diffview verification waits until both old and new file contents are
displayed in editor windows before closing its asynchronous view.

Agent command resolution was checked without sending model requests. Codex
CLI help, updated Claude Code 2.1.303 version, and OpenCode help start successfully.
GitHub and Codex login status were verified read-only. A paid agent conversation
was not exercised. No user project was pushed or changed by the fixtures.

Syntax parsing passed for every configuration Lua file. Mason packages and all
configured syntax parsers installed successfully. Plugin revisions are recorded
in lazy-lock.json. Tests were run headlessly; an interactive iTerm GUI
session was not controlled. The final inventory lists optional language SDKs and debug adapters
that are not part of the active setup. Core Kun orchestration tools are now
installed privately, with project setup deferred until the user invokes `kun`.

#### Kun project workflow

- PASS: 20 functional checks in `agentic/test_kun.py`. These cover nested project
  discovery, preserving instructions/dirty files, separate project state,
  official registry mode/prefix parsing, native mode changes, redacting remote
  credentials, candidate command detection, an actual project test command,
  no-model launch preview, harness selection, actionable Git errors, real tmux
  startup/session reuse, permission adapters, native worker-template execution
  after PATH reordering, and disabling startup sync for linked source checkouts.
- PASS: Firstmate's installed bootstrap/dependency detection accepts the real
  tool versions and generated project home.
- PASS: Treehouse leases a real isolated worktree/branch and releases it.
- PASS: No Mistakes initializes a local gate/daemon against a disposable bare
  origin; repeat setup preserves it. Fixture daemon/LaunchAgent cleaned up.
- PASS: Native Codex accepts the selected sandbox/approval/add-directory flags
  without a model request.
- PASS: Installed Neovim Space a k callback resolves the launcher, finds the
  project and quotes a path containing spaces without starting an assistant.
- PASS: All Lua configuration files parse after the new mapping/helper.
- PASS: The installed launcher and Tasks AXI work with a minimal PATH that lacks
  Homebrew Python/Node entries, using their recorded runtime paths.

Sources: `agentic/test_kun.py`, `agentic/integration.py`, `verification/kun-nvim.lua`.
Logs: `kun-tests.log`, `kun-integration.log`, `kun-nvim.log`, `kun-doctor.log`.
The tests deliberately do not submit a paid agent task, push a user project,
create a PR or merge. The first bounded real task remains the project-specific
end-to-end check. See the Kun command reference above.

Machine-readable results/logs are local ignored files beside this report.

### Packaging and cursor-merge verification

#### Repository export — October 18, 2026

The exported init.lua, Lua settings, style config and plugin lockfile match the
active configuration byte for byte. Local filesystem paths were normalized only
in copied documentation/test helpers; the editor settings were preserved.

Packaging verification passed:

- All 12 Neovim settings Lua files parse without loading plugins or agents.
- Python helper sources and JSON profile/toolchain/plugin records parse.
- A real disposable Git repository demonstrated the then-current pre-commit
  requirement for CHANGELOG.md. The consolidation subsequently migrated and
  reverified that requirement for this file, README.md.
- Repository Markdown file links resolve; the final stack remains the handbook's
  last section.
- The packaged files were checked for the original user-specific paths, private
  author email and common credential/private-key patterns. Machine installation
  records, local state, backups, binaries and transcript downloads are excluded.

The C++ and merged checkpoints come from saved milestones, as explained in
README.md. They are not represented as newly rerun full runtime suites. The
export introduced documentation/history tooling and preserved the active runtime
settings, so no additional paid agent call was made for packaging.

#### Magicalbat merge — October 19, 2026

Five additional runtime checks passed in a terminal Neovim instance:

- The real pinned cursor plugin loads with typing/terminal/command-line effects off.
- Space u c disables and re-enables it.
- Cursor movement creates smear-cursor renderer frames without changing text.
- Visual J/K move selected lines and Visual p preserves the copied register.
- Ctrl+Arrow resize works; help, tmux navigation, source/header and debugger keys survive.

The MATLAB syntax parser compiled, installed and parsed a real function without
syntax errors. A Neovide-mode launch skipped the terminal renderer. All 13 Lua settings
files and the Python/JSON records parse. Exported settings match the active files;
document links resolve. Earlier C++/language/tmux checks above are prior recorded
results, not newly rerun suites. No model calls were made. This verifies renderer
activity, not an exact visual match to an unidentified video/GUI animation.

### Additional autocommand verification — October 19, 2026

Five checks passed against the candidate module and installed NvChad terminal
implementation: reload twice without duplicated registrations; a real yank
fires one highlight callback; an actual horizontal shell keeps its height when
the code window splits; vertical/generic terminals remain unfixed; and the local
height preference can be disabled. Generic fixtures are real shell terminals,
not an end-to-end run of a particular test plugin. No model request was made.

### Kun follow-up verification — October 19, 2026

The updated launcher passed 23 functional fixtures, including three new cases:
custom object/array routing survives setup and launch preview byte for byte;
an explicit assistant change preserves rules while replacing the fallback; and
malformed/non-object JSON is reported without changing the saved project profile.
The original adapter, mode, worktree/session and project-preservation cases also
pass. Five installed-tool integration checks passed, including the preserved
Codex profile through official Firstmate bootstrap, real worktree leasing and
the local gate. A smoke test through the installed `kun` command also preserved
custom routing across setup/launch preview in a temporary Git repository.

`kun doctor` verified all shared tool commands and GitHub/Codex login state.
Bundled Ahoy/Bearings/Stow, dispatch and secondmate code were inspected for
availability; this was not a live exercise of a secondmate fleet, browser task,
public relay or paid model pipeline. The core installed integration results from
October 18 remain historical evidence where not explicitly rerun here.

### Vim learning verification — October 20, 2026

The local course’s `.learning/check.py` checks all 31 mirrored lessons, local
links, launch targets, retained progress, backed-up resets and plugin-demo edits
using a temporary course copy. Its `.learning/check.lua` runs with the installed
configuration: word edits/undo/redo, counts, jk, Space ;/comma, registers/Visual p,
macros/substitution, delimiter/text objects, cross-file marks, quickfix/pane
navigation, explorer actions, real Telescope results, unformatted ASCII saves
and the local Lua command. The 13 checks also record/replay inserted text and
confirm ordinary completion initialization still runs. Run these from the course directory:

```sh
python3 .learning/check.py
./learn plugin --print
nvim --headless -i NONE -n -c 'luafile .learning/check.lua'
```

The runtime check requires the installed plugins and existing navigation
fixtures. It is an integration check for this Mac’s full profile, not a promise
that a shortcut works without a suitable mode/file/search context. It does not
start agents or call a model. Only the changed mappings, plugin declaration and
completion module were synchronized; the independently adjusted local cursor
preset was preserved.

### Reproduce the relevant checks

From the settings clone, `python3 scripts/check.py` parses Lua/Python/JSON and
checks this document's local links/anchors without installing plugins or calling
a model. The history hook is `scripts/check_history.py`.

After installing the dependencies and configuring/building `example/`, the
deeper checks are:

```sh
cmake -S example -B example/build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build example/build
nvim --headless -i NONE -c 'luafile verification/runtime.lua'
nvim --headless -i NONE -c 'luafile verification/merge-runtime.lua'
nvim --headless -i NONE -n -c 'luafile verification/autocmd-runtime.lua'
python3 verification/tmux.py
python3 agentic/test_kun.py
python3 agentic/integration.py
nvim -i NONE -n -c 'luafile verification/magicalbat-runtime.lua'
```

Use the intended NVIM_APPNAME when testing an isolated profile. The tmux check
needs TPM/plugins; Kun integration checks need the installed toolchain and can
initialize a temporary daemon/skill as documented above. The cursor check uses
a terminal UI. Run only the checks relevant to what changed; these are not all
required for a small documentation edit. Results/logs are ignored local files.

[Back to contents](#contents)

## Change log

Each entry records changes, use, actual verification and a restore point.
The first three commits packaged saved, tested milestones on October 18, 2026;
their packaging times are not represented as original development timestamps.

### 2026-10-20 — publish the credited Vim learning template

- **Scope/profile:** course publication and documentation only. The editor
  checkpoint remains `setup-2026-10-20-vim-learning`.
- **Changed/why:** publish the annotated course to BIN0806/nvim_learning with main,
  its working branch, source snapshot tag and existing course checkpoints. Add
  portable clone/fixture instructions and bottom-of-README author/source credits;
  retain the upstream history, attribution and licenses.
- **Use:** clone the learning repository, follow its README and use ./learn.
  Navigation lessons require the separately cloned pinned playground; custom
  editor shortcuts require this full Neovim profile. Practice progress/backups
  remain local and ignored.
- **Validation:** course mirrored lessons, links, launcher/progress/reset behavior
  and whitespace checks pass. Published refs and a fresh remote checkout were
  verified.
  Settings documentation/parser checks pass; no editor mappings or plugins changed.
- **Restore:** `course-2026-10-20-published` identifies the published course;
  `course-2026-10-20-notes` retains the preceding annotated checkpoint and
  `source-vim-fundamentals-aed0a14` identifies the original course. Existing
  published settings and course tags remain unchanged.

### 2026-10-20 — show course differences and commented binding recipes

- **Scope/profile:** documentation follow-up for the full profile. The editor
  checkpoint remains `setup-2026-10-20-vim-learning`; no key mappings changed.
- **Changed/why:** add visible comments before adapted course instructions,
  separating changed behavior, existing mappings and optional unbound shortcuts.
  Include commented Lua recipes for the optional saved-Lua reload and CourseHello
  actions, plus recovery definitions for installed explorer/quickfix/find-repeat
  keys. Add an original-versus-current comparison to the course README.
- **Use:** read the callout before an instruction. A Binding needed note explains
  the command fallback and optional shortcut; copy only a recipe you want into
  the active lua/mappings.lua, uncomment its mapping lines, save and restart.
  Built-in Vim commands need no custom map. Current required course keys remain installed.
- **Validation:** 31 lesson pairs remain synchronized; course links, launcher,
  progress/reset checks and code fences pass. All seven Lua examples parse,
  including six commented binding recipes. Optional keys are unassigned in the
  installed full profile; temporary mappings successfully reload a saved Lua
  experiment and execute its command. Existing course aliases match the comments.
  Settings documentation/parser and diff-whitespace checks pass. No plugin
  or editor behavior changed; the prior 13 integration checks remain historical.
- **Restore:** the previous local course checkpoint is `course-2026-10-20-billy`;
  annotated lessons are saved separately as `course-2026-10-20-notes`. Existing
  practice edits were preserved, with the updated copy backed up first. Published
  settings tags retain their original commits.

### 2026-10-20 — adapt ThePrimeagen’s course to the installed shortcuts

- **Profile/checkpoint:** full; `setup-2026-10-20-vim-learning`.
- **Changed/why:** add Space ; for character-find repeat, ]q/[q for quickfix
  navigation, and Space q o/q c for its window. Guard nvim-cmp’s InsertEnter
  callback during macros to preserve recorded Insert-mode text. Preserve semicolon
  command entry and Ctrl+h/j/k/l pane navigation. Clone vim-fundamentals as vim under the local
  vim learning folder; adapt both lesson trees for NvChad/Lua/Lazy/Telescope and
  provide a launcher with writable exercise copies, reset backups and literal
  diagram presentation. The navigation fixture clone stays separate and ignored.
- **Use:** save and restart Neovim, then follow [Learn Vim with this setup](#learn-vim-with-this-setup).
  Launch `./learn 0` through `./learn 6`, `./learn nav`, `./learn js` or
  `./learn plugin` from the course folder; ordinary reopening retains progress.
- **Validation:** course structure/launcher checks and 13 installed-config runtime
  checks pass, including actual edits, Insert-mode macro recording/replay with
  normal completion initialization retained, quickfix results, explorer/pickers
  and a whitespace-preserving save. The macro also passes through real terminal
  input. Settings Lua/Python/JSON, README links, formatting and diff whitespace
  checked. Changed Lua files match active/source/export;
  unrelated local cursor settings remain untouched. No plugin installs or model calls.
- **Restore:** the preceding settings checkpoint is `setup-2026-10-19-dashboard`.
  Course adaptations are local commit ceeaf9c on codex/billy-keybindings;
  upstream master remains intact. Course progress/backups are ignored personal
  files and are not restored by settings tags. Existing profiles/tags are unchanged.

### 2026-10-19 — enable the home dashboard

- **Profile/checkpoint:** full; `setup-2026-10-19-dashboard`.
- **Changed/why:** enable NvChad's existing Nvdash startup screen, which had been
  left disabled. Add Space u d to open it manually; no extra dashboard plugin.
- **Use:** launch `nvim` or `nvim .`; use the dashboard's file/recent/text/theme/help
  actions. Explicit file arguments open directly. Set load_on_startup to false
  in lua/chadrc.lua to restore the previous startup preference.
- **Validation:** real empty, directory and file startup checks pass; rendered
  action labels and bindings verified, and the manual home shortcut preserves
  an open file. The five autocommand/terminal checks still pass after giving the
  fixture its own editable buffer. Lua/Python/JSON, formatting and links checked;
  dashboard settings match active/source/export copies. A separate local cursor
  adjustment is preserved outside this change. No plugin downloads or model requests.
- **Restore:** previous checkpoint `setup-2026-10-19-kun-routing`. The smaller
  C++ profile and existing checkpoint tags retain their original behavior.

### 2026-10-19 — Kun follow-up audit and persistent worker routing

- **Profile/checkpoint:** full; `setup-2026-10-19-kun-routing`.
- **Changed/why:** audit the high-throughput and full-stack videos against the
  existing original Kun workflow. Fix a launcher bug that reset worker routing
  every time a project was reopened; keep custom rules/default profiles intact.
- **Use:** reopen normally with `kun`. An explicit `--agent` changes the fallback
  and primary/pipeline while retaining task rules. Invalid JSON is preserved and
  reported before the saved project profile is changed.
- **Guide:** add per-video coverage, available versus optional fleet features,
  Codex recap invocations, routing behavior and a full-stack acceptance checklist.
  Kun remains Codex/tmux by default; no extra subscription, fleet or relay enabled.
- **Validation:** 23 functional checks; five installed-tool integrations and an
  installed-command routing smoke test; doctor tool/login checks;
  Python/JSON/Lua syntax, README navigation and installed/source launcher parity.
  No model calls. New transcripts unavailable; evidence limits recorded above.
- **Restore:** preceding checkpoint `setup-2026-10-19-videos`. An already-running
  primary keeps its current state; the updated launcher applies on the next open.
  Config Git rollback does not revert separately installed launcher/private state.

### 2026-10-19 — additional tutorials and agent-tool comparison

- **Profile/checkpoint:** full; `setup-2026-10-19-videos`.
- **Changed/why:** follow the additional typecraft and Courter material without
  duplicating existing editor components. Add fixed height for NvChad horizontal
  terminals and descriptions for local autocommands. Keep rule reloads grouped.
- **Use:** Space h opens the bottom shell; split code above it without shrinking
  that shell. `:setlocal nowinfixheight` opts an individual window out. New guide
  sections explain inspecting, creating, disabling and restoring rules.
- **Comparison:** Herdr is a potential tmux replacement beneath Firstmate;
  Lotus is a separate assistant/local inference option. Both remain optional
  and uninstalled. The Kun launcher still selects tmux and Codex.
- **Evidence:** three video links were repeats. New caption/transcript retrieval
  failed; descriptions/chapters, Courter example frames, author repositories and
  pinned Firstmate sources were reviewed, with the limits recorded above.
- **Validation:** five actual Neovim autocommand/terminal checks pass; settings
  Lua, Python/JSON and local document navigation checked. Active/source/export
  settings match. No new plugin installation or model request.
- **Restore:** `setup-2026-10-19-readme` is the preceding tagged profile; Git parent
  57ba83e includes the later credits-only change. Existing profile history is kept.

### 2026-10-19 — source credits at the bottom of the README

- **Profile:** full; documentation only.
- **Changed/why:** add a concise list of the tutorial/configuration authors and
  cursor-plugin author at the bottom, with their YouTube/GitHub names and links.
  Move the existing license note there and link the section from Contents.
- **Use:** follow Sources and credits to find the original creators; detailed
  contributions and substitutions remain in Tutorial sources and merge decisions.
- **Validation:** recorded video-author names checked; document links/anchors,
  single-guide policy, Python/JSON and Lua syntax checks pass.
- **Restore:** `setup-2026-10-19-readme` is the preceding tagged snapshot. Settings
  and shortcuts are unchanged.

### 2026-10-19 — display the guide on the GitHub homepage

- **Profile/checkpoint:** full; `setup-2026-10-19-readme`.
- **Changed/why:** rename Documentation.md to README.md so GitHub shows the
  complete categorized guide on the repository homepage. Keep the same content
  and navigation, with a dated entry for this rename.
- **Use:** open the repository homepage or README.md. Future settings changes
  update the Change log in README.md; the hook, commit template, agent pointers
  and missing-Kun help now refer to that filename.
- **Validation:** document links/anchors and single-guide policy; Python/JSON and
  all 13 Lua files parse; history hook tested with staged settings and README.md;
  active/source/export helper parity checked. No model request.
- **Restore:** `setup-2026-10-19-documentation` keeps the previous filename.
  Editor features, shortcuts and older profile/tag history are preserved.

### 2026-10-19 — one categorized Documentation.md

- **Profile/checkpoint:** full; `setup-2026-10-19-documentation`.
- **Changed:** consolidate the beginner guide, handbook, source/merge notes,
  cursor guide, Kun guide, profiles, test report and change log into this file.
  Keep one explanation per topic and a task-oriented contents table; embed the
  project context template here. Remove superseded user guides from main.
- **Use:** start with Quick start or follow a category link. Future changes add
  their dated entry to the Change log here; the separate CHANGELOG.md is retired.
- **Integration:** update the pre-commit hook, commit template, agent pointers
  and missing-Kun help message to refer here. The local workspace links to this
  same document. Historical profile branches/tags keep their original files.
- **Validation:** local file/anchor links, unique headings and documentation
  policy checked; history hook tested with real staged changes; Lua/Python/JSON
  parse; active/source/export helper parity checked. No agent/model call.
- **Restore:** `setup-2026-10-19-cursor` is the preceding full profile. Editor
  features and shortcuts are unchanged by this consolidation.

### 2026-10-19 — Magicalbat merge and cursor animation

- **Profile/checkpoint:** full; `setup-2026-10-19-cursor`. The smaller C++ branch stays unchanged.
- **Source reviewed:** Magicalbat/Configs at `14e1f6c5821f9c15e1805f1dc929c227c484d9ae`.
  That source contains no cursor-animation configuration; the requested effect
  is supplied with a documented terminal substitute, smear-cursor.nvim, locked
  at `f6cb57c342268177f719acc3968b9d8de3ecc969`.
- **Added:** Space u c cursor-trail toggle; Ctrl+Arrow resize; Visual J/K line
  moves and register-preserving p; Git-file/search shortcuts; F2/F4 LSP aliases;
  MATLAB syntax parser, without a MATLAB SDK/server/debugger.
- **Compatibility:** retain NvChad/Catppuccin, current LSP/Treesitter APIs,
  nvim-autopairs, completion sources, help key, debugger and Ctrl+s tmux workflow.
  Cursor animation is quiet during typing/terminal/command-line use and selected
  tool buffers; it skips Neovide. Full decisions are in the Magicalbat conflicts section.
- **Validation:** five real Neovim runtime checks passed (including renderer
  frames, toggle, text/register behavior and surviving keys); MATLAB parser
  compiles/loads; Lua/Python/JSON syntax and document-link checks pass. No model
  request or application-project changes were made.
- **Restore:** `setup-2026-10-18-full` is the previous full setup. Space u c
  disables animation immediately; `enabled = false` in configs/cursor.lua sets
  the startup preference. A pre-change backup is preserved on the original machine.

### 2026-10-18 — full profile and project-scoped Codex workflow

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
  opt-in pre-commit log enforcement, annotated checkpoints and this document’s Profiles section.
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

### 2026-10-18 — combined editor and tmux

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

### 2026-10-18 — cpp foundation

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

[Back to contents](#contents)

## Project context template

Copy the template below into the project's appropriate instruction/context file
after replacing the placeholders. It is not automatically loaded by every
assistant; explicitly ask the assistant to read it. Keep facts concise and
commands verified. A task plan, reusable skill and project context have different
jobs, so avoid turning this into an unstructured transcript dump.

```markdown
# Project context template

Copy and adapt this into the project's appropriate instruction file only after
replacing placeholders. This template is not automatically loaded by an agent.

## Purpose

What this application does and who uses it.

## Map

- Main source locations:
- Entry point:
- Tests:
- Generated files that should not be hand-edited:

## Commands verified in this repository

- Install dependencies:
- Start development app:
- Build:
- Type check / lint:
- Relevant tests:
- End-to-end verification:

## Conventions

Language/runtime versions, formatting, compatibility requirements and important
architectural constraints. Prefer a few accurate facts over a long generic list.

## Working agreement

- Reproduce reported behavior before making a fix.
- Keep a task's edits focused and explain product tradeoffs when they arise.
- Validate the intended behavior and report exact commands and results.
- Summarize changed files, limitations and next steps at handoff.

## Learned project facts

Add concise, verified lessons that would otherwise need to be rediscovered.
Move long conditional procedures into separately scoped documentation or a
reviewed skill instead of loading them into every conversation.
```

[Back to contents](#contents)

## Final installed stack

Versions below are the reviewed installation records. Fresh clones need their own
package installation and account sign-in; the original Mac's private tools/state
are not part of this repository.

The inventory covers the usable combined setup. `lazy-lock.json` records exact
editor plugin commits; optional tools are identified separately below.

### Foundation and interface

| Layer | Selected tools / configuration | Purpose |
| --- | --- | --- |
| Editor | Neovim 0.12.6 | Editing engine and native LSP APIs. |
| Distribution | NvChad v2.5 | Coherent defaults, statusline, buffer line and terminal UI. |
| Home screen | Built-in NvChad Nvdash | Startup menu and Space u d; explicit file launches open directly. |
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
| Local event rules | Described, grouped autocommands; NvChad horizontal terminals preserve height |

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
| Worker routing | Private crew-dispatch.json preserved on reopening; explicit assistant selection updates its fallback |
| Fleet context | Built-in Firstmate Bearings, Ahoy and Stow available; usage above |
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
No paid worker pipeline has been run during installation. Herdr and Lotus were
compared as optional tools; neither is installed or required by this profile.

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

### Current profile files and installed tool locations

| Item | Where to find it |
| --- | --- |
| This guide and change log | README.md in the settings repository |
| Neovim configuration | init.lua, lua/, lazy-lock.json and .stylua.toml |
| Profile metadata | profile.json |
| Optional tmux settings | tmux.conf, installed separately as ~/.tmux.conf |
| Cursor settings | lua/configs/cursor.lua |
| Completion macro compatibility | lua/configs/completion.lua |
| Optional Kun sources | agentic/; reviewed versions in agentic/toolchain-lock.json |
| Installed Kun command | ~/.local/bin/kun |
| Private Kun tools and state | ~/.local/share/kun |
| Practice project | example/ |
| Vim learning course | [nvim_learning](https://github.com/BIN0806/nvim_learning); course-2026-10-20-published |
| Current full-profile checkpoint | setup-2026-10-20-vim-learning |

Installed language/debug/CLI versions above describe the reviewed setup. Plugin
commits are locked; separately managed SDKs, accounts and private state are not
rolled back by selecting a config tag. This file is the maintained user-facing
documentation; AGENTS.md is a brief repository instruction pointer.

### Sources and credits

- [ThePrimeagen](https://github.com/ThePrimeagen/vim-fundamentals) — Vim fundamentals course and [navigation playground](https://github.com/ThePrimeagen/vim-nav-playground)
- [Dreams of Code](https://www.youtube.com/watch?v=lsFoZIg-oDs) / [dreamsofcode-io](https://github.com/dreamsofcode-io/neovim-cpp)
- [Average Neovim Enjoyer](https://www.youtube.com/watch?v=w0WzxUPtKf0)
- [The Rad Lectures](https://www.youtube.com/watch?v=lljs_7xB7Ps) / [radleylewis](https://github.com/radleylewis/nvim-lite)
- [Mental Outlaw](https://www.youtube.com/watch?v=yW3ovyQCwpw)
- [Andrew Courter](https://www.youtube.com/watch?v=xUnXcVxcJho) / [exosyphon](https://github.com/exosyphon/dotfiles)
- [Kun Chen](https://www.youtube.com/watch?v=iQyg-KypKAA) / [kunchenguid](https://github.com/kunchenguid/firstmate) — also [high-throughput workflow](https://www.youtube.com/watch?v=MSbacZ99E14) and [full-stack build](https://www.youtube.com/watch?v=kPN564Kol14)
- [typecraft](https://www.youtube.com/watch?v=J9yqSdvAKXY) / [cpow](https://github.com/cpow/cpow-dotfiles)
- [Magicalbat](https://github.com/Magicalbat/Configs)
- [sphamba](https://github.com/sphamba/smear-cursor.nvim) — cursor-animation plugin

Additional comparison sources (tools left optional):

- [Jilles](https://www.youtube.com/watch?v=qnIu-Xu64H0) — Herdr
- [Fanxy](https://www.youtube.com/watch?v=WZ9SPo_rnVU) / [Fanxy13](https://github.com/Fanxy13/homebrew-lotus) — Lotus

The NvChad starter's original public-domain license is retained. Plugin and
external-tool licenses remain with their projects; installed dependencies are
not vendored here. Captions, personal transcripts, credentials and machine
backups are not uploaded.
