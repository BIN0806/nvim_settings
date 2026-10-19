local workspace = require "configs.workspace"
require "mappings"
local fixture = vim.fn.tempname() .. "/project with spaces"
vim.fn.mkdir(fixture .. "/.git", "p")
fixture = vim.uv.fs_realpath(fixture)
local original = vim.fn.getcwd()
vim.api.nvim_set_current_dir(fixture)
local captured
workspace.terminal = function(command, cwd)
  captured = { command = command, cwd = cwd }
end
local mapping = vim.fn.maparg("<leader>ak", "n", false, true)
assert(type(mapping.callback) == "function", "Space a k callback missing")
mapping.callback()
local expected = vim.fn.shellescape(vim.fn.expand "~/.local/bin/kun")
  .. " start --project "
  .. vim.fn.shellescape(fixture)
assert(captured and captured.command == expected, "Kun project command/path quoting incorrect: " .. vim.inspect(captured))
vim.api.nvim_set_current_dir(original)
vim.fn.delete(vim.fs.dirname(fixture), "rf")
print "PASS: Space a k resolves the installed launcher and quotes the detected project path; no model started"
vim.cmd "qa!"
