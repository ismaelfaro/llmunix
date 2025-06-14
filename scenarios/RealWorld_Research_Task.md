# Scenario: Real-World Research Task

## Goal

Conduct real research on current AI developments by fetching live content from Hugging Face's blog, analyzing it, and creating a comprehensive research report with structured summaries and key insights.

## Objective

Demonstrate AGI-OS's real-world capabilities by:
1. Fetching live web content using real HTTP requests
2. Processing and analyzing actual content 
3. Creating structured output with multiple formats
4. Generating training data from real execution

## Task Specification

**Primary Goal**: Research and summarize recent AI developments from https://huggingface.co/blog

**Deliverables**:
1. `workspace/huggingface_blog_content.txt` - Raw fetched content
2. `workspace/ai_research_summary.json` - Structured JSON summary
3. `workspace/ai_research_report.md` - Formatted research report
4. `workspace/execution_trace.json` - Training data from execution

## Expected Workflow

### Phase 1: Real Web Data Acquisition
- Use RealWebFetchTool to fetch live content from Hugging Face blog
- Handle real network latency, errors, rate limits
- Capture actual HTTP response data and metadata

### Phase 2: Real Content Analysis  
- Use RealSummarizationAgent to analyze fetched content
- Generate multiple format outputs (JSON, Markdown)
- Extract key insights, trends, and important announcements

### Phase 3: Real File Operations
- Use RealFileSystemTool for all file operations
- Create structured output files in workspace
- Manage intermediate processing files

### Phase 4: Training Data Generation
- Capture complete execution trace with real tool calls
- Record actual costs, timing, and error handling
- Generate fine-tuning dataset from real execution

## Success Criteria

1. **Real Execution**: All operations use actual Claude Code tools
2. **Live Data**: Content is fetched from real, current web sources  
3. **Error Resilience**: Handles real-world network and system errors
4. **Quality Output**: Produces professional-grade research deliverables
5. **Training Data**: Generates high-quality fine-tuning examples

## Expected Challenges

- **Network Variability**: Real web requests may have timeouts or errors
- **Content Complexity**: Live content requires robust parsing and analysis
- **State Management**: Complex workflow requires careful state tracking
- **Cost Optimization**: Real tools have actual costs that need management

## Performance Targets

- **Total Execution Time**: <5 minutes
- **Content Quality**: >85% accuracy in key information extraction
- **Error Recovery**: Successfully handle at least 1 error scenario
- **Cost Efficiency**: <$0.10 total execution cost

## Training Data Output

Expected training dataset structure:
```json
{
  "execution_id": "real_research_001",
  "scenario": "RealWorld_Research_Task", 
  "total_cost": "$0.067",
  "total_time": "3m 42s",
  "tool_calls": [
    {
      "step": 1,
      "tool": "WebFetch",
      "real_inputs": {"url": "https://huggingface.co/blog"},
      "real_outputs": {"content": "...", "metadata": {...}},
      "performance": {"cost": "$0.012", "time": "8.3s"}
    }
  ],
  "state_transitions": [...],
  "final_outcome": "success",
  "quality_metrics": {...}
}
```

This scenario serves as both a practical demonstration of AGI-OS capabilities and a generator of high-quality training data for developing autonomous AI agents.