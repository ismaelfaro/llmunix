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
Start the Gemini CLI. The `GEMINI.md` manifest will be detected, turning the CLI into an autonomous agent. Provide your high-level goal directly at the prompt.

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
1.  **PLAN:** The system creates a `plan.md` using `write_file` to outline the steps: identify sources, fetch content, analyze, and generate the briefing.
2.  **EXECUTE (Loop):** It uses `web_fetch` to get raw HTML, `write_file` to save the content to `workspace/fetched_content/`, and the `summarize` tool to process the text.
3.  **COMPLETE:** It writes the final `intelligence_briefing.md` to `workspace/outputs/` using `write_file` and notifies the user.

### Dynamic Capability Evolution (Self-Improvement)

This example shows the system creating a new tool it needs to complete a task.

```
> Analyze the sentiment of the latest 5 articles on TechCrunch AI and tell me if the overall tone is positive or negative.
```

**Expected Behavior:**
1.  **PLAN & GAP ANALYSIS:** The system determines it lacks a specialized "sentiment analysis" capability.
2.  **EVOLVE:** It autonomously generates the Markdown definition for a new `SentimentAnalysisAgent.md` and uses `write_file` to save it to `components/agents/`. The runtime automatically detects this new component.
3.  **EXECUTE:** After fetching the articles, it invokes its newly created agent using the `run_agent(path="components/agents/SentimentAnalysisAgent.md", ...)` tool to get the sentiment scores for each article.
4.  **COMPLETE:** It synthesizes the scores and provides a final answer.

### Hierarchical Agent Delegation

This showcases a high-level orchestration of specialized agents.

```
> Create a full marketing campaign for a new product called 'SynthWave AI', an AI music tool. I need ad copy, a target audience profile, and a blog post outline.
```

**Expected Behavior:**
1.  **ORCHESTRATE:** The system creates a high-level plan (define audience, generate copy, create outline).
2.  **DELEGATE:** For each sub-task, it invokes a specialized agent (e.g., `AdCopyGeneratorAgent`, `MarketingPersonaAgent`) using the `run_agent` tool. If a required agent doesn't exist, it creates it first using the Evolve pattern.
3.  **SYNTHESIZE:** It combines the outputs from all the specialist agents into a final `campaign_brief.md` file using `write_file`.

---

## 🔬 Advanced Scenarios

These examples demonstrate the system's more sophisticated adaptive capabilities.

### Adaptive Execution & Constraint Management

```
> URGENT: Analyze this 50-page legal document for risks in under 10 minutes. Focus only on liability and termination clauses.
```

**Expected Behavior:**
*   The system parses the "URGENT" and "10 minutes" cues from the prompt.
*   It immediately calls `write_file` to update `workspace/state/constraints.md` with new rules like `priority: speed_and_clarity` and `max_execution_time: 600`.
*   It then proceeds with the task, altering its plan to prioritize speed over comprehensive analysis, for example by using a more focused prompt for its `summarize` tool calls.

### Memory-Driven Task Improvement

```
> Research the latest advancements in quantum computing.
```
*(After a previous run where the agent used slow or unreliable sources...)*

**Expected Behavior:**
*   The system's first action is to call `read_file` on `system/memory_log.md` to review past experiences tagged with "quantum computing".
*   It finds a log entry noting: "Fetching from `slow-science-journal.com` timed out. `fast-arxiv.com` was more reliable."
*   In its new plan, it intelligently prioritizes `fast-arxiv.com` and avoids the previously problematic source, demonstrating learning from experience.

These examples illustrate that the manifest-driven architecture provides a flexible and powerful foundation for creating truly autonomous, adaptive, and self-improving AI systems.