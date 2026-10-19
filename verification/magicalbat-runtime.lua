local root = vim.fs.dirname(vim.fs.dirname(debug.getinfo(1, "S").source:sub(2)))
local checks = {}
local original_clipboard = vim.o.clipboard
vim.o.clipboard = ""
local original_register = vim.fn.getreginfo '"'
local function pass(name)
  checks[#checks + 1] = { check = name, passed = true }
  print("PASS: " .. name)
end
local function keys(value)
  vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes(value, true, false, true), "xt", false)
end
local function run()
  require "mappings"
  require("lazy").load { plugins = { "smear-cursor.nvim" } }
  vim.wait(100, function() return false end)
  local smear = require "smear_cursor"
  assert(smear.enabled and vim.fn.exists ":SmearCursorToggle" == 2)
  assert(smear.smear_insert_mode == false and smear.smear_terminal_mode == false)
  assert(smear.smear_to_cmd == false)
  pass "Pinned cursor plugin loads with typing/terminal/command-line animation disabled"
  keys " uc"
  assert(not smear.enabled, "Cursor toggle did not disable the effect")
  keys " uc"
  assert(smear.enabled, "Cursor toggle did not re-enable the effect")
  pass "Space u c toggles the real cursor plugin off and on"

  vim.cmd.enew()
  local lines = {}
  for i = 1, 100 do lines[i] = string.rep("cursor motion ", 8) end
  vim.api.nvim_buf_set_lines(0, 0, -1, false, lines)
  vim.api.nvim_win_set_cursor(0, { 1, 0 })
  vim.cmd.redraw()
  vim.api.nvim_exec_autocmds("CursorMoved", {})
  vim.wait(100, function() return false end)
  vim.api.nvim_win_set_cursor(0, { 10, 35 })
  vim.cmd.redraw()
  vim.api.nvim_exec_autocmds("CursorMoved", {})
  local saw_frame = vim.wait(300, function()
    for _, win in ipairs(vim.api.nvim_list_wins()) do
      if vim.bo[vim.api.nvim_win_get_buf(win)].filetype == "smear-cursor" then return true end
    end
    return false
  end, 2)
  assert(saw_frame, "Cursor movement produced no animation frame")
  vim.wait(800, function() return false end)
  assert(vim.deep_equal(lines, vim.api.nvim_buf_get_lines(0, 0, -1, false)))
  pass "Cursor movement renders animation frames without changing buffer text"
  smear.enabled = false

  vim.api.nvim_buf_set_lines(0, 0, -1, false, { "alpha", "beta", "gamma", "delta" })
  vim.api.nvim_win_set_cursor(0, { 2, 0 })
  keys "VJ"
  keys "<Esc>"
  assert(vim.api.nvim_buf_get_lines(0, 0, 4, false)[3] == "beta")
  vim.api.nvim_win_set_cursor(0, { 3, 0 })
  keys "VK"
  keys "<Esc>"
  assert(vim.api.nvim_buf_get_lines(0, 0, 4, false)[2] == "beta")
  vim.fn.setreg('"', "replacement")
  vim.api.nvim_win_set_cursor(0, { 2, 0 })
  keys "viwp"
  assert(vim.api.nvim_get_current_line() == "replacement")
  assert(vim.fn.getreg '"' == "replacement")
  pass "Visual J/K move lines and visual p preserves the copied register"

  vim.bo.modified = false
  vim.cmd.vsplit()
  local width = vim.api.nvim_win_get_width(0)
  keys "<C-Left>"
  assert(vim.api.nvim_win_get_width(0) == width - 1)
  keys "<C-Right>"
  assert(vim.api.nvim_win_get_width(0) == width)
  assert(vim.fn.maparg("<leader>fh", "n"):find("help_tags", 1, true))
  assert(vim.fn.maparg("<C-h>", "n"):find("TmuxNavigateLeft", 1, true))
  assert(type(vim.fn.maparg("<leader>sh", "n", false, true).callback) == "function")
  assert(type(vim.fn.maparg("<F5>", "n", false, true).callback) == "function")
  pass "Resize keys work; help, tmux navigation, source/header and debugger bindings survive"
  smear.enabled = true
end
local ok, err = pcall(run)
vim.fn.setreg('"', original_register)
vim.o.clipboard = original_clipboard
vim.fn.writefile({ vim.json.encode { checks = checks, ok = ok, error = not ok and tostring(err) or nil } },
  root .. "/verification/magicalbat-results.json")
if not ok then
  io.stderr:write(tostring(err) .. "\n")
  vim.cmd "cquit 1"
else
  vim.cmd "qa!"
end
