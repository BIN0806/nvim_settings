local dap = require "dap"
local dapui = require "dapui"

dapui.setup()

-- The same Mason -> CodeLLDB -> nvim-dap integration used in the video.
require("mason-nvim-dap").setup {
  automatic_installation = false,
  handlers = {
    codelldb = function(config)
      -- macOS can take longer than DAP's 3.5-second default to load CodeLLDB.
      config.adapters.options = { max_retries = 160, initialize_timeout_sec = 20 }
      require("mason-nvim-dap").default_setup(config)
    end,
  },
}

dap.listeners.after.event_initialized.cpp_ui = function()
  dapui.open()
end
dap.listeners.before.event_terminated.cpp_ui = function()
  dapui.close()
end
dap.listeners.before.event_exited.cpp_ui = function()
  dapui.close()
end

vim.fn.sign_define("DapBreakpoint", { text = "●", texthl = "DiagnosticError", linehl = "", numhl = "" })
vim.fn.sign_define("DapStopped", { text = "▶", texthl = "DiagnosticWarn", linehl = "Visual", numhl = "" })
