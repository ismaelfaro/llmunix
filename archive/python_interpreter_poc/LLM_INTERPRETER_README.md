# LLMunix LLM Interpreter

The **LLM Interpreter** is a standalone runtime engine for LLMunix that reads markdown specifications and sends them to LLM for interpretation and execution of any task using OpenAI's GPT models.

## Overview

The LLM Interpreter serves as an alternative runtime to Claude Code, offering:

- **Zero Hardcoded Logic**: All decisions made by LLM interpreting markdown specifications
- **Pure Markdown Component Parsing**: Interpreter reads and sends full markdown specs to LLM for interpretation
- **Autonomous Execution**: Complete goal achievement without user intervention  
- **On-Demand Component Analysis**: Intelligent interpretation of markdown tools/agents when needed
- **Environment Detection**: Intelligent adaptation to execution environments
- **Docker Sandbox**: Secure tool execution in isolated containers
- **Modular State Management**: Complete execution tracking and resumability
- **Real Tool Integration**: Actual command execution with error recovery

## Quick Start

### 1. Installation

```bash
# Install Python dependencies
pip install -r requirements_llm.txt

# Configure environment
cp example.env .env
# Edit .env with your OpenAI API key

# Make CLI executable
chmod +x llmunix-llm
```

### 2. Basic Usage

```bash
# Boot LLMunix with LLM Interpreter
./llmunix-llm boot

# Execute a goal
./llmunix-llm execute: "Create a Python calculator application"
```

### 3. Test Installation

```bash
# Run comprehensive test suite
python3 test_llm_interpreter.py
```

## Architecture

### Core Components

#### LLMunixInterpreter Class
- **Goal Analysis**: LLM breaks down objectives into executable plans
- **Pure Markdown Parsing**: Reads and sends full markdown specifications to LLM for interpretation
- **On-Demand Component Interpretation**: Loads markdown tools/agents and sends to LLM when needed
- **Environment Adaptation**: Detects available tools and adjusts execution  
- **Autonomous Execution**: Iterative LLM-driven action selection and execution
- **State Management**: Maintains modular execution state across iterations

#### Environment Detection System
- **Tool Discovery**: Scans execution environment for available utilities
- **Package Manager Detection**: Identifies OS package managers (apk, apt-get, yum, etc.)
- **OS Identification**: Determines Linux distribution and version
- **Documentation Generation**: Creates environment reference for LLM planning

#### Docker Integration
- **Isolated Execution**: Runs tools in secure container environments
- **Environment Consistency**: Predictable tool availability across systems
- **Resource Management**: Automatic container lifecycle management
- **Cross-Platform Support**: Works with various Docker configurations

### Execution Flow

1. **Goal Reception**: User provides natural language objective
2. **Environment Detection**: System scans for available tools and capabilities
3. **Component Discovery**: Lightweight discovery of all markdown files in the system
4. **LLM Planning**: GPT model analyzes goal and creates execution strategy
5. **Iterative Execution**: LLM decides next actions and executes them
6. **On-Demand Component Analysis**: When markdown components are called, interpreter reads and sends their specifications to LLM
7. **State Tracking**: Complete execution history maintained in modular files
8. **Error Recovery**: LLM adapts to failures and continues toward goal
9. **Completion Summary**: Final results and artifacts documented

### State Management

The interpreter creates a modular state architecture in `workspace/state/`:

```
workspace/state/
├── plan.md                    # LLM-generated execution plan
├── context.md                 # Accumulated knowledge and insights
├── variables.json             # Runtime data and structured information  
├── history.md                 # Complete execution log with decisions
├── constraints.md             # Behavioral modifiers and adaptation rules
├── container_environment.md   # Environment detection results
└── execution_plan.json        # Structured plan data
```

## Environment Detection

### Automatic Tool Discovery

The interpreter automatically detects:

- **Available Commands**: python3, pip, curl, bash, git, etc.
- **Package Managers**: apk (Alpine), apt-get (Ubuntu/Debian), yum (CentOS), etc.
- **OS Information**: Distribution, version, architecture
- **Environment Characteristics**: Container vs host, tool versions

