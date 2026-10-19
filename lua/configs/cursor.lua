-- A terminal alternative to GUI cursor animation, with quiet typing/tool panes.
return {
  cursor_color = "#cdd6f4",
  smear_between_buffers = false,
  smear_between_neighbor_lines = true,
  scroll_buffer_space = true,
  smear_insert_mode = false,
  smear_terminal_mode = false,
  smear_to_cmd = false,
  legacy_computing_symbols_support = false,
  time_interval = 17,
  stiffness = 0.8,
  trailing_stiffness = 0.6,
  damping = 0.95,
  distance_stop_animating = 0.5,
  max_length = 16,
  filetypes_disabled = {
    "TelescopePrompt", "NvimTree", "lazy", "mason", "help",
    "dap-repl", "dapui_scopes", "dapui_stacks", "dapui_breakpoints", "dapui_watches", "dapui_console",
  },
}
