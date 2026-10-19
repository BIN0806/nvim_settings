local function run()
  require("lazy").load { plugins = { "mason.nvim", "nvim-treesitter" } }
  local registry = require "mason-registry"
  local refreshed = false
  local refresh_ok = false
  registry.refresh(function(success)
    refresh_ok = success
    refreshed = true
  end)
  assert(vim.wait(120000, function() return refreshed end, 100), "Mason registry refresh timed out")
  assert(refresh_ok, "Mason registry refresh failed")
  local packages = require("lazy.core.config").plugins["mason.nvim"].opts.ensure_installed
  for _, name in ipairs(packages) do
    local pkg = registry.get_package(name)
    if not pkg:is_installed() then
      print("Installing " .. name)
      pkg:install()
    end
  end
  assert(vim.wait(240000, function()
    for _, name in ipairs(packages) do
      local pkg = registry.get_package(name)
      if not pkg:is_installed() or pkg:is_installing() then return false end
    end
    return true
  end, 200), "Mason tool installation failed or timed out; inspect :MasonLog")
  local opts = require("lazy.core.config").plugins["nvim-treesitter"].opts
  require("nvim-treesitter").install(opts.ensure_installed):wait(240000)
  for _, lang in ipairs(opts.ensure_installed) do
    assert(pcall(vim.treesitter.language.add, lang), "Missing parser: " .. lang)
  end
  print "All configured Mason tools and syntax parsers installed"
end

local ok, err = pcall(run)
if not ok then
  io.stderr:write(tostring(err) .. "\n")
  vim.cmd "cquit 1"
else
  vim.cmd "qa!"
end
