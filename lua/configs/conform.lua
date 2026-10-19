return {
  formatters_by_ft = {
    c = { "clang_format" },
    cpp = { "clang_format" },
    lua = { "stylua" },
  },
  formatters = {
    clang_format = { command = require("configs.tools").find "clang-format" },
  },
  -- clang-format discovers the project's .clang-format using the buffer's path.
  format_on_save = function(bufnr)
    if vim.b[bufnr].disable_autoformat or vim.g.disable_autoformat then
      return
    end
    local ft = vim.bo[bufnr].filetype
    if ft == "c" or ft == "cpp" or ft == "lua" then
      return { timeout_ms = 2000, lsp_format = "fallback" }
    end
  end,
}
