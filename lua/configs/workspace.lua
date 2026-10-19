local M = {}

function M.root()
  local path = vim.api.nvim_buf_get_name(0)
  if path == "" or vim.bo.buftype ~= "" then
    path = vim.fn.getcwd()
  end
  return vim.fs.root(path, { ".git", "CMakeLists.txt", "pyproject.toml", "package.json", "go.mod", "Cargo.toml" })
    or vim.fn.getcwd()
end

function M.terminal(command, cwd, position)
  require("nvchad.term").new {
    pos = position or "vsp",
    cmd = command,
    termopen_opts = { cwd = cwd or M.root() },
  }
end

-- Only build a command here. Opening an agent is always a deliberate user action.
function M.agent_command(name)
  local candidates = {
    Codex = { "codex", "/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex" },
    Claude = { "claude", "/opt/homebrew/bin/claude" },
    OpenCode = { "opencode", vim.fn.expand "~/.opencode/bin/opencode" },
    Pi = { "pi" },
  }
  for _, binary in ipairs(candidates[name] or {}) do
    if vim.fn.executable(binary) == 1 then
      local command = vim.fn.shellescape(vim.fn.exepath(binary) ~= "" and vim.fn.exepath(binary) or binary)
      if name == "Codex" then
        command = command .. " --sandbox workspace-write"
      end
      return command
    end
  end
end

function M.agent(name)
  if not name then
    local choices = {}
    for _, candidate in ipairs { "Codex", "Claude", "OpenCode", "Pi" } do
      if M.agent_command(candidate) then
        choices[#choices + 1] = candidate
      end
    end
    return vim.ui.select(choices, { prompt = "Coding agent (uses its own account):" }, M.agent)
  end
  local command = M.agent_command(name)
  if not command then
    return vim.notify(name .. " CLI is not installed or not on PATH", vim.log.levels.WARN)
  end
  M.terminal(command)
end

function M.lazygit()
  if vim.fn.executable "lazygit" ~= 1 then
    return vim.notify "Install lazygit first"
  end
  M.terminal(vim.fn.shellescape(vim.fn.exepath "lazygit"), nil, "float")
end

function M.kun()
  local binary = vim.fn.expand "~/.local/bin/kun"
  if vim.fn.executable(binary) ~= 1 then
    return vim.notify("Kun launcher is missing; see agentic/README.md", vim.log.levels.WARN)
  end
  M.terminal(vim.fn.shellescape(binary) .. " start --project " .. vim.fn.shellescape(M.root()))
end

function M.task_note()
  local path = M.root() .. "/.agent-notes/task.md"
  if vim.fn.filereadable(path) == 0 then
    vim.fn.mkdir(vim.fs.dirname(path), "p")
    vim.fn.writefile({
      "# Task",
      "",
      "## Outcome",
      "What should the user be able to do?",
      "",
      "## Starting point",
      "Relevant files, current behavior, reproduction steps.",
      "",
      "## Constraints",
      "Compatibility, scope, and decisions that need my review.",
      "",
      "## Plan",
      "- [ ] Inspect the project",
      "- [ ] Agree on an approach",
      "- [ ] Implement",
      "- [ ] Run project checks",
      "- [ ] Review the diff",
      "",
      "## Validation",
      "Exact commands and expected behavior:",
      "",
      "## Handoff",
      "What changed, checks run, known limitations, next step.",
    }, path)
  end
  vim.cmd.edit(vim.fn.fnameescape(path))
end

function M.worktrees()
  local result = vim.system({ "git", "worktree", "list" }, { cwd = M.root(), text = true }):wait()
  vim.notify(
    result.code == 0 and result.stdout or result.stderr,
    result.code == 0 and vim.log.levels.INFO or vim.log.levels.ERROR
  )
end

function M.new_worktree()
  local root = M.root()
  local head = vim.system({ "git", "rev-parse", "--verify", "HEAD" }, { cwd = root, text = true }):wait()
  if head.code ~= 0 then
    return vim.notify("A worktree needs a Git repository with a commit", vim.log.levels.WARN)
  end
  vim.ui.input({ prompt = "New branch (for example codex/fix-login): " }, function(branch)
    if not branch or branch == "" then
      return
    end
    local valid = vim.system({ "git", "check-ref-format", "--branch", branch }, { cwd = root }):wait()
    if valid.code ~= 0 or branch:sub(1, 1) == "-" then
      return vim.notify("Invalid branch name", vim.log.levels.ERROR)
    end
    local default = vim.fs.dirname(root) .. "/.worktrees/" .. vim.fs.basename(root) .. "-" .. branch:gsub("/", "-")
    vim.ui.input({ prompt = "Worktree folder: ", default = default, completion = "dir" }, function(path)
      if not path or path == "" then
        return
      end
      path = vim.fn.fnamemodify(vim.fn.expand(path), ":p")
      vim.system({ "git", "worktree", "add", "-b", branch, path, "HEAD" }, { cwd = root, text = true }, function(result)
        vim.schedule(function()
          if result.code ~= 0 then
            return vim.notify(result.stderr, vim.log.levels.ERROR)
          end
          vim.notify("Worktree created: " .. path .. "\nOpen nvim here for an isolated task.")
          M.terminal(nil, path)
        end)
      end)
    end)
  end)
end

return M
