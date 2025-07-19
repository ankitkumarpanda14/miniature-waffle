const vscode = require('vscode');
const axios = require('axios');

async function askAssistant() {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showErrorMessage('No active editor.');
    return;
  }
  const selection = editor.selection;
  const text = editor.document.getText(selection.isEmpty ? undefined : selection);
  const question = await vscode.window.showInputBox({
    prompt: 'Enter your question for the assistant (leave empty to explain the code)'
  });
  if (question === undefined) {
    // User canceled the input box
    return;
  }
  try {
    const response = await axios.post('http://localhost:8000/query', {
      code: text,
      question: question || null,
    });
    const output = response.data.answer || response.data;
    const channel = vscode.window.createOutputChannel('Ollama Assistant');
    channel.appendLine(output);
    channel.show();
  } catch (err) {
    vscode.window.showErrorMessage('Request failed: ' + err.message);
  }
}

function activate(context) {
  let disposable = vscode.commands.registerCommand('ollamaCodeAssistant.ask', askAssistant);
  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};
