# Magicalbat settings and cursor merge — October 19, 2026

Reviewed [Magicalbat/Configs](https://github.com/Magicalbat/Configs) at commit
`14e1f6c5821f9c15e1805f1dc929c227c484d9ae`, including all published Neovim Lua
files and tmux settings. Your existing full NvChad profile remains the base.

## The flying cursor

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

## Added shortcuts and language syntax

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

## Conflicts and retained equivalents

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

## Verification, history and restoration

The runtime check exercises actual plugin setup/toggling, cursor-renderer frames
without text changes, selected-line movement, register-preserving paste and split
resizing. It checks that help, tmux navigation, C++ source/header and debugger keys
survive. MATLAB's parser is installed and loaded through the current API. The
repository check parses the updated Lua/Python and JSON records.

The new full-profile checkpoint is `setup-2026-10-19-cursor`. The C++ profile
branch stays on its smaller setup. CHANGELOG.md records this merge in its commit.
To inspect the exact previous full profile, use `setup-2026-10-18-full` and the
profile instructions in [PROFILES.md](PROFILES.md). Restoring an older config
does not uninstall external tools or erase private assistant state.

The original machine also has a local pre-change backup. Backups and downloaded
plugin source are excluded from this repository. Source configs were reviewed
and adapted; their complete files were not copied over your NvChad bootstrap.
