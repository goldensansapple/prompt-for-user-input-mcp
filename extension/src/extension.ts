import * as vscode from "vscode";
import express, { Request, Response } from "express";
import { Server } from "http";

let server: Server | undefined;
let pendingPrompts = new Map<
  string,
  {
    resolve: (value: string) => void;
    reject: (reason?: any) => void;
  }
>();

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
  app.post("/prompt", async (req: Request, res: Response) => {
    try {
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
  });

  // Health check endpoint
  app.get("/health", (req: Request, res: Response) => {
    res.json({ status: "ok", timestamp: new Date().toISOString() });
  });

  const port = 3001; // Different from MCP server port
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

function getWebviewContent(title: string, prompt: string): string {
  const templates = new VSCodeWebviewTemplates();

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>${templates.getStyles()}</style>
</head>
<body>
  ${templates.getBodyContent(title, prompt)}
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
      body {
        font-family: var(--vscode-font-family);
        font-size: var(--vscode-font-size);
        color: var(--vscode-foreground);
        background-color: var(--vscode-editor-background);
        padding: 20px;
        margin: 0;
      }
      .container {
        max-width: 800px;
        margin: 0 auto;
      }
      .title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 20px;
        color: var(--vscode-titleBar-activeForeground);
      }
      .prompt-section {
        background-color: var(--vscode-editor-inactiveSelectionBackground);
        border: 1px solid var(--vscode-widget-border);
        border-radius: 4px;
        padding: 15px;
        margin-bottom: 20px;
        font-family: var(--vscode-editor-font-family);
        white-space: pre-wrap;
        word-wrap: break-word;
        user-select: text;
        cursor: text;
      }
      .prompt-label {
        font-weight: bold;
        color: var(--vscode-textLink-foreground);
        margin-bottom: 10px;
        display: block;
      }
      .input-section {
        margin-top: 20px;
      }
      .input-label {
        font-weight: bold;
        margin-bottom: 8px;
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
        outline: none;
      }
      #responseInput:focus {
        border-color: var(--vscode-focusBorder);
      }
      .button-container {
        margin-top: 15px;
        text-align: right;
      }
      button {
        padding: 8px 16px;
        margin-left: 10px;
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
      .tip {
        font-size: 12px;
        color: var(--vscode-descriptionForeground);
        margin-top: 10px;
        font-style: italic;
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
          responseInput.addEventListener('keydown', handleKeyDown);
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
    `;
  }

  getBodyContent(title: string, prompt: string): string {
    return `
      <div class="container">
        <div class="title">${title}</div>
        
        <div class="prompt-section">
          <span class="prompt-label">Question (you can select and copy this text):</span>
          ${prompt}
        </div>
        
        <div class="input-section">
          <label class="input-label" for="responseInput">Your Response:</label>
          <textarea id="responseInput" placeholder="Enter your response here..."></textarea>
          <div class="tip">💡 Tip: You can select and copy any text from the question above.</div>
        </div>
        
        <div class="button-container">
          <button class="cancel-btn">Cancel</button>
          <button class="submit-btn">Submit</button>
        </div>
      </div>
    `;
  }
}
