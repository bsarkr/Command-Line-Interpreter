#!/usr/bin/env python3
"""
Utility Functions Module for Custom Shell

This module contains utility functions and stub implementations for teammate integration:
- Shell utility functions (prompt, directory management, error handling)
- Stub implementations for Max's parser/executor functions
- Stub implementations for Jake's built-in/features functions
"""

import os
import sys
import pwd
import socket
import subprocess
import shlex
from typing import List, Optional

def print_error(message: str):
    """Print error message to stderr"""
    print(f"shell: error: {message}", file=sys.stderr)

def print_info(message: str):
    """Print info message to stdout"""
    print(f"shell: {message}")

def get_current_directory() -> str:
    """Get current working directory"""
    try:
        return os.getcwd()
    except OSError as e:
        print_error(f"getcwd: {e}")
        return "/"

def set_prompt():
    """Set the shell prompt in format: user@hostname:path$"""
    from shell import shell_state
    
    cwd = shell_state.current_directory
    
    # Get home directory for path shortening
    home = os.path.expanduser("~")
    if cwd == home:
        cwd = "~"
    elif cwd.startswith(home + "/"):
        cwd = "~" + cwd[len(home):]
    
    # Get username
    try:
        username = pwd.getpwuid(os.getuid()).pw_name
    except (KeyError, OSError):
        username = os.getenv("USER", "user")
    
    # Get hostname
    try:
        hostname = socket.gethostname()
    except OSError:
        hostname = "localhost"
    
    # Create prompt
    shell_state.prompt = f"{username}@{hostname}:{cwd}$"

# ===============================================================================
# INTEGRATION POINTS FOR TEAMMATES
# ===============================================================================

def parse_command(input_str: str) -> List[str]:
    """
    Parse command line input into tokens.
    
    STUB IMPLEMENTATION - Max will replace this with robust parser
    that handles quotes, escaping, and complex tokenization.
    
    Args:
        input_str: Raw command line input
        
    Returns:
        List of command tokens
    """
    try:
        # Simple tokenization using shlex - Max will enhance this
        return shlex.split(input_str)
    except ValueError as e:
        print_error(f"Parse error: {e}")
        return []

def execute_command(args: List[str], background: bool = False) -> int:
    """
    Execute external command using subprocess.
    
    STUB IMPLEMENTATION - Max will replace this with fork/exec approach
    and proper process management.
    
    Args:
        args: Command and arguments as list
        background: Whether to run in background
        
    Returns:
        Exit status of command
    """
    if not args:
        return 1
    
    # For now, just show what would be executed
    command_str = " ".join(f"'{arg}'" for arg in args)
    if background:
        command_str += " &"
    print(f"DEBUG: Would execute: {command_str}")
    
    # Simulate successful execution
    return 0

def is_builtin_command(command: str) -> bool:
    """
    Check if command is a built-in shell command.
    
    BASIC IMPLEMENTATION - Jake will expand this with more built-ins.
    
    Args:
        command: Command name
        
    Returns:
        True if it's a built-in command
    """
    builtins = {
        "exit", "cd", "pwd", "help", "jobs", "history",
        "echo", "export", "unset", "alias"  # Jake will implement these
    }
    return command in builtins

def execute_builtin(args: List[str]) -> int:
    """
    Execute built-in shell command.
    
    BASIC IMPLEMENTATION - Jake will enhance with full feature set.
    
    Args:
        args: Command and arguments
        
    Returns:
        Exit status (0 for success, non-zero for error)
    """
    if not args:
        return 1
    
    command = args[0]
    from shell import shell_state
    
    if command == "pwd":
        print(get_current_directory())
        return 0
        
    elif command == "cd":
        # Change directory
        if len(args) > 1:
            target_dir = args[1]
        else:
            # No argument, go to home directory
            target_dir = os.path.expanduser("~")
        
        try:
            # Expand ~ and environment variables
            target_dir = os.path.expanduser(target_dir)
            target_dir = os.path.expandvars(target_dir)
            
            os.chdir(target_dir)
            shell_state.current_directory = get_current_directory()
            return 0
        except OSError as e:
            print_error(f"cd: {e}")
            return 1
            
    elif command == "help":
        show_help()
        return 0
        
    elif command == "jobs":
        from signals_mod import print_background_jobs
        print_background_jobs()
        return 0
        
    elif command == "history":
        show_history()
        return 0
        
    elif command == "echo":
        # Simple echo implementation
        if len(args) > 1:
            print(" ".join(args[1:]))
        else:
            print()
        return 0
        
    elif command == "export":
        # Simple environment variable setting - Jake will enhance
        if len(args) != 2 or "=" not in args[1]:
            print_error("export: usage: export VAR=value")
            return 1
        
        var, value = args[1].split("=", 1)
        os.environ[var] = value
        return 0
        
    elif command == "unset":
        # Remove environment variable - Jake will enhance
        if len(args) != 2:
            print_error("unset: usage: unset VAR")
            return 1
        
        var = args[1]
        if var in os.environ:
            del os.environ[var]
        return 0
        
    else:
        print_error(f"Unknown built-in command: {command}")
        return 1

def show_help():
    """Display help information"""
    help_text = """
Available commands:
  exit [code]     - Exit the shell with optional exit code
  cd [directory]  - Change current directory (default: home)
  pwd             - Print current working directory
  help            - Show this help message
  jobs            - List active background jobs
  history         - Show command history
  echo [text]     - Print text to stdout
  export VAR=val  - Set environment variable
  unset VAR       - Remove environment variable

Special operators:
  &               - Run command in background
  Ctrl+C          - Interrupt (doesn't exit shell)
  Ctrl+D          - Exit shell
  
Note: I/O redirection (>, <, |) will be implemented by Jake.
"""
    print(help_text.strip())

def show_history():
    """Display command history"""
    from shell import shell_state
    
    if not shell_state.command_history:
        print("No commands in history.")
        return
    
    print("Command history:")
    for i, cmd in enumerate(shell_state.command_history[-20:], 1):  # Show last 20
        print(f"  {i:2d}  {cmd}")

# ===============================================================================
# BACKGROUND PROCESS UTILITIES
# ===============================================================================

def handle_background_processes():
    """Handle background process management - called from main loop"""
    from signals_mod import handle_background_processes as handle_bg
    handle_bg()

def add_background_process(pid: int):
    """Add process to background tracking"""
    from signals_mod import add_background_process as add_bg
    add_bg(pid)
