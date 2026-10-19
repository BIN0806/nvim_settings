local root = vim.fs.dirname(vim.fs.dirname(debug.getinfo(1, "S").source:sub(2)))
local checks = {}
local function passed(name, detail)
  checks[#checks + 1] = { check = name, detail = detail, passed = true }
  print("PASS: " .. name)
end

local function run()
  vim.fn.chdir(root .. "/example")
  vim.cmd.edit(root .. "/example/src/main.cpp")
  local bufnr = vim.api.nvim_get_current_buf()
  local client
  assert(vim.wait(30000, function()
    client = vim.lsp.get_clients({ bufnr = bufnr, name = "clangd" })[1]
    return client and client.initialized
  end, 100), "clangd did not attach")
  passed("clangd attachment", client.config.cmd[1])

  local uri = vim.uri_from_bufnr(bufnr)
  local hover = client:request_sync("textDocument/hover", {
    textDocument = { uri = uri }, position = { line = 6, character = 13 },
  }, 15000, bufnr)
  assert(hover and hover.result and hover.result.contents, "C++ hover failed")
  passed("C++ hover", "clangd resolves local symbols")

  -- Exercise language completion and diagnostics on unsaved buffer contents.
  local original = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false)
  vim.api.nvim_buf_set_lines(bufnr, 7, 8, false, { "  prices." })
  local completion = client:request_sync("textDocument/completion", {
    textDocument = { uri = uri }, position = { line = 7, character = 9 },
    context = { triggerKind = 1 },
  }, 15000, bufnr)
  local items = completion and completion.result and (completion.result.items or completion.result) or {}
  assert(#items > 0, "C++ completion returned no items")
  passed("C++ completion", #items .. " vector member suggestions")
  vim.api.nvim_buf_set_lines(bufnr, 7, 8, false, { "  undefined_nvim_probe();" })
  assert(vim.wait(15000, function()
    for _, diagnostic in ipairs(vim.diagnostic.get(bufnr)) do
      if diagnostic.message:find("undefined_nvim_probe", 1, true) then return true end
    end
    return false
  end, 100), "C++ diagnostics did not report the unknown function")
  passed("C++ diagnostics", "unknown function detected")
  vim.api.nvim_buf_set_lines(bufnr, 0, -1, false, original)
  vim.bo[bufnr].modified = false

  require("lazy").load { plugins = { "nvim-cmp", "conform.nvim", "nvim-dap" } }
  assert(require("cmp").get_config().sources[1].name == "nvim_lsp", "LSP completion source missing")
  passed("completion menu", "nvim-cmp LSP source loaded")
  assert(pcall(vim.treesitter.get_parser, bufnr, "cpp"), "C++ syntax parser missing")
  passed("C++ syntax highlighting", "C++ tree-sitter parser loaded")

  local format_path = root .. "/example/src/.nvim-format-probe.cpp"
  vim.cmd.edit(format_path)
  vim.api.nvim_buf_set_lines(0, 0, -1, false, { "int main(){int x=1;return x;}" })
  vim.cmd.write()
  local formatted = table.concat(vim.api.nvim_buf_get_lines(0, 0, -1, false), "\n")
  assert(formatted:find("int x = 1;", 1, true) and formatted:find("\n"), "Format on save failed")
  passed("format on save", "clang-format reformatted a C++ buffer when written")
  vim.cmd.bdelete()
  vim.fn.delete(format_path)

  vim.cmd.edit(root .. "/example/src/main.cpp")
  local dap = require "dap"
  assert(vim.wait(10000, function() return dap.adapters.codelldb ~= nil end, 100), "CodeLLDB adapter was not configured")
  vim.api.nvim_win_set_cursor(0, { 8, 0 })
  dap.toggle_breakpoint()
  local stopped = false
  dap.listeners.after.event_stopped.nvim_setup_test = function() stopped = true end
  dap.run {
    name = "Neovim setup smoke test", type = "codelldb", request = "launch",
    program = root .. "/example/build/app", cwd = root .. "/example",
    stopOnEntry = false, args = {}, runInTerminal = false,
  }
  assert(vim.wait(60000, function()
    local session = dap.session()
    return stopped and session and session.current_frame
  end, 100), "Debugger did not stop at the C++ breakpoint")
  passed("C++ breakpoint", "CodeLLDB stopped at main.cpp:8")
  local session = dap.session()
  local evaluated, evaluation_error, evaluation
  session:request("evaluate", {
    expression = "total", context = "watch", frameId = session.current_frame.id,
  }, function(err, result)
    evaluation_error, evaluation, evaluated = err, result, true
  end)
  assert(vim.wait(15000, function() return evaluated end, 100), "Variable evaluation timed out")
  assert(not evaluation_error and evaluation and evaluation.result == "100", vim.inspect(evaluation_error or evaluation))
  passed("debugger variables", "total = 100")
  dap.continue()
  assert(vim.wait(15000, function() return dap.session() == nil end, 100), "Debug session did not exit")
  passed("debugger exit", "Program resumed and exited")
  vim.fn.writefile({ vim.json.encode(checks) }, root .. "/verification/results.json")
end

local ok, err = xpcall(run, debug.traceback)
if ok then
  print "All Neovim C++ runtime checks passed"
  vim.cmd "qa!"
else
  io.stderr:write(err .. "\n")
  local ok_dap, dap = pcall(require, "dap")
  if ok_dap then pcall(dap.terminate) end
  vim.cmd "cquit 1"
end
