local M = {}

-- Match the tutorial's Mason-managed tools; retain Homebrew as a fallback.
function M.find(name)
  local mason = vim.fn.stdpath "data" .. "/mason/bin/" .. name
  if vim.fn.executable(mason) == 1 then
    return mason
  end
  for _, prefix in ipairs { "/opt/homebrew/opt/llvm/bin/", "/usr/local/opt/llvm/bin/" } do
    if vim.fn.executable(prefix .. name) == 1 then
      return prefix .. name
    end
  end
  return vim.fn.exepath(name) ~= "" and vim.fn.exepath(name) or name
end

return M
