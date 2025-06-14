# LLM-OS:

**LLM-OS** Is a revolutionary document-centric agent framework that bridges the gap between AI simulation and real-world execution. Using Claude Code as its runtime engine, it performs actual tasks while generating high-quality training data for developing truly autonomous AI agents.

This system transforms the paradigm from simulation-only to **real execution with automatic training data generation**.

## 🚀 What Makes LLM-OS Unique

### Dual-Mode Architecture
- **EXECUTION MODE**: Real operations using Claude Code's native tools (WebFetch, Read, Write, Bash)
- **SIMULATION MODE**: Training data generation through realistic simulation
- **State Machine Design**: Every action is an atomic, auditable state transition

### Real-World Grounding  
- **Live Web Content**: Fetch actual data from real websites with error handling
- **File System Operations**: Read, write, search real files with security boundaries
- **Error Resilience**: Handle actual network timeouts, file errors, API limits
- **Cost Awareness**: Track real execution costs and optimize performance

### Training Data Engine
- **Complete Execution Traces**: Full tool call sequences with real results
- **Performance Metrics**: Actual costs, timing, success rates
- **Error Scenarios**: Real error handling examples for robust training
- **Quality Assessment**: Output quality scoring and metadata

## Core Concepts

-   **Components as Documents**: Agents and Tools are `.md` files with Claude Code tool mappings
-   **Smart Library**: Registry of real and simulated components with [REAL] tags
-   **Smart Memory**: Experience log for continuous learning from real executions
-   **SystemAgent**: State machine orchestrator that bridges documents to real tools
-   **Execution State**: Persistent state management with atomic transitions (`workspace/execution_state.md`)
-   **Tool Mapping**: Bridge between framework components and Claude Code's native tools

## Project Structure

```
llm-os/
├── system/
│   ├── SystemAgent.md              # State machine orchestrator with real tool support
│   ├── SmartLibrary.md             # Component registry with [REAL] and legacy tools
│   ├── SmartMemory.md              # Experience log from real executions
│   ├── ClaudeCodeToolMap.md        # Tool mapping and performance metadata
│   └── ExecutionStateTemplate.md   # State management template
├── components/
│   ├── tools/
│   │   ├── RealWebFetchTool.md     # [REAL] Live web content retrieval
│   │   ├── RealFileSystemTool.md   # [REAL] File operations with Claude Code
│   │   └── [Legacy simulation tools]
│   └── agents/
│   │   ├── RealSummarizationAgent.md # [REAL] Content analysis with quality metrics
│   │   └── [Legacy simulation agents]
├── scenarios/
│   ├── RealWorld_Research_Task.md  # Live web research demonstration
│   └── [Legacy simulation scenarios]
├── workspace/                      # Active execution environment
│   └── execution_state.md          # Current execution state (created during runs)
├── LLM-OS-BLUEPRINT.md            # Complete architecture documentation
└── CLAUDE.md                      # Claude Code runtime configuration
```

## 🎯 Quick Start Tutorial

### Real Task Execution
```bash
# Execute live research task with real tools
"Act as SystemAgent and execute the RealWorld_Research_Task scenario in EXECUTION MODE"
```

### Training Data Generation
```bash
# Generate training data through simulation
"Act as SystemAgent and simulate the research task scenario in SIMULATION MODE"
```

### Expected LLM-OS Execution Flow

When executing in EXECUTION MODE, LLM-OS follows this state machine process:

1. **Initialize State**: Creates `workspace/execution_state.md` with execution plan
2. **Real Tool Planning**: Maps framework components to Claude Code tools with cost/latency data
3. **State Machine Loop**:
   - **State 1→2**: RealWebFetchTool performs actual HTTP request to live website
   - **State 2→3**: RealSummarizationAgent analyzes real content with quality metrics  
   - **State 3→4**: RealFileSystemTool saves structured outputs to workspace
4. **Training Data Collection**: Captures complete execution trace with real performance data
5. **Memory Update**: Records experience with actual costs, timing, and outcomes

### Verify Real Execution Results

After a real execution, you'll find:

-   `workspace/execution_state.md`: Complete state machine trace with real tool results
-   `workspace/[content_files]`: Live data fetched from actual websites
-   `workspace/[summary_files]`: Analysis results with quality metrics
-   `system/SmartMemory.md`: Updated with real execution experience and performance data

## 🔧 Development & Evolution

### Adding Real Components
1. Create component `.md` file with Claude Code tool mapping
2. Register in `system/SmartLibrary.md` with [REAL] tag and performance metadata
3. Test both execution and training data generation modes

### Extending Tool Capabilities
1. Add new mappings to `system/ClaudeCodeToolMap.md`
2. Include cost, latency, and error mode specifications  
3. Update component definitions to leverage new tools

### Training Pipeline
AGI-OS automatically generates structured datasets for fine-tuning:

```json
{
  "execution_id": "real_001",
  "goal": "Research AI developments",
  "tool_calls": [
    {
      "tool": "WebFetch",
      "real_inputs": {"url": "https://openai.com/blog"},
      "real_outputs": {"content": "...", "metadata": {...}},
      "performance": {"cost": "$0.012", "time": "8.3s", "success": true}
    }
  ],
  "state_transitions": [...],
  "quality_metrics": {"accuracy": 0.94, "completeness": 0.87}
}
```

## 🔮 Future Vision

LLM-OS represents the next evolution in AI development:

1. **Training Data Engine**: Generate unlimited, high-quality training examples from real execution
2. **Real-World Testing**: Test agent capabilities against actual challenges and edge cases
3. **Autonomous Evolution**: Agents that improve through real-world experience and feedback
4. **Human-AI Collaboration**: Natural interaction patterns for hybrid workflows

## 📚 Documentation

- [LLMunix-README.md](LLMunix-README.md) - LLMunix README
- [LLM-OS-BLUEPRINT.md](LLM-OS-BLUEPRINT.md) - Complete architecture and design documentation
- [CLAUDE.md](CLAUDE.md) - Claude Code runtime configuration and usage
- [LLM_TRAINING_METHODOLOGY.md](LLM_TRAINING_METHODOLOGY.md) - Training methodology and dataset generation

---

## Acknowledgements

*   Original Concept Contributors: [Matias Molinas](https://github.com/matiasmolinas) and [Ismael Faro](https://github.com/ismaelfaro).

*LLM-OS: Where simulation meets reality, and training data drives the future of autonomous AI.*
