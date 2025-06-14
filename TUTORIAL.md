# LLM-OS Tutorial: From Setup to Real AI Research

This tutorial guides you through using LLM-OS to perform real-world AI research tasks using Claude Code as the runtime engine.

## What You'll Learn

- How to execute real tasks using Claude Code's native tools
- How LLM-OS bridges simulation and reality for training data generation
- How to use the state machine execution model
- How to generate high-quality training datasets from real execution

## Prerequisites

- Claude Code CLI installed and configured
- This project directory open in Claude Code
- Basic understanding of AI research and web content analysis

## Table of Contents

1. [Quick Start: Hugging Face Research](#quick-start-hugging-face-research)
2. [Understanding AGI-OS Architecture](#understanding-agi-os-architecture)
3. [Step-by-Step Tutorial](#step-by-step-tutorial)
4. [Training Data Generation](#training-data-generation)
5. [Error Recovery and Debugging](#error-recovery-and-debugging)
6. [Advanced Usage](#advanced-usage)

## Understanding AGI-OS Architecture

### Dual-Mode Operation
- **EXECUTION MODE**: Uses real Claude Code tools (WebFetch, Read, Write)
- **SIMULATION MODE**: Generates training data through realistic simulation

### Core Components
- **SystemAgent** (`system/SystemAgent.md`) - State machine orchestrator
- **Components** (`components/`) - Real and simulated tool definitions
- **SmartLibrary** (`system/SmartLibrary.md`) - Component registry with [REAL] tools
- **SmartMemory** (`system/SmartMemory.md`) - Experience log from real executions
- **ExecutionState** (`workspace/execution_state.md`) - Live execution tracking

## Quick Start: Hugging Face Research

### 30-Second Demo

Execute this command to see LLM-OS in action:

```bash
"Act as SystemAgent and execute the RealWorld_Research_Task scenario in EXECUTION MODE"
```

### What Happens
1. LLM-OS creates a state machine execution plan
2. Attempts to fetch live content from https://huggingface.co/blog
3. Analyzes content using real summarization
4. Generates structured outputs and training data
5. Provides complete audit trail of execution

## Step-by-Step Tutorial

### Step 1: Initial State Check

Before running, verify the initial state:

```bash
# Check workspace is ready
ls workspace/

# Check past experiences
cat system/SmartMemory.md

# Check available [REAL] components
grep -A 3 "\[REAL\]" system/SmartLibrary.md
```

### Step 2: Execute the Updated Research Scenario

The updated scenario now uses Hugging Face blog for better accessibility:

```bash
"Act as SystemAgent and execute the RealWorld_Research_Task scenario in EXECUTION MODE"
```

### Step 3: Understanding the Real Execution Flow

Watch for these phases in AGI-OS execution:

#### Phase 1: State Initialization
```
**Goal Comprehension & State Setup**:
- Creates workspace/execution_state.md with 4-step execution plan
- Sets variables: target_url: https://huggingface.co/blog
- Mode: EXECUTION (using real tools)
```

#### Phase 2: Planning with Real Tools
```
**Component Discovery**: 
- tool_real_web_fetch_v1 [REAL]: WebFetch tool, cost: $0.001-0.01, latency: 2-10s
- agent_real_summarizer_v1 [REAL]: Analysis with quality metrics
- tool_real_filesystem_v1 [REAL]: Read/Write operations, cost: none
```

#### Phase 3: State Machine Execution
```
**State Transition [1→2]: Real Web Data Acquisition**
- Tool: WebFetch
- Input: {"url": "https://huggingface.co/blog", "prompt": "Extract blog content"}
- Real Output: Live content from Hugging Face blog
- Updates execution_state.md with real performance data

**State Transition [2→3]: Real Content Analysis**  
- Tool: Built-in analysis + Read/Write
- Input: Raw blog content
- Real Output: Structured JSON with quality metrics (confidence: 0.92)

**State Transition [3→4]: Report Generation**
- Tool: Write
- Input: Combined analysis and raw data
- Real Output: Professional research report

**State Transition [4→COMPLETE]: Training Data Collection**
- Tool: Write  
- Input: Complete execution trace
- Real Output: Training dataset with real performance metrics
```

### Step 4: Examine the Complete Results

After execution, you'll have these files:

```bash
# Check the state machine audit trail
cat workspace/execution_state.md

# Check the fetched content
cat workspace/huggingface_blog_content.txt

# Check the structured analysis
cat workspace/ai_research_summary.json

# Check the professional report
cat workspace/ai_research_report.md

# Check the training dataset
cat workspace/execution_trace.json

# Check updated experience log
tail -20 system/SmartMemory.md
```

## Training Data Generation

### Generate Simulation Data

For large training datasets without real tool costs:

```bash
"Act as SystemAgent and simulate the RealWorld_Research_Task scenario in SIMULATION MODE for training data"
```

### Batch Training Data Creation

```bash
"Act as SystemAgent and generate 10 variations of research tasks in SIMULATION MODE with focus areas: AI safety, multimodal AI, language models, computer vision, reinforcement learning, AI ethics, edge AI, hardware, generative AI, and applications"
```

## Error Recovery and Debugging

AGI-OS handles real-world errors gracefully:

### Common Error Scenarios
- **WebFetch failures**: 403, 404, timeout errors
- **Network issues**: Connection timeouts, rate limits
- **Content processing**: Large files, malformed data

### Error Recovery Process
1. Error detected and logged in execution_state.md
2. Recovery strategies attempted (retries, alternatives)
3. Graceful degradation when needed
4. Training data includes error scenarios

### Debugging Failed Executions
```bash
# Check where execution stopped
cat workspace/execution_state.md

# Look for error details in training data
grep -A 5 "error" workspace/execution_trace.json
```

## Advanced Usage

### Custom Research Tasks

```bash
"Act as SystemAgent and execute: Research the latest transformer architectures from Hugging Face papers and create a technical comparison report"
```

### Multi-Source Research

```bash
"Act as SystemAgent and execute: Fetch AI news from multiple sources and create a comprehensive weekly AI update report"
```

### Specialized Analysis

```bash
"Act as SystemAgent and execute: Analyze recent computer vision models on Hugging Face and create an implementation guide"
```

You have now learned how to use AGI-OS for real AI research with automatic training data generation!