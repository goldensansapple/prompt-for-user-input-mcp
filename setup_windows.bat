@echo off
echo Setting up Prompt For User Input MCP on Windows...
echo.

echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Setting up VSCode extension...
cd extension

echo Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo Failed to install Node.js dependencies
    echo Make sure Node.js is installed: https://nodejs.org/
    pause
    exit /b 1
)

echo Compiling TypeScript...
npm run compile
if %errorlevel% neq 0 (
    echo Failed to compile TypeScript
    pause
    exit /b 1
)

cd ..

echo.
echo ===== Setup Complete! =====
echo.
echo Next steps:
echo 1. Install the extension in VSCode:
echo    - Open VSCode/Cursor
echo    - Press F5 to run extension in development mode
echo    OR
echo    - Press Ctrl+Shift+P and run "Extensions: Install from VSIX..."
echo.
echo 2. Start the enhanced MCP server:
echo    python mcp_server_vscode.py
echo.
echo 3. Configure Cursor/VSCode MCP settings to use:
echo    http://localhost:8000/sse
echo.
pause 