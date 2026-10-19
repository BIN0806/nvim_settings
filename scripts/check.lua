local root = vim.fs.dirname(vim.fs.dirname(debug.getinfo(1, "S").source:sub(2)))
local paths = vim.fn.glob(root .. "/lua/**/*.lua", false, true)
table.insert(paths, root .. "/init.lua")
for _, path in ipairs(paths) do
  local _, err = loadfile(path)
  if err then
    io.stderr:write(err .. "\n")
    vim.cmd "cquit 1"
  end
end
print("PASS: " .. #paths .. " Neovim Lua settings files parse; no plugins/agents loaded")
vim.cmd "qa!"
