# LLC Protocol Specification
## LLM Communication Language for Agent Interoperability

### Protocol Overview
LLC (LLM Communication Language) is a hybrid protocol combining structured markdown with embedded code blocks for optimal context passing between AI agents. It enables efficient, type-safe, and semantically rich inter-agent communication.

### Core Design Principles
1. **Context Efficiency**: Minimal token overhead with maximum semantic density
2. **Type Safety**: Structured data with validation and error handling
3. **Human Readability**: Natural language descriptions with embedded data
4. **Composability**: Modular message components for complex workflows
5. **Backward Compatibility**: Fallback to pure markdown for unsupported systems

### LLC Message Structure

```llc
@protocol: LLC/1.0
@from: AgentID
@to: AgentID | broadcast
@priority: low | medium | high | critical
@type: request | response | notification | heartbeat

# Message Title
Brief natural language description of the message purpose.

## Context Block
```context
domain: string
task_type: enum[analysis, transformation, query, action]
confidence: float[0.0-1.0]
dependencies: [AgentID]
resources: {
  memory_required: MB,
  cpu_intensive: boolean,
  external_apis: [string]
}
```

## Data Block
```data
{
  "structured_payload": "JSON or YAML",
  "metadata": {
    "timestamp": "ISO8601",
    "version": "semver",
    "checksum": "hash"
  }
}
```

## Actions Block
```actions
- name: action_name
  parameters: {key: value}
  expected_output: type_definition
  error_handling: strategy
```

## Response Block (for responses only)
```response
status: success | partial | failure | retry
execution_time: milliseconds
resource_usage: {
  tokens_used: integer,
  memory_peak: MB,
  external_calls: integer
}
result: structured_data
errors: [error_objects]
```

@end
```

### Message Types

#### 1. Request Messages
For agent-to-agent task requests with full context and expectations.

#### 2. Response Messages  
Structured responses with execution metadata and results.

#### 3. Notification Messages
Broadcast updates about state changes or system events.

#### 4. Heartbeat Messages
Lightweight status updates for distributed agent coordination.

### Context Optimization Features

1. **Semantic Compression**: High-level descriptions reduce token count
2. **Incremental Updates**: Delta messages for state changes
3. **Context Inheritance**: Reference previous messages to avoid repetition  
4. **Lazy Loading**: Optional deep context fetched on-demand
5. **Type Inference**: Smart defaults reduce explicit type annotations

### Error Handling

```llc
@protocol: LLC/1.0
@type: response
@from: ProcessorAgent
@to: CoordinatorAgent

# Task Execution Failed

## Context Block
```context
domain: data_processing
task_type: transformation
confidence: 0.0
error_category: validation_error
```

## Response Block
```response
status: failure
execution_time: 1250
resource_usage: {
  tokens_used: 3421,
  memory_peak: 45,
  external_calls: 0
}
errors: [
  {
    code: "INVALID_INPUT_FORMAT",
    message: "Expected JSON array, received string",
    context: "line 42, column 15",
    recovery_suggestion: "validate_input_format"
  }
]
```

@end
```

### Security Considerations

1. **Message Signing**: Optional cryptographic signatures for sensitive communications
2. **Access Control**: Agent capability declarations and permission checks
3. **Rate Limiting**: Built-in throttling for resource protection
4. **Audit Trail**: Message logging for debugging and compliance

### Implementation Notes

- LLC messages are UTF-8 encoded with .llc extension
- Parsers should gracefully degrade to markdown for compatibility
- Context blocks are optional but recommended for complex workflows
- All timestamps use ISO8601 format with UTC timezone
- Resource usage tracking is mandatory for system optimization