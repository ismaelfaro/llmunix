# Claude Code Tool Mapping

This file defines how AGI-OS framework components map to Claude Code's native tools and their real-world characteristics.

## Tool Mappings

### WebFetcherTool → WebFetch
```yaml
framework_tool: tool_web_fetcher_v1
claude_tool: WebFetch
parameters:
  url: url
  prompt: "Extract the main content from this webpage"
cost: low ($0.001-0.01 per call)
latency: medium (2-10 seconds)
side_effects: "Network request, may be rate limited"
error_modes: ["timeout", "404", "forbidden", "rate_limit"]
capabilities: ["html_parsing", "text_extraction", "link_following"]
limitations: ["no_javascript", "static_content_only"]
```

### FileWriterTool → Write
```yaml
framework_tool: tool_file_writer_v1
claude_tool: Write
parameters:
  file_path: file_path
  content: content
cost: none
latency: low (<100ms)
side_effects: "Creates/overwrites files in workspace"
error_modes: ["permission_denied", "disk_full", "invalid_path"]
capabilities: ["text_files", "json", "csv", "markdown"]
limitations: ["workspace_only", "text_only"]
```

### FileReaderTool → Read
```yaml
framework_tool: tool_file_reader_v1
claude_tool: Read
parameters:
  file_path: file_path
cost: none
latency: low (<100ms)
side_effects: none
error_modes: ["file_not_found", "permission_denied", "too_large"]
capabilities: ["text_files", "images", "structured_data"]
limitations: ["size_limits", "binary_limited"]
```

### SearchTool → Grep/Glob
```yaml
framework_tool: tool_search_v1
claude_tool: Grep
parameters:
  pattern: pattern
  path: path
  include: include
cost: none
latency: low (<1s)
side_effects: none
error_modes: ["invalid_regex", "permission_denied"]
capabilities: ["regex_search", "file_filtering", "content_search"]
limitations: ["text_only", "repo_scope"]
```

### SystemTool → Bash
```yaml
framework_tool: tool_system_v1
claude_tool: Bash
parameters:
  command: command
  description: description
cost: variable
latency: variable (1s-10min)
side_effects: "Can modify system state, install packages, etc."
error_modes: ["command_not_found", "permission_denied", "timeout"]
capabilities: ["full_system_access", "package_management", "file_operations"]
limitations: ["security_restrictions", "timeout_limits"]
```

### SubTaskTool → Task
```yaml
framework_tool: tool_subtask_v1
claude_tool: Task
parameters:
  description: description
  prompt: prompt
cost: medium (spawns new agent)
latency: high (30s-5min)
side_effects: "Creates parallel execution context"
error_modes: ["task_failure", "context_limit", "infinite_recursion"]
capabilities: ["parallel_execution", "specialized_agents", "complex_workflows"]
limitations: ["context_sharing", "coordination_complexity"]
```

### HumanInTheLoopTool → Interactive Input
```yaml
framework_tool: tool_human_v1
claude_tool: console_interaction
parameters:
  question: question
  context: context
cost: high (human time)
latency: very_high (minutes-hours)
side_effects: "Pauses execution, requires human presence"
error_modes: ["no_response", "ambiguous_input", "unavailable"]
capabilities: ["complex_decisions", "domain_expertise", "approval_workflows"]
limitations: ["availability", "response_time", "scalability"]
```

## Cost Model

### Token Cost Estimates
- **WebFetch**: 1000-5000 tokens per call
- **Read**: 100-2000 tokens per file
- **Write**: 50-500 tokens per operation
- **Grep**: 100-1000 tokens per search
- **Bash**: 200-2000 tokens per command
- **Task**: 5000-50000 tokens per subtask

### Time Estimates
- **Immediate**: <100ms (Read, Write, local Grep)
- **Fast**: 100ms-1s (Bash commands, complex Grep)
- **Medium**: 1-10s (WebFetch, simple Task)
- **Slow**: 10s-1min (complex Bash, large Task)
- **Interactive**: 1min+ (Human input)

### Decision Matrix

**When to use WebFetch vs cached content:**
- Fresh data needed → WebFetch
- Static reference → cached content

**When to use Task vs direct execution:**
- Complex subtask → Task
- Simple operation → direct

**When to use Bash vs native tools:**
- System integration → Bash
- File operations → native tools

## Real-World Constraints

### Rate Limits
- WebFetch: Respectful crawling, avoid hammering
- API calls: Respect service limits
- Token usage: Monitor consumption

### Security
- Bash: Sanitize inputs, avoid dangerous commands
- File operations: Workspace containment
- Network: HTTPS only, validate domains

### Reliability
- Retry logic for transient failures
- Fallback strategies for tool unavailability
- Graceful degradation when tools fail

## Training Data Collection

Each tool call generates training data:
```json
{
  "tool_call": {
    "framework_tool": "tool_web_fetcher_v1",
    "claude_tool": "WebFetch",
    "inputs": {"url": "https://example.com"},
    "outputs": {"content": "..."},
    "metadata": {
      "cost": "$0.003",
      "latency": "2.4s",
      "success": true,
      "errors": []
    }
  }
}
```

This mapping enables AGI-OS to make intelligent tool choices based on real performance characteristics while generating high-quality training data.