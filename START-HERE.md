# Your Neovim setup: a beginner's working guide

> Repository edition: examples assume a clone at `~/.config/nvim-billy`.
> Run it with `NVIM_APPNAME=nvim-billy nvim`; see README.md and PROFILES.md.

For the complete single-file reference, use [NVIM-HANDBOOK.md](NVIM-HANDBOOK.md):
all six videos, integrated coding instructions, and the final stack inventory.

You can use this guide without watching the tutorial. It describes what is
installed on your Mac and how to use it. When we change this setup, the explanation
should cover what changed, what it lets you do, how to use it, and what was checked.

The five-video merge is now installed too. After the basics below, continue with
[the combined workflow guide](MERGED-WORKFLOW.md) for surround/block editing, more
languages, Git review, saved layouts, tmux, coding assistants and isolated tasks.
[The video comparison](MERGE-NOTES.md) explains substitutions, optional tools and
the transcript scraping limitations.

**1. Understand the four actions in a C++ workflow.**

Editing changes your source files, such as `main.cpp`. Saving writes those changes
to disk and runs the formatter. Building compiles the saved source into an
executable program. Running executes that program; debugging runs it with the
ability to pause and inspect it.

Your normal loop is **edit → save → build → run or debug**. Saving does not build
your program. After changing C++ code, build again before running or debugging so
you are testing the current version.

Neovim is the editor. NvChad supplies the interface and common editing tools.
Clangd understands C/C++ code. Clang-format arranges its spacing and layout.
CodeLLDB runs your program under the debugger. Mason installs those tools. You
mostly interact with their shortcuts and menus, rather than their package names.

You can now edit, understand, format, compile, run, and debug C/C++ from one editor.

**2. Learn how to type commands without accidentally editing code.**

Neovim has modes. In Normal mode, keys perform actions. Press `i` to enter Insert
mode, where keys type text. Press `Esc` to return to Normal mode. You can also type
`jk` quickly to leave Insert mode in your configuration.

Most shortcuts in this guide start in Normal mode. Press `Esc` first if unsure.
`Space f f` means press Space, then f, then f; it is a sequence, not three keys held
together. `Ctrl+n` means hold Control and press n. A capital letter means Shift is
needed: `K` means Shift+k, and the final `O` in `Space d O` is uppercase.

Colon commands start with `:` and finish with Enter. For example, `:w` means type
colon, w, then Enter. Shell commands such as `cmake` belong in a terminal, not in
Neovim's colon command line.

| Action | Keys in Normal mode |
| --- | --- |
| Start typing | `i` |
| Insert a new line below and start typing | `o` |
| Stop typing and return to Normal mode | `Esc` |
| Save the current file | `:w`, then Enter |
| Save and close the current window | `:wq`, then Enter |
| Close the current window | `:q`, then Enter; save first if prompted |
| Quit all windows | `:qa`, then Enter; save first if prompted |
| Undo an edit | `u` |
| Redo an edit | `Ctrl+r` |
| Copy the current line inside Neovim | `yy` |
| Paste the copied line below | `p` |
| Select characters / whole lines | `v` / `V`, then move the cursor |
| Comment or uncomment a line / selected lines | `Space /` |

Arrow keys work. You can gradually learn h/j/k/l for left/down/up/right, `w` for
the next word, `b` for the previous word, `gg` for the start of a file, and `G` for
the end. Relative line numbers help with motions such as `5j`, meaning move down
five lines. You do not need to memorize all of these before starting.

You can now type, save, undo, navigate, and exit confidently.

**3. Open a project and find the files you need.**

First save any work in your existing Neovim session, quit, and reopen it to load
the new configuration. Try the example from your ordinary terminal:

```sh
cd ~/.config/nvim-billy/example
nvim src/main.cpp
```

For your own project, `cd` into its main directory first, then run `nvim .` or
`nvim path/to/file.cpp`. The main directory usually contains `CMakeLists.txt` or
the `.git` directory. Starting there makes project search, builds, and debugger
paths easier to understand.

| What you want | Shortcut | How to use it |
| --- | --- | --- |
| Browse folders and files | `Ctrl+n` | Move with arrows or j/k; Enter opens a file or expands a folder. |
| Focus the file explorer | `Space e` | Moves your cursor into the explorer. |
| Find a file by its name | `Space f f` | Type part of the name, select a result, press Enter. |
| Search text across the project | `Space f w` | Type the text, select a matching line, press Enter. |
| Find text within the current file | `/text`, Enter | `n` goes to the next match; `N` goes backward. |
| List open files | `Space f b` | Choose the file you want to return to. |
| Move between open files | `Tab` / `Shift+Tab` | Use in Normal mode. |
| Close an open file buffer | Save, then `Space x` | Other open files remain available. |

