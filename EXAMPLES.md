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

### External LLM Integration (Multi-Model Workflows)

This example demonstrates using local LLMs alongside the primary model for specialized tasks.

```
> Please analyze the following code snippet `function example(a, b) { return a + b / 2; }` for potential bugs. 
> First, get a second opinion from the llama3.2 model, then provide your final analysis. 
> Use the Ollama that is running in my local machine
```

**Expected Behavior:**
1. **CAPABILITY CHECK:** The system uses `list_files` and finds `LocalLLMTool.md` in `components/tools/`.
2. **TOOL EXECUTION:** Calls `run_tool` with `path="components/tools/LocalLLMTool.md"` and arguments:
   ```json
   {
     "model": "llama3.2",
     "prompt": "Please analyze this code for bugs: function example(a, b) { return a + b / 2; }"
   }
   ```
3. **LLM RESPONSE:** The llama3.2 model identifies several issues:
   - **Operator precedence**: Division happens before addition (b/2 is calculated first)
   - **No input validation**: Missing type checks for parameters
   - **Division by zero**: No check if b could be zero
   - **Floating point precision**: Potential rounding errors
4. **SYNTHESIS:** The primary model combines llama3.2's analysis with its own insights, providing a comprehensive review that includes:
   - The operator precedence bug (likely intent was `(a + b) / 2`)
   - Type coercion issues in JavaScript
   - Recommendations for improvement

**Actual Output Example:**
```
✦ The llama3.2 model has provided a good initial analysis. Here's my final analysis of the code snippet function example(a, b) { return a + b / 2; }:

Potential Bugs and Considerations:

1. **Operator Precedence**: The most immediate and common issue with this snippet is operator precedence. Division (/) has higher precedence than addition (+). This means b / 2 will be calculated first, and then the result will be added to a.
   * Example: If a = 10 and b = 4, the function will return 10 + (4 / 2) = 10 + 2 = 12.
   * If the intent was `(a + b) / 2`: The code should be return (a + b) / 2; to ensure the sum of a and b is divided by 2.

2. **Input Validation / Type Coercion**: JavaScript is dynamically typed, so a and b can be of any type.
   * If a or b are not numbers, JavaScript will attempt type coercion.
   * Example: If a = "hello" and b = 4, b / 2 is 2, but "hello" + 2 results in "hello2" (string concatenation).

3. **Division by Zero**: If b is 0, the expression b / 2 will result in 0. This is generally not an error in JavaScript.

4. **Floating-Point Precision**: As with any language using standard floating-point representation (IEEE 754), arithmetic operations can sometimes lead to small precision errors.
```

**Key Benefits:**
- **Model specialization**: Use models optimized for specific tasks
- **Local processing**: Keep sensitive code on-premise
- **Cost optimization**: Use smaller models for routine tasks
- **Consensus building**: Get multiple perspectives on critical decisions

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

### Complex Tool Orchestration

This example shows how virtual tools can work together in sophisticated workflows.

```
> Create a comprehensive competitor analysis for our new AI music app. 
> Use web search for public info, consult llama3.2 for market insights, 
> and generate visualizations of the competitive landscape.
```

**Expected Behavior:**
1. **MULTI-TOOL PLANNING:** Creates a plan involving multiple tools:
   - `web_fetch` for competitor websites
   - `google_search` for market data
   - `LocalLLMTool` for analysis via llama3.2
   - A newly created `VisualizationAgent` for charts
2. **PARALLEL EXECUTION:** Runs multiple tools concurrently when possible
3. **DATA FLOW:** Passes outputs between tools, e.g., web data → llama3.2 → visualization
4. **ERROR RESILIENCE:** If one tool fails (e.g., web fetch quota), adapts by using alternatives

### Virtual Tool Creation On-Demand

This demonstrates the system creating new tools during execution.

```
> I need to analyze 100 CSV files for anomalies. Create whatever tools you need to process them efficiently.
```

**Expected Behavior:**
1. **CAPABILITY GAP:** Realizes no CSV processing tool exists
2. **TOOL GENERATION:** Creates `CSVAnalyzer.md` with:
   ```markdown
   #### analyze_csv
   `sh`
   ```sh
   #!/bin/bash
   FILE_PATH=$(echo "$GEMINI_TOOL_ARGS" | jq -r .path)
   # Use awk/sed for CSV processing
   # Detect anomalies based on statistical analysis
   ```
   ```
3. **BATCH PROCESSING:** Uses the new tool to process all files
4. **OPTIMIZATION:** May create additional tools for parallel processing

## Key Insights

These examples illustrate the transformative power of the manifest-driven virtual tool system:

1. **Immediate Extensibility**: New capabilities can be added by writing Markdown
2. **Tool Composition**: Complex workflows emerge from simple tool combinations  
3. **Runtime Evolution**: The system adapts its toolset during execution
4. **Security & Transparency**: All tool logic is auditable and sandboxed
5. **Multi-Model Orchestration**: Seamlessly integrate external AI services

The manifest-driven architecture provides a flexible and powerful foundation for creating truly autonomous, adaptive, and self-improving AI systems that can leverage the best tools and models for each task.