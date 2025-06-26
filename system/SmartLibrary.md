# Smart Library Index

This file is the central registry for all components available to the SystemAgent. Components marked with [REAL] use Claude Code's native tools for actual execution.

## LLM-OS Real Components

---
-   **id**: `tool_real_web_fetch_v1`
-   **name**: RealWebFetchTool [REAL]
-   **file_path**: `components/tools/RealWebFetchTool.md`
-   **record_type**: REAL_TOOL
-   **claude_tool**: WebFetch
-   **domain**: data_acquisition
-   **description**: Fetches real, live content from web URLs using Claude Code's WebFetch capability.
-   **cost**: low ($0.001-0.01 per call)
-   **latency**: medium (2-10 seconds)
-   **side_effects**: "Network request to external server"
-   **version**: 1.0.0
-   **tags**: [web, fetch, http, real, claude-code]
-   **applicability_text**: "Use for fetching real, live web content. Replaces simulation-based web fetching with actual HTTP requests. Ideal for current data, news, articles, and dynamic content that cannot be mocked."

---
-   **id**: `tool_real_filesystem_v1`
-   **name**: RealFileSystemTool [REAL]
-   **file_path**: `components/tools/RealFileSystemTool.md`
-   **record_type**: REAL_TOOL
-   **claude_tool**: Read, Write, Glob, LS
-   **domain**: file_system
-   **description**: Performs real file system operations using Claude Code's native file tools.
-   **cost**: none
-   **latency**: low (<100ms)
-   **side_effects**: "Creates/modifies/reads real files in workspace"
-   **version**: 1.0.0
-   **tags**: [file, read, write, search, real, claude-code]
-   **applicability_text**: "Use for all file operations including reading, writing, searching, and listing. Provides real file system access with workspace security boundaries. Essential for persistent data storage and file-based workflows."

---
-   **id**: `agent_real_summarizer_v1`
-   **name**: RealSummarizationAgent [REAL]
-   **file_path**: `components/agents/RealSummarizationAgent.md`
-   **record_type**: REAL_AGENT
-   **domain**: text_processing
-   **description**: Advanced summarization agent that reads real files and generates structured summaries using Claude Code's native capabilities.
-   **cost**: medium (depends on content length)
-   **latency**: medium (5-30 seconds)
-   **side_effects**: "May create intermediate analysis files"
-   **version**: 1.0.0
-   **tags**: [summary, nlp, real, multi-format, claude-code]
-   **applicability_text**: "Use for comprehensive text summarization from files, URLs, or direct text input. Supports multiple output formats (JSON, Markdown, Plain) and quality metrics. Ideal for document analysis, content extraction, and report generation."

---
-   **id**: `agent_memory_analysis_v1`
-   **name**: MemoryAnalysisAgent [REAL]
-   **file_path**: `components/agents/MemoryAnalysisAgent.md`
-   **record_type**: REAL_AGENT
-   **claude_tool**: Read, Grep, Bash
-   **domain**: memory_management
-   **description**: Intelligent memory querying agent that analyzes historical task executions to provide insights and recommendations.
-   **cost**: low ($0.01-0.03 per query)
-   **latency**: medium (2-5 seconds)
-   **side_effects**: "None - read-only memory analysis"
-   **version**: 1.0.0
-   **tags**: [memory, analysis, learning, patterns, real, claude-code]
-   **applicability_text**: "Use for learning from past experiences, identifying successful patterns, detecting failure modes, and generating behavioral recommendations. Essential for adaptive execution and continuous improvement."

---
-   **id**: `tool_query_memory_v1`
-   **name**: QueryMemoryTool [REAL]
-   **file_path**: `components/tools/QueryMemoryTool.md`
-   **record_type**: REAL_TOOL
-   **claude_tool**: Read, Grep, Bash
-   **domain**: memory_management
-   **description**: Bridge tool that enables SystemAgent to query memory through MemoryAnalysisAgent with standardized interface.
-   **cost**: low ($0.01-0.03 per query)
-   **latency**: medium (2-5 seconds)
-   **side_effects**: "May cache query results temporarily"
-   **version**: 1.0.0
-   **tags**: [memory, query, bridge, learning, real, claude-code]
-   **applicability_text**: "Use during planning and error recovery to consult past experiences. Provides actionable insights for constraint adaptation, component selection, and strategy optimization based on historical performance."

