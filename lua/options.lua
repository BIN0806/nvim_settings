require "nvchad.options"

vim.opt.termguicolors = true
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.scrolloff = 8
vim.opt.updatetime = 250
vim.opt.signcolumn = "yes"
vim.opt.splitright = true
vim.opt.splitbelow = true
vim.opt.undofile = true
vim.opt.autoread = true
vim.opt.ignorecase = true
vim.opt.smartcase = true
vim.opt.inccommand = "split"
vim.opt.breakindent = true
vim.opt.cursorline = true
vim.opt.foldmethod = "expr"
vim.opt.foldexpr = "v:lua.vim.treesitter.foldexpr()"
vim.opt.foldlevelstart = 99
vim.opt.diffopt:append { "linematch:60", "algorithm:histogram" }
-- Layouts are saved on request. Restoring a layout must not relaunch an agent.
vim.opt.sessionoptions = { "buffers", "curdir", "tabpages", "winsize", "help", "folds" }
