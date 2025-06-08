import * as vscode from "vscode";
import express from "express";
import { Server } from "http";

let server: Server | undefined;

export function activate(context: vscode.ExtensionContext) {
  console.log("Prompt For User Input MCP extension is now active!");

  // Start the local HTTP server to receive prompt requests
  startLocalServer();

  // Register the command for manual testing
  const disposable = vscode.commands.registerCommand(
    "promptForUserInputMcp.showInputDialog",
    () => {
      vscode.window.showInformationMessage(
        "Prompt For User Input MCP is active!"
      );
    }
  );

  context.subscriptions.push(disposable);
}

export function deactivate() {
  if (server) {
    server.close();
  }
}

function startLocalServer() {
  const app = express();
  app.use(express.json());

  // Endpoint for receiving prompt requests from MCP server
  app.post("/prompt", (req: express.Request, res: express.Response) => {
    (async () => {
      try {
        res.setTimeout(60 * 60 * 1000); // 1 hour timeout
        const { id, title = "User Input Required", prompt } = req.body;

        if (!id || !prompt) {
          return res
            .status(400)
            .json({ error: "Missing required fields: id, prompt" });
        }

        // Show the input dialog in VSCode
        const response = await showInputDialog(title, prompt);

        res.json({ response });
      } catch (error) {
        console.error("Error handling prompt request:", error);
        res.status(500).json({ error: "Internal server error" });
      }
    })();
  });

  // Health check endpoint
  app.get("/health", (_req: express.Request, res: express.Response) => {
    res.json({ status: "ok", timestamp: new Date().toISOString() });
  });

  // Get port from settings or use default
  const config = vscode.workspace.getConfiguration("promptForUserInputMcp");
  const port = config.get<number>("serverPort", 3001);

  server = app.listen(port, "localhost", () => {
    console.log(
      `VSCode extension server listening on http://localhost:${port}`
    );
  });
}

async function showInputDialog(title: string, prompt: string): Promise<string> {
  return new Promise((resolve) => {
    // Create a webview panel for better text display and selection
    const panel = vscode.window.createWebviewPanel(
      "userInput",
      title,
      vscode.ViewColumn.One,
      {
        enableScripts: true,
        localResourceRoots: [],
      }
    );

    // Set the HTML content with selectable text and input field
    panel.webview.html = getWebviewContent(title, prompt);

    // Handle messages from the webview
    panel.webview.onDidReceiveMessage((message) => {
      console.log("Received message:", message);

      switch (message.command) {
        case "submit":
          console.log("Submit received with text:", message.text);
          const responseText = message.text || "[Empty response]";
          resolve(responseText);
          panel.dispose();
          return;
        case "cancel":
          console.log("Cancel received");
          resolve("[Cancelled by user]");
          panel.dispose();
          return;
        default:
          console.log("Unknown command:", message.command);
      }
    });
  });
}