In a search picker, arrow keys select results and Esc closes it. A fuzzy file
search accepts fragments of a filename; you do not have to type its complete
path. Text search normally respects ignored files, so build output may be absent
from search results.

A **buffer** holds an open file in memory. A **window** is an area displaying a
buffer. Two windows can show the same file. A **tmux pane** is a separate terminal
area outside Neovim; tmux is optional for this editing workflow.

You can now jump around a project without closing and reopening the editor.

**4. Let C++ completion and diagnostics help you write code.**

In Insert mode, suggestions appear as you type. For example, after a vector
variable and a dot, the menu can offer member functions. Use Tab/Shift+Tab to
choose an entry and Enter to accept it. Ctrl+e closes the completion menu.
Ctrl+Space requests completion if the terminal delivers that shortcut; your Mac
may reserve it for input-source switching. Automatic suggestions still work.

Snippets can insert reusable code patterns. When a snippet has editable
placeholders, Tab can move through them. Paired brackets and quotes are inserted
automatically while typing. Syntax highlighting gives different kinds of code
different colors.

Clangd also reports errors and warnings while you edit. These are called
**diagnostics**. They can catch problems before you build, although a successful
build and appropriate tests remain necessary.

| What you want | Keys in Normal mode |
| --- | --- |
| Read documentation or type information at the cursor | `K` |
| Jump to a symbol's definition | `g d` |
| Jump back after following code | `Ctrl+o` |
| Find uses of a symbol | `g r` |
| Rename a symbol through the language server | `Space r a` |
| Ask for available fixes or refactorings | `Space c a` |
| Show the current file's diagnostic list | `Space d s` |
| Show a diagnostic at the cursor | `Ctrl+w`, then `d` |
| Switch between a C/C++ source file and its header | `Space s h` |

Rename understands symbols; it can update uses across the project. Check the
result and save affected files. Code actions depend on what clangd can offer at
your cursor; some locations have no available actions. Source/header switching
requires a counterpart clangd can find.

For a real CMake project, generate its compilation database as described below.
That tells clangd the actual include directories, compiler options, and C++
standard. Missing build information can cause errors about headers that do exist.

You can now explore unfamiliar code, follow definitions, inspect types, find uses,
and apply language-aware edits.

**5. Save code with consistent formatting.**

When you save C, C++, or Lua files, the configured formatter runs automatically.
For C/C++, clang-format uses the project's `.clang-format` file. The example uses
Google style with two-space indentation. A different project can choose its own
style without changing your editor configuration.

`Space f m` formats immediately. `Space u f` turns automatic formatting off or on
for the current buffer. This toggle lasts for that buffer's lifetime. It does not
prevent explicit formatting with `Space f m`.

Formatting changes layout. It does not compile your program or fix its logic.
During normal work, simply save with `:w` and let the formatter handle spacing.

You can now keep code consistently formatted without repeatedly arranging it by
hand.

**6. Build and run the example inside Neovim.**

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

**7. Debug a program by pausing it and inspecting values.**

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
Step over is usually the best first choice while learning; step into can take you
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

**8. Arrange your workspace and use the built-in helpers.**

Use `:vsplit` for two side-by-side views of the current file or `:split` for a view
above/below it. Ctrl+h/j/k/l moves left/down/up/right between windows in Normal
mode. For example, keep a header on one side and its implementation on the other,
or keep code above a build terminal.

Your tmux navigation plugin also connects those keys with neighboring tmux panes.
Your existing tmux prefix is Ctrl+s, so it can intercept Neovim's Ctrl+s save
shortcut. Use `:w` reliably in either environment. Tmux is not required to use the
rest of this setup.

Catppuccin is the current color theme. `Space t h` opens the theme selector. Git
signs in a tracked file's margin identify changed lines. `Space g t` opens Git
status through the picker, and `Space c m` opens commit history. These views help
you review changes; saving a file does not create a Git commit.

Press Space and pause to see available shortcuts. `Space c h` opens NvChad's
cheat sheet, and `Space f h` searches help pages. `:help` opens Neovim's built-in
manual. You can learn a few motions at a time.

You can now keep related files and terminal output visible while finding help as
you work.

**9. Recognize common problems and check the right place.**

