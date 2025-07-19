# Ollama Code Assistant VSCode Extension

This extension sends the selected code from the editor to a local API
(`http://localhost:8000/query`) that uses an Ollama language model.
When you run the command a chat panel opens where you can enter questions and
see the assistant's responses.

## Development

1. Install the dependencies:

```bash
npm install
```

2. Launch the extension in the Extension Development Host.

3. Ensure the Python API server is running. Execute the
   **Ask Ollama Assistant** command from the command palette to open the chat
   panel and start interacting with the assistant.
