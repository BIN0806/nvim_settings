require("nvchad.configs.lspconfig").defaults()

local capabilities = vim.deepcopy(require("nvchad.configs.lspconfig").capabilities)
capabilities.offsetEncoding = { "utf-16" }

vim.lsp.config("clangd", {
  cmd = {
    require("configs.tools").find "clangd",
    "--background-index",
    "--clang-tidy",
    "--completion-style=detailed",
  },
  capabilities = capabilities,
  init_options = { clangdFileStatus = true },
})

vim.lsp.enable "clangd"
