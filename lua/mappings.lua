require "nvchad.mappings"

local map = vim.keymap.set

map("n", ";", ":", { desc = "Enter command mode" })
map("i", "jk", "<Esc>", { desc = "Leave insert mode" })

map("n", "<C-h>", "<cmd>TmuxNavigateLeft<CR>", { desc = "Window / tmux left" })
map("n", "<C-j>", "<cmd>TmuxNavigateDown<CR>", { desc = "Window / tmux down" })
map("n", "<C-k>", "<cmd>TmuxNavigateUp<CR>", { desc = "Window / tmux up" })
map("n", "<C-l>", "<cmd>TmuxNavigateRight<CR>", { desc = "Window / tmux right" })

map("n", "K", vim.lsp.buf.hover, { desc = "LSP documentation" })
map("n", "gr", vim.lsp.buf.references, { desc = "LSP references" })
map({ "n", "v" }, "<leader>ca", vim.lsp.buf.code_action, { desc = "LSP code action" })
map("n", "<leader>sh", function()
  local bufnr = vim.api.nvim_get_current_buf()
  local client = vim.lsp.get_clients({ bufnr = bufnr, name = "clangd" })[1]
  if not client then
    return vim.notify("clangd is not attached to this file", vim.log.levels.WARN)
  end
  client:request("textDocument/switchSourceHeader", vim.lsp.util.make_text_document_params(), function(err, result)
    if err then
      return vim.notify(err.message, vim.log.levels.ERROR)
    end
    if result and result ~= "" then
      vim.cmd.edit(vim.uri_to_fname(result))
    end
  end, bufnr)
end, { desc = "C++ switch source / header" })

map("n", "<leader>uf", function()
  vim.b.disable_autoformat = not vim.b.disable_autoformat
  vim.notify("Format on save: " .. (vim.b.disable_autoformat and "off" or "on"))
end, { desc = "Toggle format on save for buffer" })
map("n", "<leader>ud", "<cmd>Nvdash<CR>", { desc = "Open home dashboard" })

for lhs, rhs in pairs { ["<C-d>"] = "<C-d>zz", ["<C-u>"] = "<C-u>zz", n = "nzzzv", N = "Nzzzv" } do
  map("n", lhs, rhs, { desc = "Navigate and center view" })
end
map("n", "<Esc>", "<cmd>nohlsearch<CR>", { desc = "Clear search highlight" })
map("n", "<leader>sv", "<cmd>vsplit<CR>", { desc = "Split vertically" })
map("n", "<leader>ss", "<cmd>split<CR>", { desc = "Split horizontally" })
map("n", "<leader>Ss", function()
  vim.ui.input(
    { prompt = "Save layout as: ", default = vim.fs.basename(require("configs.workspace").root()) },
    function(name)
      if name and name:match "^[%w_.-]+$" then
        require("mini.sessions").write(name)
      end
    end
  )
end, { desc = "Save editor session" })
map("n", "<leader>Sr", function()
  require("mini.sessions").select "read"
end, { desc = "Restore editor session" })
map("n", "<leader>Sd", function()
  require("mini.sessions").select "delete"
end, { desc = "Delete saved session" })
map("n", "<leader>z", "<cmd>ZenMode<CR>", { desc = "Toggle focus view" })

map("n", "]h", function()
  require("gitsigns").nav_hunk "next"
end, { desc = "Next Git hunk" })
map("n", "[h", function()
  require("gitsigns").nav_hunk "prev"
end, { desc = "Previous Git hunk" })
map("n", "<leader>gp", function()
  require("gitsigns").preview_hunk()
end, { desc = "Preview Git hunk" })
map("n", "<leader>gs", function()
  require("gitsigns").stage_hunk()
end, { desc = "Stage / unstage Git hunk" })
map("n", "<leader>gu", function()
  require("gitsigns").reset_buffer_index()
end, { desc = "Unstage current file" })
map("n", "<leader>gb", function()
  require("gitsigns").blame_line { full = true }
end, { desc = "Git blame line" })
map("n", "<leader>gg", function()
  require("configs.workspace").lazygit()
end, { desc = "Open LazyGit" })
map("n", "<leader>gv", "<cmd>DiffviewOpen<CR>", { desc = "Review working-tree diff" })
map("n", "<leader>gq", "<cmd>DiffviewClose<CR>", { desc = "Close diff review" })
map("n", "<leader>gH", "<cmd>DiffviewFileHistory %<CR>", { desc = "Current file Git history" })

map("n", "<leader>aa", function()
  require("configs.workspace").agent()
end, { desc = "Choose coding agent" })
map("n", "<leader>ak", function()
  require("configs.workspace").kun()
end, { desc = "Open Kun project workflow (Codex)" })
map("n", "<leader>ac", function()
  require("configs.workspace").agent "Codex"
end, { desc = "Open Codex" })
map("n", "<leader>aC", function()
  require("configs.workspace").agent "Claude"
end, { desc = "Open Claude Code" })
map("n", "<leader>ao", function()
  require("configs.workspace").agent "OpenCode"
end, { desc = "Open OpenCode" })
map("n", "<leader>at", function()
  require("configs.workspace").task_note()
end, { desc = "Open project task note" })
map("n", "<leader>aw", function()
  require("configs.workspace").new_worktree()
end, { desc = "Create isolated Git worktree" })
map("n", "<leader>al", function()
  require("configs.workspace").worktrees()
end, { desc = "List Git worktrees" })

-- Compatible Magicalbat shortcuts; retain NvChad/tmux navigation and discovery.
map("n", "<C-Up>", "<cmd>resize +1<CR>", { desc = "Increase window height" })
map("n", "<C-Down>", "<cmd>resize -1<CR>", { desc = "Decrease window height" })
map("n", "<C-Left>", "<cmd>vertical resize -1<CR>", { desc = "Decrease window width" })
map("n", "<C-Right>", "<cmd>vertical resize +1<CR>", { desc = "Increase window width" })
map("x", "J", ":move '>+1<CR>gv=gv", { desc = "Move selected lines down" })
map("x", "K", ":move '<-2<CR>gv=gv", { desc = "Move selected lines up" })
map("x", "p", '"_dP', { desc = "Paste selection without replacing copied text" })
map("n", "<leader>fg", "<cmd>Telescope git_files<CR>", { desc = "Find Git-tracked files" })
map("n", "<leader>fr", "<cmd>Telescope live_grep<CR>", { desc = "Search project text (alias)" })
map("n", "<F2>", vim.lsp.buf.rename, { desc = "LSP rename symbol" })
map("n", "<F4>", vim.lsp.buf.code_action, { desc = "LSP code action" })
