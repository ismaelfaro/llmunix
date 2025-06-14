# LLMunix

A Pure Markdown Operating System where everything is either an agent or tool defined in markdown documents. Claude Code serves as the runtime engine interpreting these markdown specifications.

## Quick Start

### Prerequisites
First, start Claude Code in your terminal:
```bash
claude
```

### Boot LLMunix
Once you're in the Claude Code console, boot the LLMunix operating system:
```bash
boot llmunix
```

![LLMunix boot demo](llmunix.mp4)

*Watch LLMunix boot demonstration*

### Example Commands

**Real-world research task:**
```bash
# Act as SystemAgent and execute the RealWorld_Research_Task scenario in EXECUTION MODE
llmunix execute: "Get live content from https://huggingface.co/blog and create a research summary"
```

**Custom task execution:**
```bash  
# Act as SystemAgent and execute: [your goal] using real tools
llmunix execute: "Analyze all markdown components in this system and create an architecture overview"
```

## What is LLMunix?

LLMunix is an AI-powered operating system that:

- **Uses Pure Markdown**: All system components are markdown files interpreted by Claude
- **Generates Tools Dynamically**: Creates new tools on-demand based on natural language requests  
- **Leverages Real Tools**: Maps to Claude Code's native tools (WebFetch, FileSystem, Bash, etc.)
- **Learns from Experience**: Smart memory system tracks patterns and optimizes performance
- **Manages State**: Persistent execution state with resumable workflows

### Core Architecture

```
llmunix/
├── system/           # Core OS components (Kernel, Memory, Shell, etc.)
├── components/       # Available tools and agents
│   ├── tools/        # Executable tools (WebFetch, FileSystem, etc.) 
│   └── agents/       # Decision-making agents (Summarization, etc.)
├── scenarios/        # Pre-defined task workflows
└── workspace/        # Active execution environment and user files
```

### Key Features

- **Natural Language Commands**: Interact using plain English instead of complex syntax
- **Dynamic Tool Generation**: Creates specialized tools for any task in seconds
- **Smart Memory**: System learns from your patterns and suggests optimizations
- **Real Tool Integration**: Uses actual web fetching, file operations, and system commands
- **State Machine Execution**: Atomic operations with error recovery and resumable workflows

### Operating Modes

1. **EXECUTION MODE**: Real operations using Claude Code's native tools
2. **SIMULATION MODE**: Training data generation through simulation patterns

## Key Capabilities

- **WebFetch**: Live web content retrieval with error handling
- **FileSystem**: Real file operations (Read/Write/Search/List)  
- **Bash**: System command execution for complex tasks
- **Task**: Parallel sub-task execution for complex workflows
- **State Management**: Execution state persisted with full audit trail
- **Cost Tracking**: Real-time monitoring of execution costs
- **Training Data**: Automatic collection from real executions for AI improvement

## Summary of LLMunix Features

Based on the comprehensive documentation, LLMunix offers:

**AI-Powered Command Interface**
- Natural language command interpretation instead of traditional CLI syntax
- Intent recognition that understands what you want to accomplish
- Context-aware behavior that adapts to your workspace and patterns
- Smart suggestions and workflow automation

**Dynamic Tool Ecosystem**  
- On-demand tool creation for any task within seconds
- Component-based architecture with rich metadata management
- Real-time optimization and performance monitoring
- Tool evolution that improves automatically based on usage

**Advanced Memory Management**
- Adaptive learning from user patterns and preferences
- Predictive caching and resource preloading  
- Pattern recognition for workflow optimization
- Continuous performance optimization with minimal overhead

**Intelligent File System**
- Virtual directories (bin/, proc/, dev/) with real functionality
- Executable markdown components as programs
- Semantic search by intent rather than just name patterns
- Automatic file organization based on usage and relationships

**Process Intelligence**
- Resource optimization for CPU, memory, and I/O
- Error prevention and prediction of failure scenarios
- Performance monitoring with real-time analytics
- Automatic error recovery and process management

**Security & Safety**
- Sandboxed execution environments for all tools
- Granular permission management and access control
- Complete audit trails of all system operations
- Secure-by-default configurations and safe operation modes

---

## Acknowledgements

*   Original Concept Contributors: [Matias Molinas](https://github.com/matiasmolinas) and [Ismael Faro](https://github.com/ismaelfaro).

*LLM-OS: Where simulation meets reality, and training data drives the future of autonomous AI.*
