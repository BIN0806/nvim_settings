local root = vim.fs.dirname(vim.fs.dirname(debug.getinfo(1, "S").source:sub(2)))
local checks = {}
local tmp = vim.fn.tempname()
vim.fn.mkdir(tmp, "p")
tmp = vim.uv.fs_realpath(tmp)
local function pass(name, detail)
  checks[#checks + 1] = { check = name, detail = detail, passed = true }
  print("PASS: " .. name)
end
local function keys(value)
  vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes(value, true, false, true), "xt", false)
end
local function git(args, cwd)
  local command = { "git" }
  vim.list_extend(command, args)
  local result = vim.system(command, { cwd = cwd or tmp, text = true }):wait()
  assert(result.code == 0, result.stderr)
  return vim.trim(result.stdout or "")
end
local function write(path, lines) vim.fn.writefile(lines, tmp .. "/" .. path) end
local function edit(path) vim.cmd.edit(vim.fn.fnameescape(tmp .. "/" .. path)) end
local function attach(name)
  local client
  assert(vim.wait(40000, function()
    client = vim.lsp.get_clients({ bufnr = 0, name = name })[1]
    return client and client.initialized
  end, 100), name .. " did not initialize")
  return client
end
local function diagnostic(fragment)
  assert(vim.wait(30000, function()
    for _, item in ipairs(vim.diagnostic.get(0)) do
      if item.message:lower():find(fragment:lower(), 1, true) then return true end
    end
  end, 100), "Missing diagnostic containing " .. fragment)
