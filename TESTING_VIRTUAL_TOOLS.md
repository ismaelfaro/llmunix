# Testing Virtual Tools with Updated Gemini CLI

This guide explains how to test the new **Virtual Tools** feature that has been added to Gemini CLI. Virtual Tools allow you to define custom tools directly in `GEMINI.md` files using shell scripts and JSON schemas.

## What Are Virtual Tools?

Virtual Tools are custom tools defined directly in your project's `GEMINI.md` file. They consist of:
- A shell script that executes when the tool is called
- A JSON schema that defines the tool's parameters
- Automatic discovery and registration by Gemini CLI

The LLMunix project already uses this pattern extensively in its `GEMINI.md` file with tools like `run_agent`, `write_file`, `read_file`, etc.

## Prerequisites

### 1. Set up the Updated Gemini CLI

Since the Virtual Tools feature is a new addition, you'll need to use the updated version of Gemini CLI:

```bash
# Navigate to the gemini-cli project (adjacent to llmunix)
cd ../gemini-cli

# Install dependencies
npm install

# Build the updated CLI with Virtual Tools support
npm run build

# Optional: Build with sandbox support (recommended)
npm run build:all
```

### 2. Link the Updated CLI (Optional but Recommended)

To use the updated Gemini CLI globally without affecting your system installation:

```bash
# From the gemini-cli directory
npm link packages/cli

# Or create an alias for this specific version
alias gemini-dev="node ../gemini-cli/packages/cli/dist/index.js"
```

### 3. Environment Setup

Ensure you have the necessary environment variables:

```bash
# Required: Your Gemini API key
export GEMINI_API_KEY="your-api-key-here"

# Optional: Enable sandboxing for better security
export GEMINI_SANDBOX=true

# Optional: Add to ~/.env file for persistence
echo "GEMINI_API_KEY=your-api-key-here" >> ~/.env
echo "GEMINI_SANDBOX=true" >> ~/.env
```

## Testing Virtual Tools Discovery

### Test 1: Verify Tool Discovery

First, let's verify that the virtual tools in LLMunix's `GEMINI.md` are properly discovered:

```bash
# From the llmunix directory
cd ../llmunix

# Start Gemini CLI and check if virtual tools are loaded
# You should see messages about registering virtual tools during startup
gemini
```

**Expected behavior:**
- During startup, you should see console messages like:
  ```
  [ToolRegistry] Registered virtual tool 'run_agent' from GEMINI.md manifest.
  [ToolRegistry] Registered virtual tool 'write_file' from GEMINI.md manifest.
  [ToolRegistry] Registered virtual tool 'read_file' from GEMINI.md manifest.
  ...
  ```

### Test 2: Basic Tool Functionality

Test a simple virtual tool to ensure it works:

```bash
# In the Gemini CLI prompt, try using a virtual tool
> Use the read_file tool to read the README.md file
```

**Expected behavior:**
- The CLI should prompt for confirmation (virtual tools require user approval)
- After approval, it should execute the shell script and return the file contents

### Test 3: Complex Tool with Arguments

Test a more complex tool that uses JSON arguments:

```bash
# Test the write_file tool
> Use the write_file tool to create a test file called "test.txt" with content "Hello Virtual Tools!"
```

**Expected behavior:**
- Confirmation prompt showing the tool execution details
- Successful file creation
- Confirmation message: "Success: Wrote to test.txt"

## Testing the LLMunix Workflow

### Test 4: Full LLMunix Agent Execution

Now test the complete LLMunix workflow with virtual tools:

```bash
# 1. Boot the LLMunix system
./llmunix-boot

# 2. Start Gemini CLI (should auto-detect GEMINI.md and load virtual tools)
gemini

# 3. Give it a simple goal to test agent orchestration
> Create a simple plan for organizing a tech meetup and save it to workspace/meetup_plan.md
```

**Expected behavior:**
- SystemAgent should use the `write_file` virtual tool to create the plan
- The tool should execute successfully within the sandbox
- The file should be created in the workspace directory

### Test 5: Agent-to-Agent Communication

Test the `run_agent` virtual tool that enables agent orchestration:

```bash
# In the Gemini CLI prompt
> Use the run_agent tool to execute the SummarizationAgent with a request to summarize the current README.md file
```

**Expected behavior:**
- The `run_agent` tool should execute successfully
- It should spawn a sub-process with the agent's markdown "firmware"
- The sub-agent should have access to the same virtual tools

## Debugging and Troubleshooting

### Common Issues and Solutions

#### 1. Virtual Tools Not Discovered

**Symptoms:** No messages about registering virtual tools during startup.

