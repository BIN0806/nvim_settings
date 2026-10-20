local M = {}

function M.setup(opts)
  require("cmp").setup(opts)

  -- The pinned cmp queues an InsertEnter callback through feedkeys even when
  -- completion is disabled for macros. Skip that injection before it happens,
  -- otherwise inserted text can disappear from the recorded register.
  local rules = vim.api.nvim_get_autocmds { group = "___cmp___", event = "InsertEnter" }
  assert(#rules == 1 and type(rules[1].callback) == "function", "Recheck nvim-cmp's macro guard after updating cmp")
  local callback = rules[1].callback
  vim.api.nvim_del_autocmd(rules[1].id)
  vim.api.nvim_create_autocmd("InsertEnter", {
    group = "___cmp___",
    desc = "Initialize completion outside macro recording and replay",
    callback = function(event)
      if vim.fn.reg_recording() ~= "" or vim.fn.reg_executing() ~= "" then
        return
      end
      return callback(event)
    end,
  })
end

return M
