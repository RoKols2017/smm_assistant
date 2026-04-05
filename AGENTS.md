# AGENTS.md

> Project map for AI agents. Keep this file up-to-date as the project evolves.

## Project Overview
Python project for generating SMM content with OpenAI, publishing it to VK and Telegram, and collecting basic social media statistics. See `.ai-factory/DESCRIPTION.md` for the fuller project specification.

## Tech Stack
- **Language:** Python
- **Framework:** None detected
- **Database:** None detected
- **ORM:** None detected

## Project Structure
```text
.
|- generators/               # OpenAI-backed text and image generation modules
|- social_publishers/        # VK and Telegram publishing adapters
|- social_stats/             # Platform statistics collection
|- tests/                    # Unit and integration test suite
|- .cursor/                  # Editor-specific project rules
|- .opencode/                # Local AI skills and tool metadata
|- README.md                 # User-facing project overview and usage
|- SECURITY.md               # Security notes and guidance
|- requirements.txt          # Python dependencies
|- pytest.ini                # Pytest configuration and coverage thresholds
|- run_tests.py              # Test runner helper
|- test.py                   # End-to-end demo script
|- test_env.py               # Environment validation script
|- .env.example              # Example environment variables
|- .mcp.json                 # MCP server configuration for AI tooling
`- .ai-factory/              # AI Factory project context files
```

## Key Entry Points
| File | Purpose |
|------|---------|
| `test.py` | Runs the demo workflow: generate content, publish, then collect stats |
| `test_env.py` | Validates required environment variables and setup |
| `run_tests.py` | Convenience entry point for the test suite |
| `generators/text_gen.py` | Generates post text through OpenAI chat completions |
| `generators/image_gen.py` | Generates images through OpenAI image APIs |
| `social_publishers/vk_publisher.py` | Publishes posts to VK |
| `social_publishers/telegram_publisher.py` | Sends posts to Telegram |
| `social_stats/stats_collector.py` | Collects VK and Telegram statistics |
| `requirements.txt` | Declares runtime and test dependencies |
| `pytest.ini` | Defines pytest discovery and coverage settings |

## Documentation
| Document | Path | Description |
|----------|------|-------------|
| README | `README.md` | Project landing page |
| Getting Started | `docs/getting-started.md` | Installation, setup, first run |
| Configuration | `docs/configuration.md` | Environment variables and settings |
| Architecture | `docs/architecture.md` | Project structure and modules |
| Testing | `docs/testing.md` | Test and development commands |
| Security | `docs/security.md` | Secrets and security practices |

## AI Context Files
| File | Purpose |
|------|---------|
| `AGENTS.md` | This file - project structure map |
| `.ai-factory/DESCRIPTION.md` | Project specification and detected stack |
| `.ai-factory/ARCHITECTURE.md` | Architecture decisions and implementation rules |
| `CLAUDE.md` | Claude Code instructions and preferences if added later |
