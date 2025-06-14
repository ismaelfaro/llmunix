# Component: SummarizationAgent_v2

-   **Name**: SummarizationAgent_v2
-   **Type**: AGENT
-   **Description**: Analyzes a given text document and produces a structured JSON summary with separate title and summary fields.

### Inputs

-   `input_file_path` (string): The path to a text file within the `workspace/` directory that contains the content to be summarized.

### Outputs

-   `output_file_path` (string): The path within the `workspace/` directory where the generated JSON summary will be saved.

### Logic

1.  Read the full content from the `input_file_path`.
2.  Analyze the content to identify the main topic, key points, and overall message.
3.  Generate a descriptive title (5-8 words) that captures the essence of the content.
4.  Create a concise summary that is approximately 25% of the original length, capturing essential information.
5.  Format the output as valid JSON with this structure:
    ```json
    {
      "title": "Brief descriptive title (5-8 words)",
      "summary": "Concise summary paragraph with key information"
    }
    ```
6.  Write the JSON output to the `output_file_path`.

### Improvements over v1

- **Structured Output**: JSON format instead of plain text for better integration
- **Title Generation**: Automatic title creation for content categorization
- **Standardized Format**: Consistent schema for downstream processing
- **Enhanced Compatibility**: JSON output works with modern data pipelines