require "nvchad.autocmds"

vim.api.nvim_create_autocmd("FileType", {
  group = vim.api.nvim_create_augroup("CppIndent", { clear = true }),
  pattern = { "c", "cpp" },
  callback = function()
    vim.opt_local.expandtab = true
    vim.opt_local.shiftwidth = 2
    vim.opt_local.tabstop = 2
  end,
})
