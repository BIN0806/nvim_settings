local root = vim.fs.dirname(vim.fs.dirname(debug.getinfo(1, "S").source:sub(2)))
local checks = 0
local function pass(name)
  checks = checks + 1
  print("PASS: " .. name)
end

local function run()
  vim.o.lines = 48
  vim.o.columns = 120
  vim.o.shell = "/bin/sh"
  vim.wait(100, function()
    return false
  end)

  -- Load the candidate explicitly: installed NvChad may prioritize stdpath(config).
  dofile(root .. "/lua/autocmds.lua")
  local before = #vim.api.nvim_get_autocmds { group = "WorkspaceComfort" }
  dofile(root .. "/lua/autocmds.lua")
  dofile(root .. "/lua/autocmds.lua")
  local rules = vim.api.nvim_get_autocmds { group = "WorkspaceComfort" }
  assert(#rules == before, "Reloading duplicated workspace autocommands")
  for _, rule in ipairs(rules) do
    assert(rule.desc and rule.desc ~= "", "A workspace rule has no inspection description")
  end
  pass "Autocommands reload without duplicates and have readable descriptions"

  local calls = 0
  local highlight = vim.hl.on_yank
  vim.hl.on_yank = function()
    calls = calls + 1
  end
  vim.api.nvim_buf_set_lines(0, 0, -1, false, { "copy this text" })
  vim.cmd.normal { "yy", bang = true }
  vim.hl.on_yank = highlight
  assert(calls == 1, "Yanking did not trigger exactly one highlight callback")
  vim.bo.modified = false
  pass "A real yank triggers one highlight after reloading settings"

  local editor = vim.api.nvim_get_current_win()
  require("nvchad.term").new { pos = "sp" }
  vim.cmd.stopinsert()
  local terminal = vim.api.nvim_get_current_win()
  local buffer = vim.api.nvim_get_current_buf()
  assert(vim.bo[buffer].buftype == "terminal", "NvChad did not start a real terminal")
  assert(vim.wo[terminal].winfixheight, "Horizontal terminal height is not fixed")
  local height = vim.api.nvim_win_get_height(terminal)
  vim.api.nvim_set_current_win(editor)
  vim.cmd.split()
  assert(vim.api.nvim_win_get_height(terminal) == height, "Splitting code resized the fixed terminal")
  assert(not vim.wo.winfixheight, "The code split inherited fixed terminal height")
  pass "A real horizontal terminal keeps its height when the code window is split"

  require("nvchad.term").new { pos = "vsp" }
  vim.cmd.stopinsert()
  assert(not vim.wo.winfixheight, "Vertical terminal inherited the horizontal rule")
  vim.api.nvim_set_current_win(editor)
  vim.cmd.new()
  vim.fn.jobstart({ "/bin/sh" }, { term = true })
  assert(vim.bo.buftype == "terminal", "Generic terminal fixture did not start")
  assert(not vim.wo.winfixheight, "Generic test/debug terminal inherited the NvChad rule")
  pass "Vertical and generic test/debug terminals keep their normal layout behavior"

  vim.api.nvim_set_current_win(terminal)
  vim.wo.winfixheight = false
  assert(not vim.wo.winfixheight, "The terminal-height preference cannot be disabled")
  pass "The terminal-height preference can be disabled for an individual window"
end

local ok, err = xpcall(run, debug.traceback)
if not ok then
  io.stderr:write(tostring(err) .. "\n")
  vim.cmd "cquit 1"
else
  print("All " .. checks .. " autocommand runtime checks passed; no model requests")
  vim.cmd "qa!"
end
