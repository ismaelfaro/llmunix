# LLMunix: Pure Markdown Operating System Framework

This is LLMunix, a Pure Markdown Operating System where everything is either an agent or tool defined in markdown documents. Claude Code serves as the runtime engine interpreting these markdown specifications.

## Framework Philosophy: Pure Markdown

**CRITICAL: LLMunix is a PURE MARKDOWN framework. Everything is either an agent or tool defined in markdown documents.**

### Core Principles:
- **No Code Generation**: System behavior emerges from Claude interpreting markdown documents
- **Agent/Tool Duality**: Every component is either an agent (decision maker) or tool (executor)
- **Sentient State Architecture**: Behavioral constraints evolve dynamically to enable adaptive decision-making
- **Memory-Driven Learning**: Historical experiences become actionable intelligence for continuous improvement
- **Dynamic Creation**: New tools/agents are created as markdown specifications during runtime
- **Claude as Kernel**: Claude Code acts as the OS kernel interpreting markdown system definitions

### Operating Modes:
1. **EXECUTION MODE**: Real operations using Claude Code's native tools mapped through markdown specs
2. **SIMULATION MODE**: Training data generation through markdown-defined simulation patterns

The OS "boots" when Claude reads the markdown system files and begins interpreting them as a functional operating system.

## How to Boot LLMunix

### Boot Command
```
boot llmunix
```

This simple command activates the LLMunix kernel by having Claude read and interpret the markdown system files as a functional operating system. **Boot automatically cleans the workspace directory to ensure a fresh execution environment.**

### Boot Welcome Message
When LLMunix boots, display ASCII art welcome and example commands in this format:

```
██╗     ██╗     ███╗   ███╗██╗   ██╗███╗   ██╗██╗██╗  ██╗
██║     ██║     ████╗ ████║██║   ██║████╗  ██║██║╚██╗██╔╝
██║     ██║     ██╔████╔██║██║   ██║██╔██╗ ██║██║ ╚███╔╝ 
██║     ██║     ██║╚██╔╝██║██║   ██║██║╚██╗██║██║ ██╔██╗ 
███████╗███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║██╔╝ ██╗
╚══════╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝
                Pure Markdown Operating System v1.0
```

Examples:
```bash
llmunix execute: "Monitor 5 tech news sources (TechCrunch, Ars Technica, Hacker News, MIT Tech Review, Wired), extract trending topics, identify patterns, and generate a weekly intelligence briefing"

llmunix execute: "Get live content from https://huggingface.co/blog and create a research summary"

llmunix simulate: "Research task workflow for fine-tuning dataset"
```

### Running the Real-World Research Scenario

1. **Execute the scenario** by asking Claude to:
   - Act as the SystemAgent defined in `system/SystemAgent.md`
   - Execute the goal from `scenarios/RealWorld_Research_Task.md`
   - Use EXECUTION MODE for real tool calls

2. **Expected behavior:**
   - Claude creates modular `workspace/state/` directory with specialized files
   - Initializes `constraints.md` with behavioral modifiers based on task context
   - Uses QueryMemoryTool for intelligent memory consultation during planning
   - Adapts execution style based on user sentiment and historical patterns
   - State machine execution:
     - **State 1→2**: RealWebFetchTool fetches live content with constraint-aware error handling
     - **State 2→3**: RealSummarizationAgent analyzes content using memory-recommended approaches
     - **State 3→4**: RealFileSystemTool saves structured outputs with behavioral adaptations
   - Updates modular state files after each step with real results and constraint evolution
   - Records complete experience in structured memory log with sentiment and adaptation insights
   - Generates training data from real execution trace including behavioral learning patterns

## Key Capabilities

### Real Tool Integration
- **WebFetch**: Live web content retrieval with error handling
- **FileSystem**: Real file operations (Read/Write/Search/List)
- **Bash**: System command execution for complex tasks
- **Task**: Parallel sub-task execution for complex workflows

### Sentient State Management
- **Modular State Architecture**: Specialized files for plan, context, variables, history, and constraints
- **Dynamic Behavioral Adaptation**: Constraints evolve based on user sentiment and execution events
- **Memory-Driven Planning**: Historical experiences influence current decision-making
- **Intelligent Error Recovery**: Past failure patterns guide recovery strategies
- **Atomic State Transitions**: Each step updates relevant state components
- **Resumable Execution**: Can pause and resume at any step with full context preservation
- **Cost Tracking**: Real-time monitoring with budget-aware constraint adaptation

### Advanced Learning Pipeline
- **Structured Memory Log**: YAML frontmatter with qualitative insights for intelligent querying
- **Behavioral Pattern Extraction**: User sentiment evolution and constraint adaptation tracking
- **Execution Traces**: Complete tool call sequences with real results and behavioral context
- **Performance Metrics**: Actual costs, timing, success rates, and adaptation effectiveness
- **Error Scenarios**: Real error handling examples with sentiment-aware recovery strategies
- **Quality Assessments**: Output quality scoring with behavioral and contextual metadata

### File Structure

