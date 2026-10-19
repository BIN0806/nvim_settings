return {
  {
    "neovim/nvim-lspconfig",
    event = { "BufReadPre", "BufNewFile" },
    dependencies = { "mason-org/mason.nvim" },
    config = function()
      require "configs.lspconfig"
    end,
  },
  {
    "mason-org/mason.nvim",
    opts = {
      PATH = "prepend",
      ensure_installed = {
        "clangd",
        "clang-format",
        "codelldb",
        "lua-language-server",
        "stylua",
        "pyright",
        "ruff",
        "typescript-language-server",
        "prettier",
        "bash-language-server",
        "shellcheck",
        "shfmt",
        "json-lsp",
      },
    },
  },
  {
    "stevearc/conform.nvim",
    event = "BufWritePre",
    opts = require "configs.conform",
  },
  {
    "nvim-treesitter/nvim-treesitter",
    branch = "main",
    lazy = false,
    build = ":TSUpdate",
    opts = {
      ensure_installed = {
        "c",
        "cpp",
        "lua",
        "luadoc",
        "vim",
        "vimdoc",
        "query",
        "cmake",
        "bash",
        "json",
        "markdown",
        "markdown_inline",
        "python",
        "javascript",
        "typescript",
        "tsx",
        "html",
        "css",
        "yaml",
        "toml",
        "matlab",
      },
    },
    config = function()
      require("nvim-treesitter").setup {}
    end,
  },
  {
    "https://codeberg.org/mfussenegger/nvim-dap.git",
    name = "nvim-dap",
    event = "VeryLazy",
    dependencies = {
      "mason-org/mason.nvim",
      "jay-babu/mason-nvim-dap.nvim",
      "rcarriga/nvim-dap-ui",
      "nvim-neotest/nvim-nio",
    },
    config = function()
      require "configs.dap"
    end,
    keys = {
      {
        "<leader>db",
        function()
          require("dap").toggle_breakpoint()
        end,
        desc = "Debug breakpoint",
      },
      {
        "<leader>dr",
        function()
          require("dap").continue()
        end,
        desc = "Debug start / continue",
      },
      {
        "<leader>dc",
        function()
          require("dap").continue()
        end,
        desc = "Debug continue",
      },
      {
        "<leader>do",
        function()
          require("dap").step_over()
        end,
        desc = "Debug step over",
      },
      {
        "<leader>di",
        function()
          require("dap").step_into()
        end,
        desc = "Debug step into",
      },
      {
        "<leader>dO",
        function()
          require("dap").step_out()
        end,
        desc = "Debug step out",
      },
      {
        "<leader>dq",
        function()
          require("dap").terminate()
        end,
        desc = "Debug stop",
      },
      {
        "<leader>du",
        function()
          require("dapui").toggle()
        end,
        desc = "Debug panels",
      },
      {
        "<leader>de",
        function()
          require("dapui").eval()
        end,
        mode = { "n", "v" },
        desc = "Debug evaluate",
      },
      {
        "<F5>",
        function()
          require("dap").continue()
        end,
        desc = "Debug start / continue",
      },
      {
        "<F10>",
        function()
          require("dap").step_over()
        end,
        desc = "Debug step over",
      },
      {
        "<F11>",
        function()
          require("dap").step_into()
        end,
        desc = "Debug step into",
      },
      {
        "<F12>",
        function()
          require("dap").step_out()
        end,
        desc = "Debug step out",
      },
    },
  },
  {
    "christoomey/vim-tmux-navigator",
    cmd = { "TmuxNavigateLeft", "TmuxNavigateDown", "TmuxNavigateUp", "TmuxNavigateRight", "TmuxNavigatePrevious" },
  },
  {
    "nvim-mini/mini.nvim",
    version = "*",
    event = "VeryLazy",
    config = function()
      require("mini.ai").setup { n_lines = 500 }
      require("mini.surround").setup {}
      require("mini.move").setup {
        mappings = {
          left = "<leader>mh",
          right = "<leader>ml",
          down = "<leader>mj",
          up = "<leader>mk",
          line_left = "<leader>mh",
          line_right = "<leader>ml",
          line_down = "<leader>mj",
          line_up = "<leader>mk",
        },
      }
      require("mini.sessions").setup {
        autoread = false,
        autowrite = false,
        directory = vim.fn.stdpath "state" .. "/sessions",
        file = "",
      }
    end,
  },
  {
    "sindrets/diffview.nvim",
    cmd = { "DiffviewOpen", "DiffviewClose", "DiffviewFileHistory" },
    dependencies = { "nvim-lua/plenary.nvim" },
  },
  {
    "folke/zen-mode.nvim",
    cmd = "ZenMode",
    opts = { window = { width = 100 }, plugins = { tmux = { enabled = false } } },
  },
  {
    "sphamba/smear-cursor.nvim",
    main = "smear_cursor",
    event = "VeryLazy",
    cond = function()
      return not vim.g.neovide
    end,
    opts = require "configs.cursor",
    cmd = "SmearCursorToggle",
    keys = {
      { "<leader>uc", "<cmd>SmearCursorToggle<CR>", desc = "Toggle animated cursor trail" },
    },
  },
}