**Debug steps:**
```bash
# Check if GEMINI.md exists and has the ### Tools section
grep -n "### Tools" GEMINI.md

# Check for syntax errors in tool definitions
# Look for missing sh or json code blocks
```

**Solution:** Ensure your `GEMINI.md` has properly formatted tool definitions with both `sh` and `json` code blocks.

#### 2. Tool Execution Fails

**Symptoms:** Tool fails with "command not found" or similar errors.

**Debug steps:**
```bash
# Check if required dependencies are available in the sandbox
# For example, jq is required for JSON parsing in LLMunix tools
which jq

# If using Docker/Podman sandbox, check if tools are available inside
docker run --rm -it <sandbox-image> which jq
```

**Solution:** Ensure required dependencies (like `jq`) are available in your execution environment.

#### 3. Permission Errors

**Symptoms:** Tools fail with permission denied errors.

**Debug steps:**
```bash
# Check sandbox permissions
ls -la workspace/

# Check if sandbox is restricting file operations
```

**Solution:** Adjust sandbox configuration or use relative paths within the project directory.

#### 4. JSON Parsing Errors

**Symptoms:** Error messages about invalid JSON in tool definitions.

**Debug steps:**
```bash
# Validate JSON syntax in your tool definitions
# Extract and test JSON blocks individually
jq '.' <<< '{"name": "your_tool", ...}'
```

**Solution:** Fix JSON syntax errors in your tool schemas.

## Advanced Testing

### Test 6: Custom Tool Creation

Create your own virtual tool to test the system:

```bash
# Add this to your GEMINI.md file under ### Tools

#### test_echo

```sh
MESSAGE=$(echo "$GEMINI_TOOL_ARGS" | jq -r '.message')
echo "Echo: $MESSAGE"
```

```json
{
  "name": "test_echo",
  "description": "A simple echo tool for testing",
  "parameters": {
    "type": "object",
    "properties": {
      "message": {
        "type": "string",
        "description": "Message to echo"
      }
    },
    "required": ["message"]
  }
}
```
```

Then restart Gemini CLI and test:
```bash
> Use the test_echo tool with message "Virtual tools are working!"
```

### Test 7: Error Handling

Test how the system handles malformed tools:

```bash
# Add a tool with invalid JSON to test error handling
# The system should log a warning and skip the invalid tool
```

### Test 8: Multiple Tool Execution

Test chaining multiple virtual tools:

```bash
> First use write_file to create a note, then use read_file to read it back
```

## Performance Considerations

### Monitoring Tool Performance

```bash
# Monitor tool execution time
time gemini -p "Use the read_file tool to read README.md"

# Check memory usage during tool execution
# Look for any memory leaks or excessive resource usage
```

### Sandbox Overhead

```bash
# Compare performance with and without sandboxing
GEMINI_SANDBOX=false gemini  # Run without sandbox
GEMINI_SANDBOX=true gemini   # Run with sandbox
```

## Validation Checklist

Use this checklist to verify the Virtual Tools implementation:

- [ ] **Discovery**: Virtual tools are discovered and registered on startup
- [ ] **Validation**: Tool parameters are validated against JSON schemas  
- [ ] **Execution**: Shell scripts execute correctly with `GEMINI_TOOL_ARGS`
- [ ] **Security**: Tools require user confirmation before execution
- [ ] **Sandboxing**: Tools execute within the configured sandbox environment
- [ ] **Error Handling**: Invalid tools are gracefully skipped with appropriate warnings
- [ ] **Integration**: Virtual tools work alongside built-in tools seamlessly
- [ ] **Performance**: Tool execution has reasonable performance characteristics
- [ ] **LLMunix Compatibility**: All existing LLMunix agents continue to work
- [ ] **Agent Orchestration**: The `run_agent` tool enables proper agent-to-agent communication

## Contributing Test Cases

If you find issues or want to add test cases:

1. **Document the Issue**: Include exact steps to reproduce
2. **Provide Logs**: Include relevant console output and error messages  
3. **Test Environment**: Specify your OS, Node version, and sandbox configuration
4. **Expected vs Actual**: Clearly describe what should happen vs what actually happens

## Next Steps

Once you've verified that Virtual Tools are working correctly:

1. **Explore the Documentation**: Read `/docs/tools/virtual-tools.md` for comprehensive documentation
2. **Create Custom Tools**: Experiment with your own tool definitions
3. **Integrate with Projects**: Add virtual tools to your own projects' `GEMINI.md` files
4. **Share Feedback**: Report any issues or suggestions for improvement

The Virtual Tools feature opens up powerful possibilities for extending Gemini CLI with project-specific functionality, and LLMunix serves as an excellent test case for this new capability.