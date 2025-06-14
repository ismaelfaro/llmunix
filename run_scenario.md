# Execute Summarize Website Scenario

This file provides a clean way to execute the scenario. Simply copy the prompt below and use it with Claude Code.

## Execution Prompt

```
You will act as **SystemAgent**, the master orchestrator of the AGI-DAF. Your logic and instructions are defined in `system/SystemAgent.md`.

Your task is to execute the goal defined in `scenarios/Summarize_website.md`.

Follow your core instructions precisely:
1. Read the user's goal from the scenario file
2. Consult `system/SmartMemory.md` for past learnings
3. Consult `system/SmartLibrary.md` to discover necessary components
4. Formulate a step-by-step plan
5. Execute the plan, using the `workspace/` directory for all file operations
6. When finished, update `system/SmartMemory.md` with a new experience entry

Show your internal monologue (Plan, Action, Observation) as you work, and confirm when the process is complete.
```

## Expected Output

After execution, you should see:
- `workspace/summary_of_example_com.txt` containing the website summary
- Updated `system/SmartMemory.md` with the experience record
- Clear step-by-step execution log

## Clean Restart

To reset for a fresh run:
1. Clear or delete files in `workspace/`
2. Reset `system/SmartMemory.md` to its empty state
3. Execute the scenario again