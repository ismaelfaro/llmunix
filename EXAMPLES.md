# LLMunix Examples: Autonomous, Adaptive, and Evolvable Workflows

This document showcases the power of the LLMunix framework when run by a manifest-aware interpreter like an enhanced Gemini CLI. The examples demonstrate how the system can autonomously plan, evolve, and execute complex tasks.

## 🚀 The LLMunix Workflow

All examples follow a simple two-step process:

**1. Boot the System (Once per session)**
This deterministic script prepares the workspace for the agentic runtime.

```bash
./llmunix-boot
```

**2. Execute a Goal**
Start the Gemini CLI. The `GEMINI.md` manifest will be detected, turning the CLI into an autonomous agent. Provide your high-level goal at the prompt.

```bash
gemini
> Your high-level goal here...
```

---

## 🎯 Core Capability Examples

### Autonomous Research & Analysis

This demonstrates the system's ability to plan a multi-step research task, use tools to gather information, and synthesize a report.

```
> Monitor 5 tech news sources (e.g., TechCrunch, Ars Technica), extract trending topics in AI, and generate an intelligence briefing summarizing the key themes.
```

**Expected Behavior:**
1.  **Planning:** The system creates a `plan.md` to identify sources, fetch content, analyze topics, and generate the briefing.
2.  **Execution:** It loops through the plan, using tools like `web_fetch` to gather data, `write_file` to save intermediate results, and `summarize` to process content.
3.  **Completion:** It writes the final `intelligence_briefing.md` to the `workspace/outputs/` directory and notifies the user.

### Dynamic Capability Evolution (Self-Improvement)

This example shows the system creating a new tool it needs to complete a task.

```
> Analyze the sentiment of the latest 5 articles on TechCrunch AI and tell me if the overall tone is positive or negative.
```

**Expected Behavior:**
1.  **Planning & Gap Analysis:** The system determines it lacks a specialized "sentiment analysis" tool.
2.  **Evolution:** It autonomously generates the Markdown definition for a new `SentimentAnalysisAgent.md` in `components/agents/` and uses `write_file` to save it. The runtime automatically detects this new component.
3.  **Execution:** After fetching the articles, it invokes its newly created agent using the `run_agent` tool to get the sentiment scores.
4.  **Completion:** It synthesizes the scores and provides a final answer.

### Hierarchical Agent Delegation

This showcases a high-level orchestration of specialized agents.

```
> Create a full marketing campaign for a new product called 'SynthWave AI', an AI music tool. I need ad copy, a target audience profile, and a blog post outline.
```

**Expected Behavior:**
1.  **Orchestration:** The system creates a high-level plan (define audience, generate copy, create outline).
2.  **Delegation:** For each sub-task, it invokes a specialized agent (e.g., `AdCopyGeneratorAgent`, `MarketingPersonaAgent`) using the `run_agent` tool. If an agent doesn't exist, it creates it first.
3.  **Synthesis:** It combines the outputs from all the specialist agents into a final `campaign_brief.md` file.

---

## 🔬 Advanced Scenarios

These examples demonstrate the system's more sophisticated adaptive capabilities.

### Adaptive Execution & Constraint Management

```
> URGENT: Analyze this 50-page legal document for risks in under 10 minutes. Focus only on liability and termination clauses.
```

**Expected Behavior:**
*   The system parses the "URGENT" and "10 minutes" cues.
*   It uses `write_file` to update `workspace/state/constraints.md` with: `priority: speed_and_clarity`, `max_execution_time: 600`.
*   It then proceeds with the task, prioritizing speed and focusing its analysis only on the relevant sections of the document.

### Memory-Driven Task Improvement

```
> Research the latest advancements in quantum computing.
```
*(After a previous run where the agent used slow or unreliable sources...)*

**Expected Behavior:**
*   The system uses the `search_file` tool on `system/memory_log.md` to find records of past "quantum computing research".
*   It discovers a note from a previous run: "Fetching from `slow-science-journal.com` timed out. `fast-arxiv.com` was more reliable."
*   In its new plan, it intelligently prioritizes `fast-arxiv.com` and avoids the previously problematic source, demonstrating learning from experience.

These examples illustrate that the manifest-driven architecture provides a flexible and powerful foundation for creating truly autonomous, adaptive, and self-improving AI systems.