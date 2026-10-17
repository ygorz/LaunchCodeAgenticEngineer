# LaunchCodeAgenticEngineer

LaunchCode Agentic Engineer Course

Each `module_N/` folder is a self-contained Docker development environment for one module of the course. Every module has its own `Dockerfile`, `requirements.txt`, Claude Code `settings.json`, status line script, `CLAUDE.md`, and a `README.md` with build and run instructions. Later modules build on earlier ones.

## Project Structure

```
.
├── module_1/                 # Base environment: Python 3.12, AI/ML libraries, Claude Code CLI
│   ├── module_x.py           # Business-rule utilities (Session A exercise: write unit tests)
│   ├── module_y.py           # Formatting/reporting utilities (Session B exercise: improve docs)
│   └── agent_docker_check.md # Agent prompt for reviewing and test-building the Docker setup
├── module_2/                 # Adds Slack and Gmail MCP servers, skills, and agents
│   ├── agents/               # Sub-agent definitions (code-reviewer, email-summarize)
│   ├── skills/               # Slash-command skills (Slack, Gmail, email, session summary)
│   ├── sample_docs/          # Sample PRD, rubric, and iteration log
│   └── sample_review.py      # Sample file for the code-review agent
└── module_3/                 # Multi-agent orchestration, custom MCP servers, and evaluation
    ├── agents/               # Planner, implementer, reviewer, project-manager, and other agents
    ├── skills/               # Slash-command skills carried over from Module 2
    ├── mcp/                  # Course MCP servers (coursetools, retrieval, storage)
    ├── eval/                 # Orchestrator, regression/holdout runners, rubric, and tests
    ├── docs/                 # PRD, orchestration diagrams, routing map, and eval reports
    ├── scripts/              # Helpers to start MCP servers and run retrieval comparisons
    ├── .memory/reference/    # Reference notes used by the retrieval server
    └── .eval-artifacts/      # Recorded dev and holdout evaluation runs
```

## Getting Started

Pick the module you are working on and follow its README:

- [Module 1](module_1/README.md)
- [Module 2](module_2/README.md)
- [Module 3](module_3/README.md)

For example, to build and run Module 1:

```bash
cd module_1
docker build -t agentic_engineer_1 .
docker run -it --rm -v claude-auth:/claude-auth -p 8501:8501 -v "$PWD":/workspace agentic_engineer_1
```

The `claude-auth` named volume stores your Claude Code login so you only sign in once across all modules.
