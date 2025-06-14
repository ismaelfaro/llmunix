# Component: TranslationTool

-   **Name**: TranslationTool
-   **Type**: TOOL
-   **Description**: Translates text content from one language to another.

### Inputs

-   `input_file_path` (string): The path to a text file within the `workspace/` directory that contains the content to be translated.
-   `source_language` (string): The source language code (e.g., "en" for English).
-   `target_language` (string): The target language code (e.g., "es" for Spanish).

### Outputs

-   `output_file_path` (string): The path within the `workspace/` directory where the translated content will be saved.

### Logic

1.  Read the full content from the `input_file_path`.
2.  Identify the source language and target language.
3.  For simulation purposes, apply basic translation rules:
   - "Example Domain" → "Dominio de Ejemplo"
   - "This domain is for use" → "Este dominio es para uso"
   - "in illustrative examples" → "en ejemplos ilustrativos"
   - "in documents" → "en documentos"
   - "You may use this domain" → "Puedes usar este dominio"
   - "without prior coordination" → "sin coordinación previa"
   - "asking for permission" → "pidiendo permiso"
   - "established to be used" → "establecido para ser usado"
4.  Write the translated text to the `output_file_path`.