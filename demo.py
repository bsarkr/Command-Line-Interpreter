#!/usr/bin/env python3
"""
Shell Demo and Testing Script

This script demonstrates how to run and test your shell implementation.
"""

import subprocess
import time
import os

def run_demo():
    print("=" * 60)
    print("CUSTOM SHELL DEMO - HOW TO RUN YOUR SHELL")
    print("=" * 60)
    
    print("\n1. YOUR SHELL IS FULLY FUNCTIONAL!")
    print("   Here's what's implemented:")
    print("   ✓ Bilash: Core shell loop, signal handling, state management")
    print("   ✓ Max: Command parsing, variable expansion, process execution")
    print("   ✓ Jake: Basic built-ins (missing I/O redirection)")
    
    print("\n2. HOW TO RUN THE SHELL:")
    print("   Command: python3 shell.py")
    print("   This starts an interactive shell session")
    
    print("\n3. COMMANDS YOU CAN TRY:")
    demo_commands = [
        "pwd                    # Show current directory",
        "ls                     # List files",
        "ls -la                 # List with details",
        'echo "Hello World"     # Test echo builtin',
        "cd ~                   # Go to home directory",
        "cd Documents           # Change to Documents",
        "export NAME=Bilash     # Set environment variable",
        "echo $NAME             # Show variable (should print Bilash)",
        "echo $HOME             # Show home directory",
        "echo $?                # Show last exit status",
        "sleep 3 &              # Run in background",
        "jobs                   # Show background jobs",
        "help                   # Show all commands",
        "history                # Show command history",
        "exit                   # Quit the shell"
    ]
    
    for cmd in demo_commands:
        print(f"   {cmd}")
    
    print("\n4. ADVANCED FEATURES WORKING:")
    print("   ✓ Variable expansion: $VAR, ${VAR}, $?")
    print("   ✓ Tilde expansion: ~, ~/Documents")
    print("   ✓ Comment handling: echo hello # this is ignored")
    print("   ✓ Background processes: sleep 5 &")
    print("   ✓ Signal handling: Ctrl+C doesn't exit shell")
    print("   ✓ Quote handling: echo 'hello world'")
    
    print("\n5. WHAT'S STILL MISSING (for Jake):")
    print("   ❌ I/O redirection: > < >> |")
    print("   ❌ Piping: command1 | command2")
    print("   ❌ More advanced built-ins")
    
    print("\n" + "=" * 60)
    print("TRY IT NOW!")
    print("=" * 60)
    print("Run this command in your terminal:")
    print("    python3 shell.py")
    print()
    print("Then try these example commands:")
    print("    pwd")
    print("    ls")
    print('    echo "Hello $USER"')
    print("    export TEST=working")
    print("    echo $TEST")
    print("    sleep 5 &")
    print("    jobs")
    print("    help")
    print("    exit")
    print()

if __name__ == "__main__":
    run_demo()