// HTML escaping function to prevent XSS attacks
function escapeHtml(unsafe: string): string {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function getWebviewContent(title: string, prompt: string): string {
  const templates = new VSCodeWebviewTemplates();
  const escapedTitle = escapeHtml(title);

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapedTitle}</title>
  <style>${templates.getStyles()}</style>
</head>
<body>
  ${templates.getBodyContent(escapedTitle, escapeHtml(prompt))}
  <script>${templates.getScript()}</script>
</body>
</html>`;
}

// Webview content builders
interface WebviewTemplates {
  getStyles(): string;
  getScript(): string;
  getBodyContent(title: string, prompt: string): string;
}

class VSCodeWebviewTemplates implements WebviewTemplates {
  getStyles(): string {
    return `
      /* Tailwind CSS Preflight Reset - 2025 v4.1 */
      *, ::before, ::after, ::backdrop, ::file-selector-button {
        box-sizing: border-box;
        border: 0 solid;
        margin: 0;
        padding: 0;
      }

      html {
        line-height: 1.5;
        -webkit-text-size-adjust: 100%;
        -moz-tab-size: 4;
        tab-size: 4;
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
      }

      body {
        line-height: inherit;
      }

      hr {
        height: 0;
        color: inherit;
        border-top-width: 1px;
      }

      abbr:where([title]) {
        text-decoration: underline dotted;
      }

      h1, h2, h3, h4, h5, h6 {
        font-size: inherit;
        font-weight: inherit;
      }

      a {
        color: inherit;
        text-decoration: inherit;
      }

      b, strong {
        font-weight: bolder;
      }

      code, kbd, samp, pre {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        font-size: 1em;
      }

      small {
        font-size: 80%;
      }

      sub, sup {
        font-size: 75%;
        line-height: 0;
        position: relative;
        vertical-align: baseline;
      }

      sub {
        bottom: -0.25em;
      }

      sup {
        top: -0.5em;
      }

      table {
        text-indent: 0;
        border-color: inherit;
        border-collapse: collapse;
      }

      button, input, optgroup, select, textarea {
        font-family: inherit;
        font-size: 100%;
        font-weight: inherit;
        line-height: inherit;
        color: inherit;
        margin: 0;
        padding: 0;
      }

      button, select {
        text-transform: none;
      }

      button, [type="button"], [type="reset"], [type="submit"] {
        -webkit-appearance: button;
        background-color: transparent;
        background-image: none;
      }

      :-moz-focusring {
        outline: auto;
      }

      :-moz-ui-invalid {
        box-shadow: none;
      }

      progress {
        vertical-align: baseline;
      }

      ::-webkit-inner-spin-button, ::-webkit-outer-spin-button {
        height: auto;
      }

      [type="search"] {
        -webkit-appearance: textfield;
        outline-offset: -2px;
      }

      ::-webkit-search-decoration {
        -webkit-appearance: none;
      }

      ::-webkit-file-upload-button {
        -webkit-appearance: button;
        font: inherit;
      }

      summary {
        display: list-item;
      }

      blockquote, dl, dd, h1, h2, h3, h4, h5, h6, hr, figure, p, pre {
        margin: 0;
      }

      fieldset {
        margin: 0;
        padding: 0;
      }

      legend {
        padding: 0;
      }

      ol, ul, menu {
        list-style: none;
        margin: 0;
        padding: 0;
      }

      textarea {
        resize: vertical;
      }

      input::placeholder, textarea::placeholder {
        opacity: 1;
      }

      button, [role="button"] {
        cursor: pointer;
      }

      :disabled {
        cursor: default;
      }

      img, svg, video, canvas, audio, iframe, embed, object {
        display: block;
        vertical-align: middle;
      }

      img, video {
        max-width: 100%;
        height: auto;
      }

      [hidden] {
        display: none;
      }

      /* VSCode theme integration with utility-friendly base */
      body {
        font-family: var(--vscode-font-family);
        font-size: var(--vscode-font-size);
        color: var(--vscode-foreground);
        background-color: var(--vscode-editor-background);
        padding: 20px;
        display: flex;
        justify-content: center;
        min-height: 100vh;
      }

      .container {
        max-width: 800px;
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 20px;
      }

      .title {
        font-size: 18px;
        font-weight: bold;
        color: var(--vscode-titleBar-activeForeground);
      }

      .prompt-section {
        background-color: var(--vscode-editor-inactiveSelectionBackground);
        border: 1px solid var(--vscode-widget-border);
        border-radius: 4px;
        padding: 15px;
        font-family: var(--vscode-editor-font-family);
        white-space: pre-wrap;
        word-wrap: break-word;
        user-select: text;
        cursor: text;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .prompt-label {
        font-weight: bold;
        color: var(--vscode-textLink-foreground);
        display: block;
      }

      .input-section {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      .input-label {
        font-weight: bold;
        display: block;
      }

      #responseInput {
        width: 100%;
        min-height: 100px;
        padding: 10px;
        border: 1px solid var(--vscode-widget-border);
        border-radius: 4px;
        background-color: var(--vscode-input-background);
        color: var(--vscode-input-foreground);
        font-family: var(--vscode-editor-font-family);
        font-size: var(--vscode-editor-font-size);
        resize: vertical;
        box-sizing: border-box;
      }

      .button-container {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
      }

      button {
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 13px;
      }

      .submit-btn {
        background-color: var(--vscode-button-background);
        color: var(--vscode-button-foreground);
      }

      .submit-btn:hover {
        background-color: var(--vscode-button-hoverBackground);
      }

      .cancel-btn {
        background-color: var(--vscode-button-secondaryBackground);
        color: var(--vscode-button-secondaryForeground);
      }

      .cancel-btn:hover {
        background-color: var(--vscode-button-secondaryHoverBackground);
      }
    `;
  }

  getScript(): string {
    return `
      const vscode = acquireVsCodeApi();
      
      function submit() {
        const input = document.getElementById('responseInput');
        const text = input.value.trim();
        console.log('Submit function called with text:', text);
        
        try {
          vscode.postMessage({
            command: 'submit',
            text: text
          });
          console.log('Message sent successfully');
        } catch (error) {
          console.error('Error sending message:', error);
        }
      }
      
      function cancel() {
        console.log('Cancel function called');
        try {
          vscode.postMessage({
            command: 'cancel'
          });
          console.log('Cancel message sent successfully');
        } catch (error) {
          console.error('Error sending cancel message:', error);
        }
      }
      
      function saveState() {
        const input = document.getElementById('responseInput');
        if (input) {
          vscode.setState({ inputText: input.value });
          console.log('State saved:', input.value);
        }
      }
      
      function restoreState() {
        const previousState = vscode.getState();
        const input = document.getElementById('responseInput');
        
        if (previousState && previousState.inputText && input) {
          input.value = previousState.inputText;
          console.log('State restored:', previousState.inputText);
        }
      }
      
      function handleKeyDown(e) {
        console.log('Key pressed:', e.key, 'Ctrl:', e.ctrlKey, 'Shift:', e.shiftKey);
        
        if (e.ctrlKey && e.key === 'Enter') {
          console.log('Ctrl+Enter detected - submitting');
          e.preventDefault();
          submit();
          return;
        }
        
        if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
          console.log('Enter detected - submitting');
          e.preventDefault();
          submit();
          return;
        }
        
        if (e.key === 'Enter' && e.shiftKey) {
          console.log('Shift+Enter detected - allowing new line');
          return;
        }
      }
      
      document.addEventListener('DOMContentLoaded', function() {
        console.log('DOM Content Loaded');
        
        const responseInput = document.getElementById('responseInput');
        const submitBtn = document.querySelector('.submit-btn');
        const cancelBtn = document.querySelector('.cancel-btn');
        
        if (responseInput) {
          // Restore previous state first
          restoreState();
          
          responseInput.addEventListener('keydown', handleKeyDown);
          
          // Save state on every input change
          responseInput.addEventListener('input', saveState);
          
          // Save state when losing focus
          responseInput.addEventListener('blur', saveState);
          
          responseInput.focus();
          console.log('Event listeners added to textarea');
        } else {
          console.error('responseInput element not found!');
        }
        
        if (submitBtn) {
          submitBtn.addEventListener('click', function() {
            console.log('Submit button clicked');
            submit();
          });
          console.log('Submit button event listener added');
        } else {
          console.error('Submit button not found!');
        }
        
        if (cancelBtn) {
          cancelBtn.addEventListener('click', function() {
            console.log('Cancel button clicked');
            cancel();
          });
          console.log('Cancel button event listener added');
        } else {
          console.error('Cancel button not found!');
        }
      });
      
      window.addEventListener('load', function() {
        console.log('Window loaded');
        const responseInput = document.getElementById('responseInput');
        if (responseInput) {
          responseInput.focus();
          console.log('Input focused on window load');
        }
      });
      
      // Save state before the webview might be destroyed
      window.addEventListener('beforeunload', saveState);
    `;
  }

  getBodyContent(title: string, prompt: string): string {
    return `
      <div class="container">
        <div class="title">${title}</div>
        
        <div class="prompt-section">
          <span class="prompt-label">Question:</span>
          ${prompt}
        </div>
        
        <div class="input-section">
          <label class="input-label" for="responseInput">Your Response:</label>
          <textarea id="responseInput" placeholder="Enter your response here..."></textarea>
        </div>
        
        <div class="button-container">
          <button class="cancel-btn">Cancel</button>
          <button class="submit-btn">Submit</button>
        </div>
      </div>
    `;
  }
}
