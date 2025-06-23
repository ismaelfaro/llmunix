# Scenario: News Analysis Pipeline Test

**Type**: Real-world execution test for LLM Interpreter
**Goal**: Demonstrate dynamic agent/tool creation and modification for news analysis
**Mode**: EXECUTION MODE (with LLM Interpreter runtime)

## Objective

Create an automated news analysis pipeline that:
1. Fetches content from multiple news sources 
2. Analyzes sentiment and extracts key information
3. Creates a comparative analysis report
4. Tests the system's ability to create and modify components during execution

## Test Requirements

### Phase 1: Basic Tool Usage
- Use existing `RealWebFetchTool` to fetch news content
- Use existing `RealSummarizationAgent` to process articles
- Verify markdown specifications are properly interpreted

### Phase 2: Dynamic Component Creation
- Create a new `NewsAnalysisAgent` during execution
- Create a new `SentimentAnalysisTool` as needed
- Test modification of existing tools to handle edge cases

### Phase 3: Adaptive Behavior
- Demonstrate constraint adaptation based on execution results
- Show memory-driven decision making
- Test error recovery and component evolution

## Input Sources

```yaml
news_sources:
  - name: "TechCrunch AI"
    url: "https://techcrunch.com/category/artificial-intelligence/"
    focus: "AI developments"
  - name: "Reuters Technology"  
    url: "https://www.reuters.com/technology/"
    focus: "Tech business news"
  - name: "BBC Technology"
    url: "https://www.bbc.com/news/technology"
    focus: "General tech news"
```

## Expected Component Evolution

### New Components to Create:

1. **NewsAnalysisAgent.md**
   - Input: Multiple article summaries
   - Output: Comparative analysis with trends
   - Logic: Cross-reference topics, identify patterns

2. **SentimentAnalysisTool.md**
   - Input: Article text
   - Output: Sentiment scores (positive/negative/neutral)
   - Logic: Keyword analysis and tone detection

3. **TrendDetectionTool.md** (if needed)
   - Input: Historical news data
   - Output: Emerging trend identification
   - Logic: Pattern recognition across time periods

### Modifications to Test:

1. **RealWebFetchTool** enhancement for handling rate limits
2. **RealSummarizationAgent** adaptation for news-specific formatting
3. **SystemAgent** constraint updates based on news analysis requirements

## Success Criteria

### Technical Success:
- [ ] Successfully interprets existing markdown tool definitions
- [ ] Creates new agent/tool markdown files during execution
- [ ] Modifies existing components when needed
- [ ] Maintains modular state architecture
- [ ] Generates structured training data

### Functional Success:
- [ ] Fetches real content from all 3 news sources
- [ ] Generates meaningful summaries for each article
- [ ] Produces comparative analysis across sources
- [ ] Adapts to any fetch failures or rate limits
- [ ] Creates final report in structured format

### Adaptive Behavior Success:
- [ ] Shows constraint adaptation during execution
- [ ] Demonstrates memory consultation for decisions
- [ ] Handles errors gracefully with component evolution
- [ ] Updates behavioral constraints based on execution events

## Expected Output Structure

```
workspace/
├── state/
│   ├── plan.md              # Execution steps and progress
│   ├── context.md           # Knowledge accumulation
│   ├── variables.json       # Data passing between steps
│   ├── history.md           # Complete execution log
│   └── constraints.md       # Behavioral adaptations
├── news_content/
│   ├── techcrunch_ai.html   # Raw fetched content
│   ├── reuters_tech.html    
│   └── bbc_technology.html
├── summaries/
│   ├── techcrunch_summary.json
│   ├── reuters_summary.json
│   └── bbc_summary.json
├── analysis/
│   ├── sentiment_analysis.json
│   ├── trend_detection.json
│   └── comparative_report.md
└── training_data/
    └── execution_trace.json  # Complete execution trace for training
```

## Test Execution Command

For LLM Interpreter runtime:
```bash
./llmunix-llm execute: "Act as SystemAgent and execute the NewsAnalysis_InterpreterTest scenario"
```

For Claude Code runtime:
```bash
boot llmunix
llmunix execute: "Act as SystemAgent and execute the NewsAnalysis_InterpreterTest scenario"
```

## Component Creation Testing

### Phase A: Use Existing Components
1. SystemAgent reads this scenario
2. Consults SmartLibrary.md for available components
3. Plans execution using existing RealWebFetchTool and RealSummarizationAgent
4. Executes basic fetch and summarize workflow

### Phase B: Dynamic Component Creation
1. SystemAgent identifies need for sentiment analysis capability
2. Creates `components/tools/SentimentAnalysisTool.md` with proper specification
3. Updates `system/SmartLibrary.md` to register new component
4. Uses new component in subsequent execution steps

### Phase C: Component Modification
1. Encounters rate limiting or parsing issues
2. Modifies existing RealWebFetchTool.md to handle edge case
3. Updates execution approach using modified component
4. Documents adaptation in constraints.md and memory_log.md

## Error Scenarios to Test

1. **Network failures**: Test tool adaptation and retry logic
2. **Content parsing errors**: Test agent modification for different formats
3. **Rate limiting**: Test delay injection and alternative sources
4. **Component not found**: Test dynamic component creation
5. **Low confidence results**: Test human-in-loop integration

## Expected Learning Outcomes

1. **Component Flexibility**: Markdown definitions are interpreted and can be created/modified during runtime
2. **Adaptive Execution**: System adapts constraints and behavior based on execution events
3. **Memory Integration**: Past experiences influence current decision making
4. **Training Data Generation**: Complete execution traces suitable for fine-tuning
5. **Error Resilience**: Intelligent error recovery using component evolution

## Validation Points

### During Execution:
- Monitor constraint evolution in `constraints.md`
- Check component creation timestamps and modification logs
- Verify tool call patterns match markdown specifications
- Confirm modular state updates after each step

### Post Execution:
- Analyze training data quality and completeness
- Review memory log entries for learning insights
- Validate final output quality and structure
- Check component registry updates in SmartLibrary.md

This scenario thoroughly tests the LLM interpreter's ability to use, create, and modify markdown-defined components while maintaining the pure markdown operating system philosophy.