| What you see | What to check |
| --- | --- |
| A shortcut types letters into the file | Press Esc first; you were probably in Insert mode. |
| A command such as `cmake` is not understood after `:` | Run shell commands in a terminal opened with Space h. |
| C++ headers or symbols appear missing | Configure the project with compilation database export enabled; inspect `:checkhealth vim.lsp`. |
| Suggestions do not appear | Confirm you are editing a C/C++ file, wait for clangd to start, and inspect `:checkhealth vim.lsp`. |
| Formatting does not run | Inspect `:ConformInfo`; check whether Space u f disabled it for this buffer. |
| The debugger cannot find the program | Build it first and select the executable path, such as `build/app`. |
| Breakpoints do not match your edits | Save, rebuild with Debug information, and restart the debug session. |
| Debugging is unexpectedly slow to start | The first CodeLLDB startup on macOS can take longer; the setup allows additional startup time. |
| You need to see previous editor messages | Run `:messages`. |

`:Lazy` manages editor plugins. `:Mason` manages external language tools and the
debugger. `:TSUpdate` updates syntax parsers. You do not need to run updates every
time you open Neovim. When you choose to update, restart and try a small C++ file
and a debug session afterward.

C and C++ have the full completion/diagnostics/debugging workflow described here.
Lua has language help and automatic formatting for editing your configuration.
Python now has Pyright and Ruff; JavaScript/TypeScript has the TypeScript language
server and Prettier; Bash/sh has Bash language server, ShellCheck and shfmt; JSON
has a language server and Prettier. More files have syntax highlighting and
formatting. See MERGED-WORKFLOW.md for the exact coverage and project prerequisites.

You can now distinguish an editor-mode problem, a build problem, and a tooling
problem instead of treating every symptom as a broken Neovim installation.

**10. Put the pieces together in a daily routine.**

1. Open a terminal in the project's main directory, then start Neovim.
2. Find the file with Space f f, or browse with Ctrl+n.
3. Read unfamiliar code with K, g d, and g r; Ctrl+o returns from a jump.
4. Enter Insert mode with i and edit. Use completion rather than retyping long names.
5. Press Esc and save with :w. Formatting runs automatically.
6. Look at diagnostics, then use Space c a when an appropriate fix is available.
7. Open a terminal with Space h and rebuild. Fix compilation failures before running.
8. Run the executable for a quick check, or use Space d b and Space d r to investigate behavior.
9. At a breakpoint, inspect variables and step over lines. Continue or stop when finished.
10. Save affected files and review Git changes before committing through your usual Git workflow.

Start with five habits: **Esc, i, :w, Space f f, Space h**. Add **g d, K,
Space d b, Space d r, and Space d o** as you begin exploring and debugging.
This smaller set is enough for productive C++ practice.

**11. Keep this capability recap nearby.**

| Capability | What you can now do | Useful starting action |
| --- | --- | --- |
| Project navigation | Find files and search code across the project. | Space f f / Space f w |
| Efficient editing | Switch modes, undo/redo, comment selections, and reuse snippets. | i, Esc, u, Space / |
| C++ completion | Discover members, functions, and symbols as you type. | Type in Insert mode; Tab then Enter |
| Code understanding | Read documentation, follow definitions, find references, and rename symbols. | K, g d, g r, Space r a |
| Early feedback | Inspect clangd errors/warnings and available fixes. | Space d s / Space c a |
| Consistent formatting | Format on save using the project's chosen style. | :w / Space f m |
| Building and running | Compile saved C++ code and run the resulting executable. | Space h, then build/run commands |
| Debugging | Pause at breakpoints, inspect values, step through code, and examine calls. | Space d b / Space d r |
| Workspace layout | Keep related files, code, and terminal output visible together. | :vsplit / Ctrl+h/j/k/l |
| Git awareness | See changed lines and inspect status/history. | Space g t / Space c m |
| Git review | Inspect side-by-side changes, stage hunks, and use LazyGit. | Space g v / Space g s / Space g g |
| Saved layouts | Save and restore editor files/splits manually. | Space S s / Space S r |
| Kun project workflow | Open Firstmate with Codex and isolated workers. | Space a k / terminal: kun |
| Coding assistants | Open Codex, Claude Code or OpenCode beside your code. | Space a a |
| Parallel tasks | Create/list independent Git worktrees. | Space a w / Space a l |
| Discovery and maintenance | Find shortcuts/help and inspect installed tools. | Space, Space f h, :Lazy, :Mason |

The setup was checked with a real C++23 example: building and running it,
requesting completion and diagnostics, formatting on save, hitting a CodeLLDB
breakpoint, reading `total = 100`, and continuing to program exit all passed.

This repository's root is your configuration. README.md explains installation
and updates; PROFILES.md explains profile/version restoration; the timestamped
C++ tutorial comparison is in video-checklist.md. The documented example path
assumes a clone at ~/.config/nvim-billy.
