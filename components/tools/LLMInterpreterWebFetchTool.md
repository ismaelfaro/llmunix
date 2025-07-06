# Component: LLMInterpreterWebFetchTool

- **Name**: LLMInterpreterWebFetchTool
- **Type**: TOOL
- **Runtime**: LLM Interpreter
- **Description**: Fetches real web content using standard command-line tools (curl/wget) for LLM Interpreter runtime.

## Inputs

- `url` (string): The URL to fetch content from
- `prompt` (string): Instructions for content extraction (default: "Extract the main text content")

## Outputs

- `content` (string): The extracted content from the webpage
- `summary` (string): Brief summary of what was fetched
- `metadata` (object): Information about the fetch operation

## Command Mapping

```yaml
base_command: curl
parameters:
  url: {{url}}
  options: ["-L", "--user-agent", "Mozilla/5.0", "-s"]
cost: none (uses local networking)
latency: medium (2-10 seconds)
side_effects: "Network request to external server"
error_modes: ["timeout", "404", "403", "connection_error", "ssl_error"]
```

## Logic

### Web Content Fetching:
1. **Primary Method**: Use curl with follow redirects and user agent
   ```bash
   curl -L --user-agent "Mozilla/5.0 (compatible; LLMunix)" -s "$URL"
   ```

2. **Fallback Method**: Use wget if curl unavailable
   ```bash
   wget -q -O - --user-agent="Mozilla/5.0 (compatible; LLMunix)" "$URL"
   ```

3. **Text Extraction**: Basic HTML-to-text conversion using sed/awk:
   - Remove HTML tags: `sed 's/<[^>]*>//g'`
   - Clean whitespace: `sed 's/&nbsp;/ /g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g'`
   - Extract paragraphs and headers only

4. **Content Processing**: Apply prompt instructions to filter content:
   - If prompt contains "title": Extract content between `<title>` tags
   - If prompt contains "article": Focus on `<article>`, `<main>`, or large text blocks
   - If prompt contains "summary": Return first few paragraphs

## Implementation Template

```bash
#!/bin/bash
# LLM Interpreter WebFetch Implementation

URL="$1"
PROMPT="$2"

# Check if curl is available, fallback to wget
if command -v curl >/dev/null 2>&1; then
    FETCHER="curl -L --user-agent 'Mozilla/5.0 (compatible; LLMunix)' -s"
elif command -v wget >/dev/null 2>&1; then
    FETCHER="wget -q -O - --user-agent='Mozilla/5.0 (compatible; LLMunix)'"
else
    echo "Error: Neither curl nor wget available for web fetching"
    exit 1
fi

# Fetch content
echo "Fetching content from: $URL"
RAW_CONTENT=$($FETCHER "$URL" 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "Error: Failed to fetch content from $URL"
    exit 1
fi

# Basic HTML-to-text conversion
CLEAN_CONTENT=$(echo "$RAW_CONTENT" | \
    sed 's/<script[^>]*>.*<\/script>//g' | \
    sed 's/<style[^>]*>.*<\/style>//g' | \
    sed 's/<[^>]*>//g' | \
    sed 's/&nbsp;/ /g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g' | \
    sed '/^[[:space:]]*$/d' | \
    head -100)

# Apply prompt-based filtering
if echo "$PROMPT" | grep -qi "title"; then
    TITLE=$(echo "$RAW_CONTENT" | sed -n 's/.*<title>\(.*\)<\/title>.*/\1/p' | head -1)
    echo "Title: $TITLE"
fi

echo "Content extracted successfully"
echo "Word count: $(echo "$CLEAN_CONTENT" | wc -w)"
echo ""
echo "=== CONTENT ==="
echo "$CLEAN_CONTENT"
```

## Usage Examples

**Simple webpage fetch:**
```bash
# LLM Interpreter will execute:
bash webfetch.sh "https://example.com" "Get the main content"
```

**Article extraction:**
```bash
# LLM Interpreter will execute:
bash webfetch.sh "https://blog.com/article" "Extract article title and body"
```

## Error Handling

- **Command Not Found**: Check for curl, then wget, provide clear error if neither available
- **Network Error**: Return network connectivity guidance
- **Timeout**: Use curl/wget timeout options (30s default)
- **SSL Issues**: Add --insecure flag as fallback option
- **Rate Limiting**: Detect rate limit responses and suggest retry delays

## Integration with SystemAgent

The SystemAgent should detect runtime environment and use appropriate tool:

```markdown
**Web Fetch Tool Selection Logic:**
- If running in Claude Code runtime → Use RealWebFetchTool (WebFetch tool)
- If running in LLM Interpreter runtime → Use LLMInterpreterWebFetchTool (curl/wget commands)
- If neither available → Use simulation mode with mock content
```

## Training Data Format

```json
{
  "tool_call": {
    "tool": "curl",
    "command": "curl -L --user-agent 'Mozilla/5.0' -s 'https://example.com'",
    "inputs": {"url": "https://example.com", "prompt": "Extract content"},
    "outputs": {"content": "...", "metadata": {"status": "200", "words": 542}},
    "performance": {"time": "2.1s", "success": true, "method": "curl"}
  }
}
```

## Security Considerations

- Use proper user agent to avoid being blocked
- Implement reasonable timeouts to prevent hanging
- Sanitize URLs to prevent command injection
- No automatic following of suspicious redirects
- Basic rate limiting respect (delays between requests)