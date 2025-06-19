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

![LLMunix boot demo](./llmunix.gif)

*Watch LLMunix boot demonstration*

### Example Commands

**Constraint-aware intelligence gathering:**
```bash
llmunix execute: "Monitor 5 tech news sources, extract trending topics, and generate intelligence briefing"
# System adapts constraints based on API limitations, maintains intelligence value through graceful degradation
```

**Memory-driven task execution:**
```bash
llmunix execute: "Research AI safety papers - query memory for past research patterns and apply successful approaches"
# QueryMemoryTool consults past experiences, MemoryAnalysisAgent recommends optimal strategy
```

**Adaptive execution with sentiment tracking:**
```bash
llmunix execute: "Urgent: analyze this legal document for risks in 10 minutes"
# System detects urgency, adapts constraints: priority='speed_and_clarity', persona='concise_assistant'
```

## What is LLMunix?

LLMunix is an AI-powered operating system that implements **Adaptive Behavior Management** - where system behavior dynamically adapts through evolving behavioral constraints:

- **Pure Markdown Architecture**: All system components are markdown files interpreted by Claude as a functional OS
- **Adaptive State Management**: Behavioral constraints (user sentiment, priorities, error tolerance) evolve during execution
- **Intelligent Memory System**: Structured, queryable experience database with pattern recognition and adaptive learning
- **Modular State Architecture**: Specialized state files (plan.md, context.md, constraints.md) for atomic updates
- **Real Tool Integration**: Maps to Claude Code's native tools with graceful degradation and error recovery
- **Adaptive Execution**: Dynamic constraint evolution based on user feedback, errors, and execution context

### Sentient State Architecture

```
llmunix/
├── system/
│   ├── SystemAgent.md              # Sentient state machine orchestrator
│   ├── memory_log.md               # Structured, queryable experience database
│   ├── StateDirectoryTemplate.md   # Modular state architecture template
│   └── ClaudeCodeToolMap.md        # Real tool mappings with error handling
├── components/
│   ├── tools/
│   │   ├── RealWebFetchTool.md     # Live web content with constraint-aware execution
│   │   ├── QueryMemoryTool.md      # Intelligent memory consultation
│   │   └── RealFileSystemTool.md   # File operations with behavioral adaptation
│   └── agents/
│       ├── RealSummarizationAgent.md  # Content analysis with confidence scoring
│       └── MemoryAnalysisAgent.md     # Pattern recognition across experiences
├── scenarios/           # Real-world task workflows with adaptive execution
└── workspace/
    ├── state/           # Modular execution state
    │   ├── plan.md      # Execution steps and metadata
    │   ├── context.md   # Knowledge accumulation
    │   ├── variables.json # Structured data passing
    │   ├── history.md   # Execution log
    │   └── constraints.md # Behavioral modifiers (sentient state)
    └── [Output files]   # Task results and artifacts
```

### Advanced Features

#### Adaptive State Management
- **Behavioral Constraints**: Dynamic user sentiment tracking, priority adaptation, error tolerance management
- **Constraint Evolution**: Real-time behavioral modification based on execution events and user feedback
- **Adaptive Personas**: Communication style switching (concise assistant, detailed analyst, proactive collaborator)
- **Memory-Driven Initialization**: Past experiences inform initial constraint settings for similar tasks

#### Intelligent Memory System
- **Structured Experience Database**: YAML frontmatter with qualitative insights for intelligent querying
- **QueryMemoryTool**: Natural language interface to historical experience patterns
- **MemoryAnalysisAgent**: Advanced pattern recognition and recommendation engine
- **Behavioral Learning**: User sentiment evolution and constraint preference tracking

#### Modular State Architecture
- **Atomic State Transitions**: Independent updates to plan, context, variables, history, and constraints
- **Resumable Execution**: Full context preservation with mid-task pause/resume capabilities
- **Constraint-Aware Planning**: Historical patterns guide component selection and execution strategy

### Operating Modes

1. **EXECUTION MODE**: Real operations with adaptive constraint management and intelligent error recovery
2. **SIMULATION MODE**: Training data generation with behavioral pattern simulation for agent fine-tuning

### Adaptive Behavior Principles

LLMunix operates on **Adaptive Behavior Management**: system state encompasses not just data and decisions, but **evolving behavioral constraints** that actively modify decision-making processes for intelligent adaptive behavior.

#### Key Behavioral Modifiers:
- **user_sentiment**: Detected emotional state influencing interaction style (neutral, pleased, frustrated, stressed)
- **priority**: Execution focus (speed_and_clarity, comprehensiveness, cost_efficiency, quality)
- **active_persona**: Communication style (concise_assistant, detailed_analyst, proactive_collaborator)
- **error_tolerance**: Risk acceptance level (strict, moderate, flexible)
- **human_review_trigger_level**: Threshold for seeking guidance (low, medium, high)