### Adaptive Command Selection

Based on detection results, the LLM automatically:

- Uses correct package manager for the detected OS
- Selects available tools instead of assuming standard ones
- Adapts commands to environment capabilities
- Provides fallback strategies for missing tools

### Example Detection Output

```markdown
# Container Environment Detection

## Available Tools
python3, pip, curl, bash, sh, cat, grep, sed, awk

## Package Managers  
apk

## OS Information  
Linux 5.15.0 x86_64

## Distribution
Alpine Linux v3.22

## Recommendations for LLM
- Use these available tools: python3, pip, curl, bash, sh
- For package installation, use: apk
- This is an Alpine Linux system
```

## Configuration

### Environment Variables (.env file)

```bash
# Required: OpenAI API access
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o

# Optional: Docker settings
DOCKER_IMAGE=alpine:latest

# Optional: Execution parameters
MAX_ITERATIONS=10
EXECUTION_TIMEOUT=300
```

### Docker Requirements

Docker is optional but recommended for:
- **Real Tool Execution**: Actual command execution vs simulation
- **Environment Isolation**: Secure execution sandbox
- **Consistent Results**: Predictable tool availability

**Without Docker**: Interpreter runs in simulation mode, providing execution plans and analysis without actual tool execution.

## CLI Usage

### Boot Command
```bash
./llmunix-llm boot
```
Initializes LLMunix operating system with ASCII art welcome and environment setup.

### Execute Command
```bash
# Standard syntax
./llmunix-llm execute: "Your goal description"

# Alternative syntax  
./llmunix-llm execute "Your goal description"
```

### Example Commands

```bash
# Development tasks
./llmunix-llm execute: "Create a REST API using Flask"
./llmunix-llm execute: "Build a web scraper for news websites"

# Research and analysis
./llmunix-llm execute: "Fetch content from https://example.com and create summary"
./llmunix-llm execute: "Research current AI trends and generate report"

# System operations
./llmunix-llm execute: "Set up Python development environment"
./llmunix-llm execute: "Create automated backup script"
```

## Testing

### Test Suite

Run the comprehensive test suite to validate installation:

```bash
python3 test_llm_interpreter.py
```

**Test Coverage:**
- Environment setup and API key validation
- Interpreter initialization and configuration
- Docker availability and container management
- Environment detection capabilities
- Simple goal execution and state management

### Manual Testing

1. **Environment Test**: `./llmunix-llm boot`
2. **Simple Goal**: `./llmunix-llm execute: "Create hello.txt with greeting"`
3. **Web Request**: `./llmunix-llm execute: "Fetch content from https://httpbin.org/json"`
4. **Development Task**: `./llmunix-llm execute: "Create Python script to calculate fibonacci"`

## Error Handling

### Common Issues

**API Key Problems:**
```bash
❌ OpenAI API key not found
💡 Solution: Set OPENAI_API_KEY in .env file
```

**Docker Issues:**
```bash
⚠️  Docker not available - running in simulation mode
💡 Install Docker for real tool execution
```

**Permission Errors:**
```bash
❌ Permission denied: ./llmunix-llm
💡 Solution: chmod +x llmunix-llm
```

### Error Recovery

The interpreter includes intelligent error recovery:

- **API Failures**: Automatic retry with exponential backoff
- **Tool Errors**: LLM analyzes failures and adapts approach
- **Environment Issues**: Graceful degradation to available tools
- **Timeout Handling**: Configurable execution timeouts

## Advanced Features

### Pure Markdown Component System
The interpreter features **markdown-driven execution** where LLM interprets any markdown component:

- **Zero Hardcoded Rules**: Interpreter reads and sends markdown files to LLM for interpretation
- **On-Demand Analysis**: Markdown specifications sent to LLM only when components are called
- **Intelligent Recognition**: Flexible pattern matching for component names and capabilities
- **Automatic Discovery**: Finds all markdown components across the system

