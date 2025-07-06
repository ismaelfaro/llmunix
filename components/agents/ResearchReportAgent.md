# ResearchReportAgent
This agent transforms a raw research summary into a structured and polished formal report.

## Input
The input to this agent is a JSON object with the following structure:
```json
{
  "research_summary": "The detailed summary of the research findings...",
  "title": "The title of the report"
}
```

## Output
The output of this agent is a Markdown-formatted research report.

## Logic
1.  **Parse Input**: Read the `research_summary` and `title` from the input JSON.
2.  **Structure the Report**: Organize the summary into a standard report format with the following sections:
    *   Title
    *   Executive Summary
    *   Key Advancements (using bullet points for clarity)
    *   Conclusion/Outlook
3.  **Format and Refine**: Ensure the language is professional and the formatting is clean and readable using Markdown.
4.  **Generate Report**: Output the final, polished Markdown report.
