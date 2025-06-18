# State Directory Template

This template defines the new modular execution state structure that replaces the monolithic `execution_state.md`.

## Architecture: Modular State Management

The execution state is now split into focused, specialized files within `workspace/state/`:

```
workspace/state/
├── plan.md              # Execution plan and step definitions
├── context.md           # Knowledge accumulation and insights
├── variables.json       # Structured key-value data
├── history.md           # Append-only execution log
└── constraints.md       # Behavioral modifiers and sentient state
```

## File Templates

### plan.md
```markdown
# Execution Plan: [Goal Title]

## Metadata
- **execution_id**: exec_[timestamp]_[uuid]
- **goal**: [User's original goal]
- **status**: PLANNING | IN_PROGRESS | COMPLETED_SUCCESS | COMPLETED_FAILURE | PAUSED
- **current_step**: [number]
- **start_time**: [ISO timestamp]
- **last_updated**: [ISO timestamp]
- **mode**: SIMULATION | EXECUTION

## Steps

### Step 1: [Action Name]
- **component**: [component_id from SmartLibrary]
- **tool_mapping**: [Claude Code tool if EXECUTION mode]
- **status**: PENDING | RUNNING | COMPLETED | FAILED
- **inputs**: 
  - param1: value or {{variable_reference}}
- **expected_outputs**:
  - result: description
- **estimated_cost**: $X.XX
- **estimated_time**: Xs
- **side_effects**: [description]

### Step 2: [Action Name]
[... continue for all planned steps]
```

### context.md
```markdown
# Execution Context: [Goal Title]

## Knowledge Accumulation
[Summaries, insights, and key findings gathered during execution]

### Web Content Summaries
[Summaries of fetched web pages, extracted data]

### Document Analysis Results
[Key insights from analyzed documents]

### Key Findings
[Important discoveries that influence subsequent steps]

## Current Understanding
[Agent's evolving understanding of the task and domain]

## Decision Rationale
[Explanations for major decisions made during execution]
```

### variables.json
```json
{
  "execution_metadata": {
    "execution_id": "exec_[timestamp]_[uuid]",
    "goal": "[User's original goal]",
    "mode": "EXECUTION|SIMULATION"
  },
  "step_data": {
    "current_step": 1,
    "total_steps": 5
  },
  "file_paths": {
    "output_file": "workspace/research_summary.md",
    "temp_dir": "workspace/temp/"
  },
  "extracted_data": {
    "urls_processed": [],
    "key_metrics": {},
    "flags": {}
  },
  "cost_tracking": {
    "total_cost": 0.0,
    "step_costs": []
  }
}
```

### history.md
```markdown
# Execution History: [Goal Title]

## Step Execution Log

### Step 1 Execution - [timestamp]
- **component_used**: [component name]
- **tool_used**: [actual Claude Code tool]
- **real_inputs**: [actual parameters]
- **real_outputs**: [actual results]
- **actual_cost**: $X.XX
- **actual_time**: Xs
- **errors**: [any errors encountered]
- **state_changes**: [files created/modified]
- **notes**: [any observations or insights]

### Step 2 Execution - [timestamp]
[... continue chronologically]

## Training Data Collection
[Structured data for fine-tuning - only in EXECUTION mode]
- **conversation_trace**: [full conversation snippets]
- **tool_calls**: [all tool invocations with results]
- **state_transitions**: [state changes between steps]
- **performance_metrics**: [cost, time, success rate]
```

### constraints.md (Core of Sentient State)
```markdown
# Execution Constraints: [Goal Title]

## Behavioral Modifiers
- **user_sentiment**: "neutral" | "pleased" | "frustrated" | "impatient"
- **priority**: "speed_and_clarity" | "comprehensiveness" | "cost_efficiency" | "quality"
- **max_cost_per_task**: 0.50
- **human_review_trigger_level**: "low" | "medium" | "high"
- **active_persona**: "concise_assistant" | "detailed_analyst" | "proactive_collaborator"
- **error_tolerance**: "strict" | "moderate" | "flexible"

## Resource Constraints
- **max_execution_time**: 300 seconds
- **max_file_operations**: 20
- **max_web_requests**: 5
- **preferred_tools**: ["WebFetch", "Read", "Write"]

## Active Directives
[Dynamic behavioral rules that evolve during execution]
- For the next 2 steps, prioritize tools with lower latency
- Do not generate any new components unless explicitly approved
- Provide brief, bulleted summaries instead of long paragraphs
- If sentiment drops to "frustrated", immediately seek human guidance

## Adaptation Rules
[Rules for self-modification of constraints]
- If 2+ consecutive steps fail → set human_review_trigger_level to "low"
- If user provides positive feedback → set user_sentiment to "pleased"
- If cost exceeds 80% of budget → set priority to "cost_efficiency"
- If execution time > 200s → set priority to "speed_and_clarity"

## Context-Aware Behaviors
[Behaviors that adapt based on task type or domain]
- **legal_tasks**: Increase error_tolerance to "strict", require human review
- **creative_tasks**: Set active_persona to "proactive_collaborator"
- **research_tasks**: Set priority to "comprehensiveness"
- **debugging_tasks**: Set human_review_trigger_level to "medium"
```

## State Management Rules

1. **Atomic File Updates**: Each file can be updated independently
2. **Cross-File Consistency**: Variables in variables.json can be referenced in other files
3. **Immutable History**: history.md is append-only
4. **Dynamic Constraints**: constraints.md can be modified by the agent during execution
5. **Resumability**: State can be reconstructed from all files

## State Transitions

```
PLANNING → IN_PROGRESS → COMPLETED_SUCCESS
    ↓           ↓              ↑
  FAILED ← PAUSED --------→ RESUMED
```

## Usage

1. SystemAgent creates `workspace/state/` directory
2. Initializes all files using these templates
3. Reads constraints.md before planning to understand behavioral context
4. Updates individual files as needed during execution
5. Uses variables.json for data passing between steps
6. Accumulates knowledge in context.md
7. Logs all actions in history.md
8. Adapts constraints.md based on execution events

## Benefits of Modular State

- **Focused Updates**: Agent only reads/writes relevant state files
- **Reduced Token Usage**: Smaller, targeted file operations
- **Enhanced Traceability**: Clear separation of concerns
- **Sentient Behavior**: constraints.md enables true behavioral adaptation
- **Better Error Recovery**: Isolated state components reduce corruption risk