# LLMunix Interactive Session

The LLMunix LLM Interpreter now supports an interactive session mode similar to Claude Code, allowing you to refine goals and execute new tasks without terminating the session.

## Getting Started

### Start Interactive Session
```bash
./llmunix-llm interactive
```

### Execute Goal and Enter Interactive Mode
```bash
./llmunix-llm execute: "Create a Python calculator" -i
```

## Interactive Commands

Once in the interactive session, you can use these commands:

### Goal Execution
Simply type any goal to execute it:
```
🎯 llmunix> Create a web scraper for news articles
🎯 llmunix> Build a REST API with FastAPI  
🎯 llmunix> Analyze the data in my workspace
```

### Goal Refinement
Use the `refine` command to improve the last executed goal:
```
🎯 llmunix> refine
Previous goal: Create a web scraper for news articles
How would you like to refine this goal?
🔄 refinement> Add error handling and save to JSON format
```

### Status and Monitoring
- `status` - Show workspace files, state directory, and recent files
- `history` - Display execution history from the current session
- `clear` - Clear workspace with confirmation prompt

### Session Management
- `help` - Show available commands and examples
- `exit` or `quit` - Exit interactive session with cleanup

## Key Features

### Pure Markdown Component System
- **Robust LLM-based parsing**: Any markdown component can be understood and executed
- **On-demand analysis**: Components analyzed only when needed for optimal performance
- **Intelligent recognition**: Flexible pattern matching for component names and types
- **Zero hardcoded rules**: LLM interprets component specifications dynamically

### Persistent Environment
- Docker containers persist across multiple executions within a session
- Workspace state is maintained between commands
- Full execution history and context available throughout session
- Component analysis cache preserved across commands

### Session Context
- Last executed goal is remembered for refinement
- Execution state persists across commands
- Component registry maintained throughout session
- Clean resource management on session exit

### Error Handling
- Graceful handling of Ctrl+C interruption
- Error recovery with helpful guidance
- Safe workspace clearing with confirmation

## Examples

### Complete Workflow
```bash
# Start interactive session
./llmunix-llm interactive

# Execute initial goal
🎯 llmunix> Create a simple web scraper

# Check status
🎯 llmunix> status

# Refine the goal
🎯 llmunix> refine
🔄 refinement> Add beautiful soup parsing and error handling

# Execute new task
🎯 llmunix> Create unit tests for the scraper

# View history
🎯 llmunix> history

# Exit session
🎯 llmunix> exit
```

### One-Shot with Interactive
```bash
# Execute goal and enter interactive mode
./llmunix-llm execute: "Build a FastAPI server" -i

# Now in interactive mode - can refine or add new goals
🎯 llmunix> refine
🔄 refinement> Add database integration with SQLAlchemy

🎯 llmunix> Create documentation for the API

🎯 llmunix> exit
```

## Technical Details

### State Management
- Execution context preserved across commands
- Modular state files updated continuously
- Docker container lifecycle managed efficiently

### Resource Cleanup
- Containers cleaned up only on session exit
- Workspace preserved during session
- Graceful shutdown on interruption

### Integration with LLMunix
- Full compatibility with existing LLMunix features
- SystemAgent delegation for all executions
- Pure markdown component system integration
- Real tool integration maintained
- On-demand component analysis for any markdown file