---
-   **id**: `tool_llc_parser_v1`
-   **name**: LLC_Parser [REAL]
-   **file_path**: `components/tools/LLC_Parser.md`
-   **record_type**: REAL_TOOL
-   **claude_tool**: Read, Write, Grep, Glob
-   **domain**: communication
-   **description**: Parses, validates, and generates LLC (LLM Communication Language) messages for optimal agent-to-agent communication.
-   **cost**: low ($0.001-0.005 per message)
-   **latency**: low (<500ms)
-   **side_effects**: "Creates/reads .llc message files"
-   **version**: 1.0.0
-   **tags**: [communication, protocol, parsing, llc, agent-messages, real, claude-code]
-   **applicability_text**: "Use for all internal agent-to-agent communication. Provides context-efficient, type-safe message passing with 48% token reduction vs traditional approaches. Essential for coordinating multi-agent workflows and maintaining structured communication context."

---
-   **id**: `tool_hackernews_summary_v1`
-   **name**: HackerNewsSummaryTool [REAL]
-   **file_path**: `components/tools/HackerNewsSummaryTool.md`
-   **record_type**: REAL_TOOL
-   **claude_tool**: WebFetch, Read, Write
-   **domain**: data_acquisition
-   **description**: Fetches and summarizes trending stories from Hacker News, providing structured summaries with key insights and discussion metrics.
-   **cost**: medium ($0.01-0.05 per execution)
-   **latency**: medium (5-15 seconds)
-   **side_effects**: "Creates summary files in workspace"
-   **version**: 1.0.0
-   **tags**: [hackernews, news, summary, trending, real, claude-code]
-   **applicability_text**: "Use for staying current with tech industry trends and discussions. Provides filtered, structured summaries of top Hacker News stories with trending topic analysis. Ideal for research, competitive intelligence, and tech news monitoring."

---
-   **id**: `agent_data_coordinator_v1`
-   **name**: DataCoordinatorAgent [REAL]
-   **file_path**: `components/agents/DataCoordinatorAgent.md`
-   **record_type**: REAL_AGENT
-   **claude_tool**: Read, Write, Grep, Glob, Task, Bash
-   **domain**: orchestration
-   **description**: Coordinates complex data processing workflows by orchestrating multiple specialized agents through LLC protocol communication.
-   **cost**: medium ($0.01-0.05 per coordination task)
-   **latency**: medium (3-15 seconds depending on subtasks)
-   **side_effects**: "Creates LLC message files, coordinates sub-agents"
-   **version**: 1.0.0
-   **tags**: [coordination, workflow, multi-agent, llc, orchestration, real, claude-code]
-   **applicability_text**: "Use for complex tasks requiring multiple specialized agents. Handles task decomposition, resource allocation, dependency resolution, and result aggregation. Optimizes agent-to-agent communication through LLC protocol for maximum efficiency."

---
-   **id**: `agent_statistical_analysis_v1`
-   **name**: StatisticalAnalysisAgent [REAL]
-   **file_path**: `components/agents/StatisticalAnalysisAgent.md`
-   **record_type**: REAL_AGENT
-   **claude_tool**: Read, Write, Bash, Task
-   **domain**: data_analysis
-   **description**: Performs advanced statistical analysis on datasets through LLC protocol communication with context-aware processing capabilities.
-   **cost**: medium ($0.02-0.08 per analysis depending on complexity)
-   **latency**: medium (5-30 seconds depending on dataset size)
-   **side_effects**: "Creates analysis result files, generates statistical reports"
-   **version**: 1.0.0
-   **tags**: [statistics, analysis, data-science, llc, clustering, correlation, real, claude-code]
-   **applicability_text**: "Use for comprehensive statistical analysis including descriptive statistics, correlation analysis, clustering, and trend analysis. Communicates through LLC protocol for efficient context passing and provides business-ready insights with confidence metrics."

