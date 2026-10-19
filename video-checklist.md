# Comparison with the tutorial transcript

> Repository edition: examples assume a clone at `~/.config/nvim-billy`.
> Run it with `NVIM_APPNAME=nvim-billy nvim`; see README.md and PROFILES.md.

Source: [Dreams of Code, “The perfect Neovim setup for C++”](https://www.youtube.com/watch?v=lsFoZIg-oDs),
published July 11, 2023. Instructions were extracted from YouTube's English
auto-generated transcript and checked against the author's repository.

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
| 15:45–16:28 | Build with debug symbols in an NvChad terminal | Space h opens terminal; example builds with CMake Debug. Direct clang++ example below follows his terminal workflow. |
| 16:30–17:07 | Set a breakpoint, select executable, inspect and control execution | CodeLLDB launch prompt and UI; actual breakpoint, variable evaluation, resume and exit checked. |

To use the simple single-file build shown near the end of the video:

```sh
cd ~/.config/nvim-billy/example
nvim src/main.cpp
```

Press Space h, then run:

```sh
mkdir -p build
clang++ -std=c++23 -g -O0 src/main.cpp -o build/main
```

Press Ctrl+x to leave Terminal mode, then `:q`. Set a breakpoint with Space d b,
start with Space d r, and enter the full path to `example/build/main`.

Modernization references: [NvChad](https://nvchad.com/docs/quickstart/install/),
[LSP configuration migration](https://github.com/neovim/nvim-lspconfig),
[Conform](https://github.com/stevearc/conform.nvim),
[mason-nvim-dap](https://github.com/jay-babu/mason-nvim-dap.nvim),
[nvim-dap-ui dependencies](https://github.com/rcarriga/nvim-dap-ui).
