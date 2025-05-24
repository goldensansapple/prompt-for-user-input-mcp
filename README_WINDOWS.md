# Windows Setup - Quick Start

## 🚀 Immediate Working Solution

The **console-based approach** is ready to use right now on Windows with enhanced UI!

### 1. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 2. Start the MCP Server
```cmd
python mcp_server.py
```

### 3. Configure Cursor
Add to your MCP configuration:
```json
{
  "mcpServers": {
    "prompt-for-user-input-mcp": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### 4. Use This System Prompt
```text
IMPORTANT - Do not finish responding until explicitly told to do so, instead always use MCP `prompt_for_user_input` and wait for response in all cases. If you feel stuck, have a question or you are finished with the work, always communicate with the user using this MCP.
```

## ✨ Enhanced Windows Console Features

The console now has:
- 🎨 **Beautiful formatting** with emojis and colors
- 📏 **Text wrapping** for long prompts  
- 🖼️ **Custom console title** shows the prompt title
- 📏 **Optimized window size** (80x25)
- ⏱️ **Auto-close** after 3 seconds
- 🔄 **Better error handling** with visual feedback
- 🚫 **Graceful cancellation** (Ctrl+C)

## 🎯 Future: VSCode Extension (Advanced)

For native in-editor dialogs, the VSCode extension is available but needs:
1. Node.js installed
2. Run `setup_windows.bat` 
3. Extension compilation and installation

The console approach works immediately and provides an excellent user experience!

## 🔧 Quick Test

1. Start the server: `python mcp_server.py`
2. Test manually: Open a new PowerShell and run:
   ```cmd
   python user_input_console.py "Test Title" "What is your favorite color?" "test_response.txt"
   ```
3. You should see a beautiful formatted console window!

## 📋 What You Get

```
🤖 MCP User Input Console
============================================================

📋 Test Title
------------------------------------------------------------

❓ Question:

   What is your favorite color?

💬 Please enter your response below:
   (Press Enter when finished, or Ctrl+C to cancel)

👤 Your response:
   > 
```

Ready to use right now! 🎉 