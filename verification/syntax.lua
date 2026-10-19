local root = vim.fs.dirname(vim.fs.dirname(debug.getinfo(1, "S").source:sub(2)))
for _, path in ipairs(vim.fn.glob(root .. "/**/*.lua", false, true)) do
  assert(loadfile(path))
end
print "All Neovim configuration files parse successfully"