```
llm-os/
├── system/
│   ├── SystemAgent.md              # Sentient state machine orchestrator with adaptive behavior
│   ├── SmartLibrary.md             # Component registry with real tools and memory components
│   ├── memory_log.md               # Structured, queryable experience database
│   ├── StateDirectoryTemplate.md   # Modular state architecture template
│   ├── ClaudeCodeToolMap.md        # Tool mapping and metadata
│   └── ExecutionStateTemplate.md   # Legacy template (deprecated)
├── components/
│   ├── tools/
│   │   ├── RealWebFetchTool.md     # [REAL] Live web content
│   │   ├── RealFileSystemTool.md   # [REAL] File operations
│   │   ├── QueryMemoryTool.md      # [REAL] Memory consultation interface
│   │   └── [Legacy simulation tools]
│   └── agents/
│       ├── RealSummarizationAgent.md  # [REAL] Content analysis
│       ├── MemoryAnalysisAgent.md     # [REAL] Intelligent memory querying
│       └── [Legacy simulation agents]
├── scenarios/
│   ├── RealWorld_Research_Task.md  # Live web research demo
│   └── [Legacy simulation scenarios]
├── workspace/                      # Active execution environment
│   ├── state/                     # Modular execution state
│   │   ├── plan.md                # Execution steps and metadata
│   │   ├── context.md             # Knowledge accumulation
│   │   ├── variables.json         # Structured data passing
│   │   ├── history.md             # Execution log
│   │   └── constraints.md         # Behavioral modifiers (sentient state)
│   └── [Output files from tasks]
├── LLM-OS-BLUEPRINT.md            # Architecture documentation
└── CLAUDE.md                      # This configuration file
```

### Execution Commands

**Real Task Execution:**
```
"Act as SystemAgent and execute the RealWorld_Research_Task scenario in EXECUTION MODE"
```

**Training Data Generation:**
```  
"Act as SystemAgent and simulate the research task scenario in SIMULATION MODE for training data"
```

**Custom Real Task:**
```
"Act as SystemAgent and execute: [your goal] using real tools"
```

## Development

### Adding New Real Components:
1. Create component `.md` file in `components/` with Claude tool mapping
2. Register in `system/SmartLibrary.md` with [REAL] tag and metadata
3. Test execution and validate training data generation

### Extending Tool Mappings:
1. Add new mappings to `system/ClaudeCodeToolMap.md`
2. Include cost, latency, and error mode specifications
3. Update component definitions to reference new tools

## Advanced Features

### Sentient State Management:
- **Modular State Architecture**: Specialized files in `workspace/state/` for focused updates
- **Behavioral Constraints**: `constraints.md` enables dynamic adaptation based on user sentiment and context
- **Memory-Driven Initialization**: Past experiences inform initial constraint settings
- **Real-time Adaptation**: Constraints evolve during execution based on user feedback and events
- **Atomic State Transitions**: Each component can be updated independently
- **Full Context Preservation**: Complete behavioral and execution context maintained
- **Resumable Execution**: Can pause and resume with full sentient state restoration

### Cost Optimization:
- Real-time cost tracking for all tool calls
- Intelligent tool selection based on cost/performance
- Budget management and cost reporting

### Intelligent Error Resilience:
- **Memory-Guided Recovery**: QueryMemoryTool provides historical error recovery strategies
- **Sentiment-Aware Adaptation**: Error handling adapts based on user frustration levels
- **Constraint Evolution**: Failed attempts trigger behavioral modifications for future prevention
- **Real Error Learning**: Actual tool failures become training data for improved resilience
- **Adaptive Planning**: Execution strategy adjusts based on historical success patterns
- **Context-Aware Human Escalation**: Human-in-the-loop triggered based on confidence and constraint settings

### Training Pipeline:
- Automatic training data collection from real executions
- Structured datasets for fine-tuning autonomous agents
- Quality metrics and performance benchmarking

## Clean Restart

To reset LLM-OS:
1. Clear `workspace/` directory including `workspace/state/` (preserves execution artifacts)
2. Reset `system/memory_log.md` to empty state (clears learning history and behavioral patterns)
3. Archive any valuable execution traces and behavioral learning data for training
4. Ready for fresh scenario execution with clean sentient state

## New Memory and Learning Features

### Intelligent Memory Consultation
- **QueryMemoryTool**: Standardized interface for memory-driven decision making
- **MemoryAnalysisAgent**: Advanced pattern recognition across historical executions
- **Behavioral Learning**: User sentiment patterns and constraint preferences captured
- **Adaptive Recommendations**: Memory provides actionable insights for current tasks

### Sentient State Architecture
- **Dynamic Constraints**: Behavioral modifiers that evolve based on context and feedback
- **User Sentiment Tracking**: Emotional state detection and adaptive response strategies
- **Priority Adaptation**: Execution focus adjusts based on user needs and historical patterns
- **Persona Switching**: Communication style adapts to optimize user experience
- **Error Tolerance Management**: Risk acceptance levels adjust based on task criticality and user preferences

### Advanced Execution Patterns
- **Memory-Informed Planning**: Historical success patterns guide component selection and strategy
- **Constraint-Aware Execution**: Every action considers current behavioral modifiers
- **Real-time Adaptation**: Behavioral constraints update during execution based on events
- **Sentiment-Driven Recovery**: Error handling strategies adapt to user emotional state
- **Learning Integration**: Every execution contributes to behavioral pattern database