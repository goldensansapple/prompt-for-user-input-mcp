#!/usr/bin/env python3

import sys
import os
import time


def main():
    if len(sys.argv) != 4:
        print("Usage: user_input_console.py <title> <prompt> <response_file>")
        sys.exit(1)

    title = sys.argv[1]
    prompt = sys.argv[2]
    response_file = sys.argv[3]

    # Windows console improvements
    if os.name == 'nt':
        # Set console title
        os.system(f'title {title}')
        
        # Try to set console size (ignore errors if not supported)
        try:
            os.system('mode con cols=80 lines=25')
        except:
            pass

    # Clear screen and show banner
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("🤖 MCP User Input Console")
    print("=" * 60)
    print()

    # Display the title prominently
    if title and title != "User Input Required":
        print(f"📋 {title}")
        print("-" * 60)
        print()

    # Display the prompt with better formatting
    print("❓ Question:")
    print()
    # Wrap long prompts nicely
    words = prompt.split()
    line = ""
    for word in words:
        if len(line + word) > 55:  # Wrap at reasonable width
            print(f"   {line}")
            line = word + " "
        else:
            line += word + " "
    if line:
        print(f"   {line}")
    
    print()
    print("💬 Please enter your response below:")
    print("   (Press Enter when finished, or Ctrl+C to cancel)")
    print()

    # Get user input with enhanced error handling
    try:
        print("👤 Your response:")
        response = input("   > ").strip()
        
        if not response:
            print()
            print("⚠️  No response entered. Saving as '[Empty response]'")
            response = "[Empty response]"
        else:
            print()
            print(f"✅ Got it! Response: '{response[:50]}{'...' if len(response) > 50 else ''}'")
        
        # Write response to file with multiple attempts
        for attempt in range(3):
            try:
                with open(response_file, "w", encoding="utf-8") as f:
                    f.write(response)
                    f.flush()
                    os.fsync(f.fileno())  # Force write to disk
                print("💾 Response saved successfully!")
                break
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {e}")
                if attempt == 2:
                    raise
                time.sleep(0.1)
                    
        print()
        print("🎉 All done! You can close this window now.")
        print("   (Auto-closing in 3 seconds...)")
        time.sleep(3)
        
    except KeyboardInterrupt:
        print()
        print("🚫 Input cancelled by user (Ctrl+C pressed)")
        try:
            with open(response_file, "w", encoding="utf-8") as f:
                f.write("[Cancelled by user]")
                f.flush()
                os.fsync(f.fileno())
            print("💾 Cancellation recorded.")
        except:
            pass
        time.sleep(2)
        
    except Exception as e:
        print()
        print(f"💥 Error: {e}")
        try:
            with open(response_file, "w", encoding="utf-8") as f:
                f.write(f"[Error: {e}]")
                f.flush()
                os.fsync(f.fileno())
            print("💾 Error recorded.")
        except:
            pass
        time.sleep(2)


if __name__ == "__main__":
    main()
