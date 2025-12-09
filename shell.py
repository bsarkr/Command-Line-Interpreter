#!/usr/bin/env python3
"""
===============================================================================
CUSTOM SHELL PROJECT - BILASH'S CORE IMPLEMENTATION (PYTHON VERSION)
===============================================================================

Team: Bilash Sarkar, Max Hazelton, Jake Gesseck
Course: Operating Systems  
Project: Command-Line Interpreter (CLI/Shell)

===============================================================================
PURE PYTHON FILES INCLUDED:
===============================================================================

1. shell.py       - Main shell program (THIS FILE)  
2. signals_mod.py - Signal handling module
3. utils.py       - Utility functions and stub implementations
4. test_shell.py  - Test program to verify functionality

===============================================================================
HOW TO RUN AND TEST:
===============================================================================

STEP 1: Test your implementation
    python3 test_shell.py

STEP 2: Run the shell
    python3 shell.py

STEP 3: Test basic commands
    pwd
    help  
    cd ~
    jobs
    exit

===============================================================================
WHAT'S IMPLEMENTED (BILASH'S RESPONSIBILITIES):
===============================================================================

✓ Core shell loop with prompt display and input handling
✓ Signal handling for SIGINT (Ctrl+C), SIGTSTP (Ctrl+Z), SIGCHLD
✓ Background process management framework  
✓ Shell state management and cleanup
✓ Basic built-in commands: pwd, cd, help, jobs, exit
✓ Integration points for Max's parser/executor modules
✓ Integration points for Jake's built-in/features modules

===============================================================================
FOR TEAMMATES - INTEGRATION POINTS:
===============================================================================

MAX (Parser & Executor) - Replace these stub functions in utils.py:
• parse_command(input_str) -> List[str]
• execute_command(args, background=False) -> int

JAKE (Built-ins & Features) - Enhance these functions in utils.py:  
• is_builtin_command(command) -> bool
• execute_builtin(args) -> int
• Add I/O redirection and piping functionality

===============================================================================
"""

import os
import sys
import signal
from typing import List, Dict, Any
from utils import *
from signals_mod import setup_signal_handlers

class ShellState:
    """Global shell state management"""
    def __init__(self):
        self.running = True
        self.current_directory = os.getcwd()
        self.previous_directory = None
        self.aliases = {}
        self.prompt = ""
        self.last_exit_status = 0
        self.background_processes = []
        self.command_history = []

# Global shell state instance
shell_state = ShellState()

def main():
    """Main entry point for the shell"""
    print("=== Custom Shell v1.0 (Python) ===")
    print("Team: Bilash, Max, Jake")
    print("Type 'help' for commands or 'exit' to quit.")
    print()
    
    # Initialize shell state
    shell_state.current_directory = get_current_directory()
    
    # Setup signal handlers
    setup_signal_handlers()
    
    # Set initial prompt
    set_prompt()
    
    # Enter main shell loop
    shell_loop()
    
    # Cleanup and exit
    cleanup_shell()
    
    return shell_state.last_exit_status

def shell_loop():
    """Main interactive shell loop"""
    while shell_state.running:
        try:
            # Handle background processes
            handle_background_processes()
            
            # Display prompt and read input
            display_prompt()
            user_input = read_input()
            
            # Skip empty input
            if not user_input.strip():
                continue
            
            # Add to history
            shell_state.command_history.append(user_input)
            
            # Parse command
            args = parse_command(user_input)
            if not args:
                continue
            
            # Check for background execution
            background = False
            if args and args[-1] == "&":
                background = True
                args.pop()
            
            if not args:
                continue
            
            # Handle exit command specially
            if args[0] == "exit":
                if len(args) > 1:
                    try:
                        shell_state.last_exit_status = int(args[1])
                    except ValueError:
                        print_error(f"Invalid exit code: {args[1]}")
                        shell_state.last_exit_status = 1
                shell_state.running = False
                break
            
            # Execute command (built-in or external)
            if is_builtin_command(args[0]):
                status = execute_builtin(args, shell_state)
                shell_state.last_exit_status = status
            else:
                status = execute_command(args, background)
                if not background:
                    shell_state.last_exit_status = status
            
            # Update current directory and prompt
            shell_state.current_directory = get_current_directory()
            set_prompt()
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print()
            continue
        except EOFError:
            # Handle Ctrl+D
            print()
            shell_state.running = False
            break
        except Exception as e:
            print_error(f"Shell error: {e}")

def display_prompt():
    """Display the shell prompt"""
    print(shell_state.prompt, end=" ", flush=True)

def read_input() -> str:
    """Read user input from stdin"""
    try:
        return input()
    except (KeyboardInterrupt, EOFError):
        raise

def cleanup_shell():
    """Clean up shell resources before exit"""
    print("Cleaning up shell resources...")
    
    # Terminate background processes
    if shell_state.background_processes:
        print("Terminating background processes...")
        for pid in shell_state.background_processes[:]:
            try:
                os.kill(pid, signal.SIGTERM)
                # Give processes time to terminate gracefully
                import time
                time.sleep(0.1)
                try:
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass  # Process already terminated
            except (ProcessLookupError, PermissionError):
                pass  # Process already gone or not ours
    
    print(f"Shell exited with status: {shell_state.last_exit_status}")

if __name__ == "__main__":
    sys.exit(main())