#### Constraint Adaptation Examples:
- **User Frustration Detected** → priority="speed_and_clarity", human_review_trigger_level="low"
- **Positive Feedback Received** → user_sentiment="pleased", active_persona="proactive_collaborator"
- **Repeated Failures** → error_tolerance="strict", memory consultation for recovery strategies
- **Cost Exceeding Budget** → priority="cost_efficiency", prefer lower-cost tool alternatives

## Advanced Capabilities

### Real Tool Integration with Adaptive Behavior
- **RealWebFetchTool**: Live content retrieval with constraint-aware error handling and graceful degradation
- **RealFileSystemTool**: File operations with behavioral adaptation based on user preferences
- **RealSummarizationAgent**: Content analysis with confidence scoring and memory-recommended approaches
- **QueryMemoryTool**: Intelligent consultation of historical experiences for decision-making

### Sentient State Features
- **Dynamic Constraint Evolution**: Behavioral modifiers adapt based on user sentiment, errors, and context
- **Intelligent Error Recovery**: Memory-guided recovery strategies from past failure patterns
- **Adaptive Execution Style**: Priority shifting (speed vs comprehensiveness) based on user needs
- **Human-in-the-Loop Integration**: Context-aware escalation based on confidence and constraint settings

### Advanced Learning Pipeline
- **Structured Memory Log**: Complete execution traces with behavioral context and learning insights
- **Pattern Recognition**: Cross-execution analysis for workflow optimization and error prevention
- **Training Data Generation**: Real execution experiences converted to fine-tuning datasets
- **Performance Optimization**: Cost tracking, latency analysis, and success rate monitoring

## Advanced Capabilities: Intelligent Adaptive Systems

### Adaptive State Management
- **Emotional Intelligence**: Real-time user sentiment detection with adaptive response strategies
- **Behavioral Evolution**: Constraints dynamically modify based on execution events and user feedback
- **Memory-Driven Adaptation**: Historical patterns inform current behavioral settings and decision-making
- **Context-Aware Personas**: Communication and execution style adapts to optimize user experience

### Intelligent Memory Architecture
- **Structured Experience Database**: YAML frontmatter enables complex querying of past executions
- **Pattern Recognition Engine**: Cross-execution analysis identifies successful approaches and failure patterns
- **Adaptive Recommendations**: Memory provides actionable insights for current task optimization
- **Behavioral Learning Database**: User preference evolution and constraint effectiveness tracking

### Modular Execution Framework
- **Atomic State Transitions**: Independent file updates (plan.md, context.md, constraints.md) for precision
- **Resumable Workflows**: Full context preservation enables pause/resume at any execution point
- **Constraint-Aware Planning**: Behavioral modifiers influence component selection and execution strategy
- **Graceful Degradation**: Intelligent fallback strategies maintain value when external dependencies fail

### Advanced Error Intelligence
- **Memory-Guided Recovery**: QueryMemoryTool provides historical error recovery strategies
- **Predictive Failure Prevention**: Pattern analysis prevents repeated failure scenarios
- **Adaptive Error Tolerance**: Risk acceptance adjusts based on task criticality and user preferences
- **Human-in-the-Loop Optimization**: Context-aware escalation based on confidence and constraint settings

### Real-World Integration
- **Production-Ready Execution**: Real Claude Code tool integration with enterprise-grade error handling
- **Cost-Aware Operations**: Intelligent tool selection balancing performance, cost, and quality constraints
- **Training Data Generation**: Complete execution traces become fine-tuning datasets for autonomous agents
- **Security & Compliance**: Complete audit trails with behavioral context for enterprise deployment

## Quick Start Guide

### 1. Boot LLMunix
```bash
boot llmunix
```

### 2. Execute with Constraint Awareness
```bash
llmunix execute: "[your goal here]"
# System automatically:
# - Initializes modular state architecture (workspace/state/)
# - Consults memory for similar task patterns
# - Adapts behavioral constraints based on context
# - Executes with real tools and adaptive error recovery
# - Records complete experience for future learning
```

### 3. Monitor Adaptive Behavior
Watch as LLMunix:
- Detects your sentiment and adapts communication style
- Evolves constraints based on execution events
- Learns from memory to optimize current task approach
- Maintains intelligence value despite external tool limitations

---

## Implementation Status: Production Ready

✅ **Sentient State Architecture**: Fully implemented with behavioral constraint evolution  
✅ **Modular State Management**: Complete workspace/state/ directory structure  
✅ **Intelligent Memory System**: Structured experience database with QueryMemoryTool  
✅ **Real Tool Integration**: Production Claude Code tool mappings with error recovery  
✅ **Adaptive Execution**: Dynamic constraint modification based on user feedback and events  
✅ **Training Data Pipeline**: Automatic generation from real execution experiences  

---

## Acknowledgements

*   Original Concept Contributors: [Matias Molinas](https://github.com/matiasmolinas) and [Ismael Faro](https://github.com/ismaelfaro).

*LLMunix: Where Adaptive Behavior meets Intelligent Memory, creating the foundation for truly intelligent autonomous AI.*
