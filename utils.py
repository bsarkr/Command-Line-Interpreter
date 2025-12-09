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
import re
import signal
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

# Regex for $VAR, ${VAR}, and $?
_VAR_PATTERN = re.compile(r"\$(\w+|\{[^}]+\}|\?)")

def _expand_variables(token: str) -> str:
    """
    Expand shell-style variables in a single token.

    Supports:
      - $VAR
      - ${VAR}
      - $?  (last exit status from shell_state)
    """
    # Lazy import to avoid circular import at module import time
    from shell import shell_state

    def repl(match: re.Match) -> str:
        name = match.group(1)

        # Special case: $?
        if name == "?":
            return str(shell_state.last_exit_status)

        # Handle ${VAR}
        if name.startswith("{") and name.endswith("}"):
            name = name[1:-1]

        return os.environ.get(name, "")

    return _VAR_PATTERN.sub(repl, token)

def _expand_tilde(token: str) -> str:
    """
    Expand ~ and ~user in tokens.
    """
    if token.startswith("~"):
        return os.path.expanduser(token)
    return token

def parse_command(input_str: str) -> List[str]:
    """
    Parse command line input into tokens.

    Features:
      - Quote/escape-aware splitting via shlex
      - Support for comments starting with '#'
      - Variable expansion ($VAR, ${VAR}, $?)
      - Tilde expansion (~, ~user)
      - Keeps operators (> < >> | &) as tokens so the shell
        can later implement redirection and pipes.

    Args:
        input_str: Raw command line input

    Returns:
        List of command tokens
    """
    try:
        # shlex handles quotes and escaping similarly to a POSIX shell
        lexer = shlex.shlex(input_str, posix=True)
        lexer.whitespace_split = True
        lexer.commenters = "#"   # ignore comments outside quotes

        tokens = list(lexer)

        expanded_tokens: List[str] = []
        for tok in tokens:
            tok = _expand_variables(tok)
            tok = _expand_tilde(tok)
            expanded_tokens.append(tok)

        return expanded_tokens

    except ValueError as e:
        print_error(f"Parse error: {e}")
        return []

def execute_command(args: List[str], background: bool = False) -> int:
    """
    Execute external command using fork/exec.

    - Foreground:
        * Parent waits for the child with waitpid()
        * Returns the child's exit status.
    - Background:
        * Parent does NOT wait.
        * Registers the PID with add_background_process().
        * Returns 0 if the process started successfully.

    Error conventions:
        127 -> command not found
        126 -> permission denied
        1   -> generic failure
    """
    if not args:
        return 1

    try:
        pid = os.fork()
    except OSError as e:
        print_error(f"fork failed: {e}")
        return 1

    if pid == 0:
        # --- Child process ---
        # Reset signal handlers so Ctrl+C / Ctrl+Z affect the child normally
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTSTP, signal.SIG_DFL)

        try:
            # Replace the child process image with the requested command
            os.execvp(args[0], args)
        except FileNotFoundError:
            print_error(f"{args[0]}: command not found")
            os._exit(127)
        except PermissionError:
            print_error(f"{args[0]}: permission denied")
            os._exit(126)
        except OSError as e:
            print_error(f"{args[0]}: {e}")
            os._exit(1)

    else:
        # --- Parent process ---
        if background:
            # Track as a background job (signals_mod will manage it)
            add_background_process(pid)
            # Don't wait for it; shell returns to prompt immediately
            return 0

        # Foreground: wait for this specific child
        while True:
            try:
                _, status = os.waitpid(pid, 0)
                break
            except InterruptedError:
                # Interrupted by a signal; retry the wait
                continue
            except ChildProcessError:
                # Child may already have been reaped by SIGCHLD handler
                return 0

        if os.WIFEXITED(status):
            return os.WEXITSTATUS(status)
        elif os.WIFSIGNALED(status):
            # Typical shell convention: 128 + signal number
            return 128 + os.WTERMSIG(status)
        else:
            return 1

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
        "echo", "export", "unset", "alias"  # Jake
    }
    return command in builtins

def execute_builtin(args: List[str], shell_state=None) -> int:
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
    
    if command == "pwd":
        print(get_current_directory())
        return 0
        
    elif command == "cd": # Change directory
        if len(args) > 2:
            print_error("cd: too many arguments")
            return 1
        if len(args) > 1:
            target_dir = args[1]

            if target_dir == "-":
                if hasattr(shell_state, "previous_directory") and shell_state.previous_directory:
                    target_dir = shell_state.previous_directory
                    print(target_dir)
                else:
                    print_error("cd: OLDPWD not set")
                    return 1
        else:
            # No argument, go to home directory
            target_dir = os.path.expanduser("~")
        
        try:
            if shell_state:
                shell_state.previous_directory = shell_state.current_directory

            target_dir = os.path.expanduser(target_dir)
            target_dir = os.path.expandvars(target_dir)
            
            os.chdir(target_dir)
            if shell_state:
                shell_state.current_directory = get_current_directory()

            return 0
        except OSError as e:
            if e.errno == 2:
                print_error(f"cd: no such file or directory: {target_dir}")
            else:
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
        echo_args = args[1:]
        newline = True

        if echo_args and echo_args[0] == "-n":
            newline = False
            echo_args = echo_args[1:]
        
        output = " ".join(echo_args) if echo_args else ""

        if newline:
            print(output)
        else:
            print(output, end="")

        return 0
        
    elif command == "export":
        # Simple environment variable setting - Jake
        if len(args) == 1:
            for key, value in os.environ.items():
                print(f"export {key}='{value}'")
            return 0
        for arg in args[1:]:
            if "=" not in arg:
                if arg in os.environ:
                    continue
                else:
                    print_error(f"export: invalid argument: {arg}")
                    return 1
            else:
                var, value = arg.split("=", 1)
                value = value.strip("'\"")
                os.environ[var] = value
        return 0
              
    elif command == "unset":
        # Remove environment variable - Jake
        if len(args) != 2:
            print_error("unset: usage: unset VAR")
            return 1
        
        var = args[1]
        if var in os.environ:
            del os.environ[var]
        return 0  

    elif command == "exit":
        exit_code = 0
        if len(args) > 1:
            try:
                exit_code = int(args[1])
            except ValueError:
                print_error(f"Invalid exit code: {args[1]}")
                exit_code = 1

        sys.exit(exit_code)
    
    elif command == "alias":
        if not shell_state:
            print_error("alias: shell state not provided")
            return 1
        
        if len(args) == 1:
            if hasattr(shell_state, 'aliases') and shell_state.aliases:
                for name, value in shell_state.aliases.items():
                    print(f"alias {name}='{value}'")
            return 0
        elif len(args) == 2 and "=" in args[1]:
            name, value = args[1].split("=", 1)
            value = value.strip("'\"")
            if not hasattr(shell_state, 'aliases'):
                shell_state.aliases = {}
            shell_state.aliases[name] = value
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