```bash
# Components are discovered and analyzed automatically
🔍 Analyzing component: QueryMemoryTool.md
✅ Found component: Query Memory Tool
🔧 Executing markdown component: QueryMemoryTool
```

### Custom Model Selection
```bash
# Use different OpenAI model
OPENAI_MODEL=gpt-4o python3 llm_interpreter.py execute "Your goal"
```

### Docker Customization
```bash
# Use custom Docker image
DOCKER_IMAGE=ubuntu:latest ./llmunix-llm execute: "Your goal"
```

### State Inspection
```bash
# Monitor execution state in real-time
watch -n 1 cat workspace/state/history.md
```

### Debugging Mode
```bash
# Enable verbose logging
DEBUG=1 ./llmunix-llm execute: "Your goal"
```

## Integration

### Programmatic Usage

```python
from llm_interpreter import LLMunixInterpreter

# Initialize interpreter
interpreter = LLMunixInterpreter(model="gpt-4o")

# Execute goal
interpreter.execute("Create data analysis script")

# Access results
summary_path = interpreter.workspace_dir / "execution_summary.md"
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Run LLMunix Task
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: |
    ./llmunix-llm execute: "Generate test report from coverage data"
```

## Comparison with Claude Code Runtime

| Feature | Claude Code Runtime | LLM Interpreter |
|---------|-------------------|-----------------|
| **Execution Style** | Interactive dialogue | Autonomous |
| **User Interaction** | Real-time feedback | Hands-off |
| **Tool Execution** | Claude's native tools | Docker + real commands |
| **Environment Awareness** | Implicit context | Explicit detection |
| **State Management** | Full modular system | Full modular system |
| **Error Recovery** | Interactive problem-solving | Autonomous adaptation |
| **API Dependency** | Claude API | OpenAI API |
| **Setup Requirements** | Claude Code CLI | Python + API key |
| **Docker Requirement** | No | Optional |

Both runtimes execute identical markdown specifications and produce equivalent results.

## Security Considerations

### API Key Management
- Store API keys in `.env` files (not version controlled)
- Use environment variables in production
- Rotate keys regularly for security

### Docker Security
- Containers run with limited privileges
- No host filesystem access by default  
- Automatic cleanup of temporary containers

### Code Execution
- All tool execution happens in isolated containers
- LLM decisions are logged for audit trails
- No arbitrary code execution on host system

## Performance Optimization

### API Usage
- Efficient prompt design to minimize token usage
- Streaming responses for long operations
- Automatic retry logic for reliability

### Docker Performance  
- Image caching for faster container startup
- Resource limits to prevent runaway processes
- Cleanup automation to manage disk usage

### State Management
- Modular file updates for minimal I/O
- JSON for structured data, Markdown for human-readable logs
- Compression for large execution histories

## Troubleshooting

### Debug Information
```bash
# Enable debug mode
DEBUG=1 ./llmunix-llm execute: "Your goal"

# Check Docker status
docker ps -a | grep llmunix

# Inspect state files
ls -la workspace/state/
```

### Log Analysis
```bash
# View execution history
cat workspace/state/history.md

# Check LLM decisions
grep -A 5 -B 5 "LLM Decision" workspace/state/history.md

# Monitor real-time execution
tail -f workspace/state/history.md
```

### Common Solutions

1. **Slow Execution**: Reduce MAX_ITERATIONS or use faster model
2. **High API Costs**: Switch to gpt-4o-mini for simpler tasks
3. **Docker Issues**: Verify Docker daemon is running
4. **Memory Usage**: Monitor container resource usage

## Contributing

The LLM Interpreter is part of the LLMunix framework. Contributions welcome:

1. **Environment Detection**: Add support for new OS distributions
2. **Tool Integration**: Expand available tool mappings
3. **Error Recovery**: Improve autonomous failure handling
4. **Performance**: Optimize LLM prompt efficiency

## License

Same as LLMunix framework - open source with attribution to original contributors.

---

*LLM Interpreter: Autonomous execution of the Pure Markdown Operating System through LLM-driven decision making.*