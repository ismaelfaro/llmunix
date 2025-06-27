# LLMunix 🦄

A Pure Markdown Operating System where an AI agent acts as the kernel. It's designed to be run by a manifest-aware, tool-calling runtime like an enhanced **[Gemini CLI](https://github.com/google-gemini/gemini-cli)**.

LLMunix implements a concept called **Adaptive Behavior Management**, where the system's behavior dynamically adapts through evolving behavioral constraints.

- **Pure Markdown Architecture**: All system components are human-readable Markdown files.
- **Manifest-Driven**: The entire OS "boots" from a single `GEMINI.md` file that defines its core logic and "system calls".
- **Adaptive State Management**: Behavioral constraints (e.g., user sentiment, priority) in `workspace/state/constraints.md` evolve during execution.
- **Intelligent Memory System**: The agent learns from past executions stored in `system/memory_log.md`.
- **Dynamic Evolution**: The agent can write new Markdown component files to create new tools and agents on the fly.

![LLMunix boot demo](./llmunix.gif)

## How It Works

This repository doesn't contain an executable itself. It is a "program" written in Markdown, meant to be run by a capable interpreter like a future version of Gemini CLI.

### The Vision: Running with Gemini CLI

The goal is to enable this kind of execution:

```bash
# 1. cd into the llmunix directory
cd llmunix

# 2. Start Gemini CLI with a high-level goal
gemini --goal "Monitor 5 tech news sources, extract trending topics, and generate an intelligence briefing"
```

### Expected Behavior of the Runtime

1.  **Manifest Detection:** The CLI finds `GEMINI.md` and enters "runtime mode".
2.  **Firmware Load:** It uses the main body of `GEMINI.md` as the core `SystemAgent` prompt.
3.  **Virtual Tool Loading:** It parses the `### Tools` section and dynamically makes those shell commands available as tools to the LLM.
4.  **Execution Loop:** The `SystemAgent` begins its loop:
    *   It uses the `state_read` tool to understand its plan and context.
    *   It calls tools like `web_fetch` (which in turn calls the native Gemini tool) to interact with the world.
    *   It uses `state_write` to update its `plan.md` and `constraints.md`.
    *   It uses `state_append` to log its `history.md`.
    *   It uses `file_writer` to create the final `intel_briefing.md` in the `workspace/` directory.

### Sentient State Architecture

```
llmunix/
├── GEMINI.md            # The master manifest: OS firmware and virtual tool definitions.
├── components/          # Directory for agents and tools defined in Markdown.
├── scenarios/           # Example tasks and workflows.
├── system/              # Core, non-executable system files like the memory log.
│   └── memory_log.md
└── workspace/           # Ephemeral working directory for a single run.
    └── state/           # The agent's live memory and state.
        ├── plan.md
        ├── context.md
        ├── history.md
        └── constraints.md
```

## Acknowledgements

*   **Original Concept & Research**: [Matias Molinas](https://github.com/matiasmolinas) and [Ismael Faro](https://github.com/ismaelfaro).

*This project is an experimental research prototype from **Evolving Agents Labs**.*
