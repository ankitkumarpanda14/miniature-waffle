const vscode = require('vscode');
const axios = require('axios');

let panel;

function getWebviewContent() {
  return `<!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <style>
      body { font-family: sans-serif; }
      #messages { height: 80vh; overflow-y: auto; }
      .msg { margin: 4px 0; }
    </style>
  </head>
  <body>
    <div id="messages"></div>
    <input id="input" type="text" placeholder="Ask a question" />
    <script>
      const vscode = acquireVsCodeApi();
      const input = document.getElementById('input');
      function addMessage(role, text) {
        const container = document.getElementById('messages');
        const div = document.createElement('div');
        div.className = 'msg';
        div.textContent = (role === 'user' ? 'You: ' : 'Assistant: ') + text;
        container.appendChild(div);
        container.scrollTop = container.scrollHeight;
      }
      input.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
          const text = input.value;
          input.value = '';
          vscode.postMessage({ command: 'ask', text });
          addMessage('user', text);
        }
      });
      window.addEventListener('message', event => {
        addMessage('assistant', event.data.text);
      });
    </script>
  </body>
  </html>`;
}

async function queryAssistant(question) {
  const editor = vscode.window.activeTextEditor;
  const text = editor ? editor.document.getText(editor.selection.isEmpty ? undefined : editor.selection) : '';
  try {
    const response = await axios.post('http://localhost:8000/query', {
      code: text,
      question,
    });
    return response.data.answer || response.data;
  } catch (err) {
    return 'Request failed: ' + err.message;
  }
}

function createOrShowPanel() {
  if (panel) {
    panel.reveal(vscode.ViewColumn.Beside);
    return panel;
  }
  panel = vscode.window.createWebviewPanel('ollamaAssistant', 'Ollama Assistant', vscode.ViewColumn.Beside, { enableScripts: true });
  panel.webview.html = getWebviewContent();
  panel.onDidDispose(() => { panel = undefined; });
  panel.webview.onDidReceiveMessage(async message => {
    if (message.command === 'ask') {
      const answer = await queryAssistant(message.text);
      panel.webview.postMessage({ text: answer });
    }
  });
  return panel;
}

function activate(context) {
  const disposable = vscode.commands.registerCommand('ollamaCodeAssistant.ask', () => {
    createOrShowPanel();
  });
  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };
