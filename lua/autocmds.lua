require "nvchad.autocmds"

vim.api.nvim_create_autocmd("FileType", {
  group = vim.api.nvim_create_augroup("CppIndent", { clear = true }),
  pattern = { "c", "cpp" },
  desc = "Use two-space indentation for C and C++",
  callback = function()
    vim.opt_local.expandtab = true
    vim.opt_local.shiftwidth = 2
    vim.opt_local.tabstop = 2
  end,
})

local group = vim.api.nvim_create_augroup("WorkspaceComfort", { clear = true })
vim.api.nvim_create_autocmd("TextYankPost", {
  group = group,
  desc = "Briefly highlight copied text",
  callback = function()
    vim.hl.on_yank { timeout = 150 }
  end,
})
vim.api.nvim_create_autocmd("BufReadPost", {
  group = group,
  desc = "Restore the last valid cursor position",
  callback = function(event)
    local mark = vim.api.nvim_buf_get_mark(event.buf, '"')
    if mark[1] > 1 and mark[1] <= vim.api.nvim_buf_line_count(event.buf) then
      pcall(vim.api.nvim_win_set_cursor, 0, mark)
    end
  end,
})
vim.api.nvim_create_autocmd("FileType", {
  group = group,
  pattern = { "markdown", "text" },
  desc = "Enable wrapping and spelling for prose",
  callback = function()
    vim.opt_local.wrap = true
    vim.opt_local.linebreak = true
    vim.opt_local.spell = true
  end,
})
vim.api.nvim_create_autocmd({ "FocusGained", "BufEnter", "CursorHold" }, {
  group = group,
  desc = "Refresh external edits only in saved normal buffers",
  callback = function(event)
    local buf = event.buf
    if vim.api.nvim_get_mode().mode == "n" and vim.bo[buf].buftype == "" and not vim.bo[buf].modified then
      vim.cmd("checktime " .. buf)
    end
  end,
})

-- NvChad already enters terminal input mode. Limit layout behavior to its own
-- horizontal terminals so debugger/test terminals do not inherit the example.
vim.api.nvim_create_autocmd("TermOpen", {
  group = group,
  desc = "Preserve NvChad horizontal terminal height when splitting code",
  callback = function(event)
    if vim.bo[event.buf].filetype == "NvTerm_sp" and vim.api.nvim_get_current_buf() == event.buf then
      vim.wo.winfixheight = true
    end
  end,
})