end
local function run()
  vim.wait(100, function() return false end)
  require("lazy").load { plugins = { "mini.nvim", "conform.nvim", "gitsigns.nvim", "diffview.nvim" } }
  local ws = require "configs.workspace"
  vim.fn.chdir(tmp)

  vim.cmd.enew()
  vim.api.nvim_buf_set_lines(0, 0, -1, false, { "alpha", "beta", "gamma" })
  vim.api.nvim_win_set_cursor(0, { 1, 0 })
  keys('saiw"')
  assert(vim.api.nvim_get_current_line() == '"alpha"', "Surround add failed")
  keys('sd"')
  assert(vim.api.nvim_get_current_line() == "alpha", "Surround delete failed")
  keys(" mj")
  assert(vim.api.nvim_buf_get_lines(0, 0, 2, false)[1] == "beta", "Line move mapping failed")
  pass("surround and moving lines", "Actual mapped keystrokes add/remove quotes and move a line")
  vim.bo.modified = false

  write("refresh.txt", { "initial" })
  edit "refresh.txt"
  write("refresh.txt", { "changed externally" })
  vim.api.nvim_exec_autocmds("FocusGained", { buffer = 0 })
  assert(vim.api.nvim_get_current_line() == "changed externally", "Unmodified file did not refresh")
  vim.api.nvim_buf_set_lines(0, 0, -1, false, { "my unsaved edit" })
  write("refresh.txt", { "another external change" })
  vim.api.nvim_exec_autocmds("FocusGained", { buffer = 0 })
  assert(vim.api.nvim_get_current_line() == "my unsaved edit", "External reload overwrote unsaved work")
  pass("external agent edits", "Saved buffers refresh; unsaved edits survive")
  vim.bo.modified = false

  write("layout.txt", { "layout" })
  edit "layout.txt"
  vim.cmd.vsplit(tmp .. "/refresh.txt")
  require("mini.sessions").setup { directory = tmp .. "/sessions", file = "", autoread = false, autowrite = false }
  local session = require "mini.sessions"
  session.write "verification"
  vim.cmd.only()
  session.read "verification"
  assert(#vim.api.nvim_tabpage_list_wins(0) == 2, "Session did not restore editor split")
  assert(not vim.o.sessionoptions:find("terminal", 1, true), "Sessions would restore terminal processes")
  pass("editor sessions", "Saved and restored two editor windows; terminal replay excluded")
  vim.cmd.only()

  write("pyproject.toml", { '[project]', 'name = "nvim-probe"', 'version = "0.0.0"' })
  write("probe.py", { "import os", 'value: int = "wrong type"', 'print(  "hello"  )' })
  edit "probe.py"
  attach "pyright"
  attach "ruff"
  diagnostic "int"
  require("conform").format { async = false, timeout_ms = 10000 }
  local python_text = table.concat(vim.api.nvim_buf_get_lines(0, 0, -1, false), "\n")
  assert(python_text:find('print("hello")', 1, true), "Ruff formatting failed: " .. python_text)
  vim.bo.modified = false
  pass("Python language tools", "Pyright type error, Ruff attachment and real formatting")

  write("package.json", { '{"name":"nvim-verification","private":true}' })
  write("tsconfig.json", { '{"compilerOptions":{"strict":true},"include":["*.ts"]}' })
  write("probe.ts", { 'const value:number="wrong type"', "console.log(value)" })
  edit "probe.ts"
  attach "ts_ls"
  diagnostic "number"
  vim.cmd.write()
  assert(vim.api.nvim_get_current_line():find("const value: number =", 1, true), "Prettier save formatting failed")
  pass("TypeScript language tools", "TypeScript type error and Prettier formatting on save")

  write("probe.json", { '{"value":1}' })
  edit "probe.json"
  attach "jsonls"
  vim.cmd.write()
  assert(table.concat(vim.api.nvim_buf_get_lines(0, 0, -1, false), ""):find('"value": 1', 1, true), "JSON formatting failed")
  pass("JSON language tools", "JSON language server and Prettier work")

  write("probe.sh", { "#!/usr/bin/env bash", "echo $1" })
  edit "probe.sh"
  attach "bashls"
  diagnostic "quote"
  pass("shell diagnostics", "Bash language server reports ShellCheck quoting warning")

  git { "init", "-q" }
  write("tracked.txt", { "before" })
  git { "add", "tracked.txt" }
  git { "-c", "user.name=Neovim Verification", "-c", "user.email=nvim-check@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture" }
  write("tracked.txt", { "after" })
  edit "tracked.txt"
  assert(vim.wait(15000, function() return vim.b.gitsigns_head ~= nil end, 100), "Git signs did not attach")
  assert(vim.wait(15000, function() return #(require("gitsigns").get_hunks() or {}) > 0 end, 100), "No Git hunk detected")
  require("gitsigns").stage_hunk()
  assert(vim.wait(10000, function() return git { "diff", "--cached", "--name-only" } == "tracked.txt" end, 100), "Hunk was not staged")
  require("gitsigns").reset_buffer_index()
  assert(vim.wait(10000, function() return git { "diff", "--cached", "--name-only" } == "" end, 100), "File was not unstaged")
  pass("Git hunks", "A real fixture change was detected, staged, and unstaged")
  vim.cmd "DiffviewOpen"
  assert(vim.wait(10000, function()
    local view = require("diffview.lib").get_current_view()
    if not (view and view.cur_layout and view.cur_layout:is_files_loaded()) then return false end
    local before, after = false, false
    for _, win in ipairs(vim.api.nvim_tabpage_list_wins(0)) do
      local text = vim.api.nvim_buf_get_lines(vim.api.nvim_win_get_buf(win), 0, 1, false)[1]
      before = before or text == "before"
      after = after or text == "after"
    end
    return before and after
  end, 100), "Diffview did not display both the old and new file contents")
  vim.cmd "DiffviewClose"
  pass("side-by-side Git review", "Diffview opened and closed a real working-tree diff")

  edit "tracked.txt"
  local inputs = { "codex/verification", tmp .. "/isolated" }
  local old_input, old_terminal = vim.ui.input, ws.terminal
  local opened
  vim.ui.input = function(_, callback) callback(table.remove(inputs, 1)) end
  ws.terminal = function(_, cwd) opened = cwd end
  ws.new_worktree()
  assert(vim.wait(15000, function() return opened ~= nil end, 100), "Worktree creation did not finish")
  vim.ui.input, ws.terminal = old_input, old_terminal
  assert(git({ "branch", "--show-current" }, opened) == "codex/verification", "Wrong worktree branch")
  assert(vim.fn.filereadable(opened .. "/tracked.txt") == 1, "Worktree checkout is incomplete")
  pass("parallel-task isolation", "Created a real independent Git worktree and branch")
  for _, name in ipairs { "Codex", "Claude", "OpenCode" } do
    local command = assert(ws.agent_command(name), name .. " missing")
    assert(not command:find("dangerously", 1, true), "Permission-bypass flag found")
  end
  pass("agent launchers", "Three installed CLIs resolve; no model calls made during verification")
  vim.fn.writefile({ vim.json.encode(checks) }, root .. "/verification/merge-results.json")
end
local ok, err = xpcall(run, debug.traceback)
if not ok then
  vim.fn.writefile({ tostring(err) }, root .. "/verification/merge-error.log")
  io.stderr:write(tostring(err) .. "\n")
  vim.cmd "cquit 1"
else
  print "All merged-workflow runtime checks passed"
  vim.cmd "qa!"
end
