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

-- Pyright supplies Python type information; Ruff supplies linting and fixes.
vim.lsp.config("pyright", {
  cmd = { require("configs.tools").find "pyright-langserver", "--stdio" },
  settings = { pyright = { disableOrganizeImports = true } },
})
vim.lsp.config("ruff", { cmd = { require("configs.tools").find "ruff", "server" } })
vim.lsp.config("ts_ls", { cmd = { require("configs.tools").find "typescript-language-server", "--stdio" } })
vim.lsp.config("bashls", { cmd = { require("configs.tools").find "bash-language-server", "start" } })
vim.lsp.config("jsonls", { cmd = { require("configs.tools").find "vscode-json-language-server", "--stdio" } })
vim.api.nvim_create_autocmd("LspAttach", {
  group = vim.api.nvim_create_augroup("RuffCapabilities", { clear = true }),
  callback = function(event)
    local client = vim.lsp.get_client_by_id(event.data.client_id)
    if client and client.name == "ruff" then
      client.server_capabilities.hoverProvider = false
    end
  end,
})
vim.lsp.enable { "pyright", "ruff", "ts_ls", "bashls", "jsonls" }
