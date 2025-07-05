# Virtual Company Demo: AI-Driven Marketing Campaign

This example demonstrates how LLMunix's memory and messaging systems enable a virtual company to create a complete marketing campaign through autonomous agent collaboration.

## Demo Goal

```
> Create a comprehensive marketing campaign for "EcoFlow Pro" - a new sustainable water purification device. 
> I need market analysis, target audience definition, blog post, ad copy, and social media strategy.
```

## Expected Execution Flow

### 1. SystemAgent Initialization
The SystemAgent begins by:
- Creating a detailed plan in `workspace/state/plan.md`
- Checking available agents in `components/agents/`
- Broadcasting the project kickoff

```
broadcast_message(
  message="New campaign project: EcoFlow Pro water purifier. All agents prepare for assignments.",
  topic="company_updates"
)
```

### 2. CEO Agent Activation
SystemAgent delegates strategic planning:

```
run_agent(
  path="components/agents/CEOAgent.md",
  arguments={
    "task": "Set strategic priorities for EcoFlow Pro campaign",
    "context": "Sustainable water purification device, need full marketing campaign"
  }
)
```

The CEO Agent:
- Stores strategic vision in permanent memory
- Sends high-priority directives to each agent
- Sets success metrics

### 3. Market Research Phase
The CEO sends a message to the Market Analyst:

```
send_message(
  to="MarketAnalystAgent",
  from="CEOAgent",
  message="Priority research needed: 1) Water purification market size 2) Competitor analysis 3) Sustainability trends 4) Target demographics",
  priority="high"
)
```

Market Analyst Agent:
- Fetches data using `web_fetch` and `google_search`
- Consults local LLMs for trend analysis
- Stores findings:
  ```
  memory_store(type="permanent", key="water_purification_market_2024", value="Market size: $XX billion...")
  memory_store(type="task", key="competitor_analysis", value="Top 3 competitors: ...")
  ```
- Sends comprehensive report to CEO and broadcasts key findings

### 4. Content Creation Phase
Content Writer receives directives and market data:

```
check_messages(agent="ContentWriterAgent")
memory_recall(type="task", key="competitor_analysis")
memory_search(pattern="sustainability trends")
```

Creates multiple content pieces:
- Blog post: "5 Ways EcoFlow Pro Revolutionizes Home Water Purification"
- Ad copy variations for different platforms
- Social media content calendar

Each draft is stored in task memory and sent for review:
```
send_message(
  to="QAReviewAgent",
  message="Blog post draft ready for review. Word count: 1200. Focus keywords: sustainable water, purification technology",
  priority="normal"
)
```

### 5. Quality Assurance Phase
QA Review Agent:
- Retrieves content and source data
- Performs multi-level review
- Sends feedback or approval

Example feedback:
```
send_message(
  to="ContentWriterAgent",
  message="Blog post review complete. Issues found: 1) Claim about '99.9% purification' needs source 2) Add CTA in conclusion. Otherwise excellent work!",
  priority="normal"
)
```

### 6. Final Compilation
SystemAgent:
- Monitors all agent communications
- Tracks task completion via memory
- Compiles final deliverables in `workspace/outputs/`

Final output structure:
```
workspace/outputs/
├── ecoflow_campaign_brief.md
├── market_analysis_report.md
├── blog_post_final.md
├── ad_copy_variations.md
├── social_media_strategy.md
└── campaign_metrics.md
```

## Memory Evolution Throughout Execution

### Permanent Memory Growth
- Market insights that inform future campaigns
- Successful content templates
- Brand voice examples

### Task Memory Lifecycle
- Active during campaign creation
- Contains drafts, feedback, iterations
- Cleared after project completion

### Volatile Memory Usage
- Temporary calculations
- API responses
- Inter-agent coordination data

## Communication Patterns Observed

1. **Hierarchical Flow**: CEO → Department Agents → SystemAgent
2. **Peer Review**: Writer ↔ QA circular feedback
3. **Broadcast Updates**: Major milestones shared system-wide
4. **Priority Escalation**: Issues bubble up to CEO when needed

## Demonstration Command Sequence

```bash
# 1. Boot the system
./llmunix-boot

# 2. Start Gemini CLI
gemini

# 3. Provide the goal
> Create a comprehensive marketing campaign for "EcoFlow Pro" - a new sustainable water purification device. 
> I need market analysis, target audience definition, blog post, ad copy, and social media strategy.

# 4. Watch the agents collaborate autonomously
# The system will show real-time message passing, memory updates, and content creation
```

## Key Insights

This demo showcases:
- **Autonomous Coordination**: Agents work together without human intervention
- **Memory-Driven Intelligence**: Past learnings improve future performance
- **Scalable Architecture**: Easy to add new agent types (Legal, Finance, etc.)
- **Transparent Operations**: All decisions traceable through messages and memory
- **Real Business Value**: Produces professional-quality marketing materials

The Virtual Company demonstrates that LLMunix isn't just a technical curiosity—it's a practical framework for building AI systems that can handle complex, real-world business processes.