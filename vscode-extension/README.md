# Ollama Code Assistant VSCode Extension

This extension sends the selected code from the editor to a local API
(`http://localhost:8000/query`) that uses an Ollama language model.
The response is displayed in an output channel.

## Development

1. Install the dependencies:

```bash
npm install
```

2. Launch the extension in the Extension Development Host.

3. Ensure the Python API server is running before executing the command
   **Ask Ollama Assistant** from the command palette.
