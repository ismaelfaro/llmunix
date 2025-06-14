# Execution State Template

This template is used to create `workspace/execution_state.md` for each task execution.

## Template Structure

```markdown
# Execution State: [Goal Title]

## Metadata
- **execution_id**: exec_[timestamp]_[uuid]
- **goal**: [User's original goal]
- **status**: PLANNING | IN_PROGRESS | COMPLETED_SUCCESS | COMPLETED_FAILURE | PAUSED
- **current_step**: [number]
- **start_time**: [ISO timestamp]
- **last_updated**: [ISO timestamp]
- **mode**: SIMULATION | EXECUTION

## Variables
[Dynamic variables that pass data between steps]
- `variable_name`: value
- `file_path`: workspace/output.txt

## Execution Plan
[Numbered steps with metadata]

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

## Execution Log
[Real-time log of step executions]

### Step 1 Execution - [timestamp]
- **tool_used**: [actual Claude Code tool]
- **real_inputs**: [actual parameters]
- **real_outputs**: [actual results]
- **actual_cost**: $X.XX
- **actual_time**: Xs
- **errors**: [any errors encountered]
- **state_changes**: [files created/modified]

## Training Data
[Structured data for fine-tuning - only in EXECUTION mode]
- **conversation_trace**: [full conversation]
- **tool_calls**: [all tool invocations]
- **state_transitions**: [state changes]
- **performance_metrics**: [cost, time, success rate]
```

## State Management Rules

1. **Atomic Updates**: Each step completion updates the entire state
2. **Immutable History**: Past executions are never modified
3. **Variable Propagation**: Outputs become inputs for subsequent steps
4. **Error Isolation**: Failed steps don't corrupt overall state
5. **Resumability**: Execution can pause and resume at any step

## State Transitions

```
PLANNING → IN_PROGRESS → COMPLETED_SUCCESS
    ↓           ↓              ↑
  FAILED ← PAUSED --------→ RESUMED
```

## Usage

1. SystemAgent copies this template to `workspace/execution_state.md`
2. Fills in goal and creates initial plan
3. Updates state after each step execution
4. Records final outcome and training data