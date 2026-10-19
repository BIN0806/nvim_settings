return {
  formatters_by_ft = {
    c = { "clang_format" },
    cpp = { "clang_format" },
    lua = { "stylua" },
    python = { "ruff_format" },
    javascript = { "prettier" },
    javascriptreact = { "prettier" },
    typescript = { "prettier" },
    typescriptreact = { "prettier" },
    json = { "prettier" },
    jsonc = { "prettier" },
    html = { "prettier" },
    css = { "prettier" },
    yaml = { "prettier" },
    markdown = { "prettier" },
    sh = { "shfmt" },
    bash = { "shfmt" },
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
    local supported = {
      c = true,
      cpp = true,
      lua = true,
      python = true,
      javascript = true,
      javascriptreact = true,
      typescript = true,
      typescriptreact = true,
      json = true,
      jsonc = true,
      html = true,
      css = true,
      yaml = true,
      markdown = true,
      sh = true,
      bash = true,
    }
    if supported[ft] then
      return { timeout_ms = 2000, lsp_format = "fallback" }
    end
  end,
}
