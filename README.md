# LLMunix 🦄

> 🌐 **Part of [Evolving Agents Labs](https://evolvingagentslabs.github.io)** | 🔬 [View All Experiments](https://evolvingagentslabs.github.io#experiments) | 📖 [Project Details](https://evolvingagentslabs.github.io/experiments/llmunix.html)

A Pure Markdown Operating System where an AI agent acts as the kernel. It's designed to be run by a manifest-aware, tool-calling runtime like an enhanced **[Gemini CLI](https://github.com/google-gemini/gemini-cli)**.

LLMunix implements a concept called **Adaptive Behavior Management**, where the system's behavior dynamically adapts through evolving behavioral constraints.

-   **Pure Markdown Architecture**: All system components—agents and tools—are human-readable Markdown files.
-   **Manifest-Driven**: The entire OS "firmware" and "system calls" are defined in a single `GEMINI.md` file.
-   **Adaptive State Management**: The agent modifies its own behavioral constraints in `workspace/state/constraints.md` during execution.
-   **Intelligent Memory System**: The agent learns from past executions stored in `system/memory_log.md`.
-   **Dynamic Evolution**: The agent can write new Markdown component files to create new tools and agents on the fly when existing ones are insufficient.

---

## Quick Start

The LLMunix workflow is a simple and powerful two-step process.

**1. Boot the System (Run Once)**

This deterministic script prepares the workspace. It clears any previous state, ensuring a fresh run.

```bash
# From the llmunix project root:
./llmunix-boot
```

**2. Execute a Goal**

Now, start the Gemini CLI. It will automatically detect the `GEMINI.md` manifest and become an autonomous agent. Provide your high-level goal directly at the prompt.

```bash
# Start the Gemini CLI
gemini

# Give the agent its goal
> Monitor 5 tech news sources, extract trending topics, and generate an intelligence briefing.
```

The system will now take over, create a plan, and execute it autonomously until the goal is complete.

![LLMunix Demo](./llmunix.gif)

---

## How It Works

This repository is a "program" written in Markdown. The `GEMINI.md` file acts as a manifest that transforms the Gemini CLI into a dedicated runtime for LLMunix.

1.  **Boot:** The `./llmunix-boot` script creates a clean `workspace/state` directory.
2.  **Activation:** When you run `gemini`, it detects `GEMINI.md`, loads the "SystemAgent" firmware, and dynamically registers the virtual tools defined within it.
3.  **Execution Loop:** When you provide a goal, the agent starts its autonomous loop:
    *   It uses `read_file` to understand its plan and context.
    *   It calls tools like `web_fetch` and `summarize` to interact with the world.
    *   It can invoke pre-built, specialized agents from the `components/agents/` directory using the `run_agent` tool.
    *   If a required capability is missing, it will use `write_file` to create a new agent or tool in the `components/` directory.
    *   It uses `write_file` and `append_to_file` to manage its state and log its history.

### Core Architecture

The architecture is designed for clarity, extensibility, and autonomous operation.

```
llmunix/
├── llmunix-boot         # The deterministic boot script.
├── GEMINI.md            # The master manifest: OS firmware and all virtual tools.
├── components/          # A library of pre-built, reusable agents and tools.
│   ├── agents/
│   └── tools/
├── scenarios/           # Example tasks and workflows.
├── system/              # Core, non-executable system files.
│   └── memory_log.md
└── workspace/           # Ephemeral working directory for a single run.
    └── state/           # The agent's live memory and state.
```

## Acknowledgements

*   **Original Concept & Research**: [Matias Molinas](https://github.com/matiasmolinas) and [Ismael Faro](https://github.com/ismaelfaro).

*This project is an experimental research prototype from **Evolving Agents Labs**.*