---
-   **id**: `agent_simulated_finetuned_v1`
-   **name**: SimulatedFineTunedAgent [SIMULATION]
-   **file_path**: `components/agents/SimulatedFineTunedAgent.md`
-   **record_type**: SIMULATION_AGENT
-   **domain**: autonomous_operation
-   **description**: Simulates how a fine-tuned LLM would operate as an autonomous state machine, making external tool calls when needed to complete agentic workflows.
-   **cost**: none (simulation only)
-   **latency**: low (immediate decision simulation)
-   **side_effects**: "Generates tool requests and demonstrates decision patterns"
-   **version**: 1.0.0
-   **tags**: [simulation, fine-tuning, autonomous, state-machine, tool-calling]
-   **applicability_text**: "Use to demonstrate and validate how an LLM trained on LLM-OS execution traces would operate autonomously. Shows target behavior for fine-tuned models that can make external tool calls when needed, similar to Claude Code's capabilities."

## Legacy Simulation Components

---
-   **id**: `tool_web_fetcher_v1`
-   **name**: WebFetcherTool
-   **file_path**: `components/tools/WebFetcherTool.md`
-   **record_type**: TOOL
-   **domain**: data_acquisition
-   **description**: A tool to fetch the raw content of a public webpage.
-   **version**: 1.0.0
-   **tags**: [web, fetch, http, content, scrape]
-   **applicability_text**: "Use as the first step for any task that requires processing information from a live website. It provides the raw text content needed for subsequent analysis, summarization, or data extraction."

---
-   **id**: `agent_summarizer_v1`
-   **name**: SummarizationAgent
-   **file_path**: `components/agents/SummarizationAgent.md`
-   **record_type**: AGENT
-   **domain**: text_processing
-   **description**: An agent that reads text and generates a concise, structured summary.
-   **version**: 1.0.0
-   **status**: DEPRECATED
-   **tags**: [summary, nlp, text, analysis, comprehension]
-   **applicability_text**: "DEPRECATED: Use agent_summarizer_v2 for new projects. This version outputs plain text summaries."

---
-   **id**: `agent_summarizer_v2`
-   **name**: SummarizationAgent_v2
-   **file_path**: `components/agents/SummarizationAgent_v2.md`
-   **record_type**: AGENT
-   **domain**: text_processing
-   **description**: An agent that reads text and generates a structured JSON summary with title and summary fields.
-   **version**: 2.0.0
-   **tags**: [summary, nlp, text, analysis, json, structured]
-   **applicability_text**: "Use this agent when you have a body of text and need to extract key points in JSON format. Ideal for processing articles, reports, or fetched web content into structured data with separate title and summary fields for better integration with downstream systems."

---
-   **id**: `tool_file_writer_v1`
-   **name**: FileWriterTool
-   **file_path**: `components/tools/FileWriterTool.md`
-   **record_type**: TOOL
-   **domain**: file_system
-   **description**: A tool to write or save text content to a specified file.
-   **version**: 1.0.0
-   **tags**: [file, write, save, output, persist]
-   **applicability_text**: "Use as the final step in a workflow to persist a result to a file. This is for creating the final deliverable, such as a report or a data export."

---
-   **id**: `tool_translation_v1`
-   **name**: TranslationTool
-   **file_path**: `components/tools/TranslationTool.md`
-   **record_type**: TOOL
-   **domain**: text_processing
-   **description**: A tool to translate text content from one language to another.
-   **version**: 1.0.0
-   **tags**: [translation, language, nlp, text, convert]
-   **applicability_text**: "Use when you need to translate content from one language to another. Ideal for processing web content, documents, or text files that need to be made available in different languages."