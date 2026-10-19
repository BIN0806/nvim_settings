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
