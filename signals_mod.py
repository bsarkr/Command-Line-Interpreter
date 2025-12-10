# signals_mod.py
#!/usr/bin/env python3
"""
Signal Handling Module for Custom Shell

This module handles POSIX signals for the shell:
- SIGINT (Ctrl+C): Interrupt current operation but don't exit shell
- SIGTSTP (Ctrl+Z): Show message but don't suspend shell  
- SIGCHLD: Handle background process completion
"""

import os
import signal
import sys
from typing import List

# Global signal flags (will be set by shell.py)
shell_state = None


def setup_signal_handlers():
    """Setup custom signal handlers for the shell"""
    # Import here to avoid circular imports
    global shell_state
    from shell import shell_state as ss
    shell_state = ss

    # Handle SIGINT (Ctrl+C) - don't terminate shell
    signal.signal(signal.SIGINT, sigint_handler)

    # Handle SIGTSTP (Ctrl+Z) - don't suspend shell
    signal.signal(signal.SIGTSTP, sigtstp_handler)

    # Handle SIGCHLD - clean up background processes
    signal.signal(signal.SIGCHLD, sigchld_handler)


def sigint_handler(sig, frame):
    """Handle SIGINT (Ctrl+C) - interrupt but don't exit"""
    print("\nUse 'exit' to quit the shell.")
    # Don't terminate the shell, just return to prompt


def sigtstp_handler(sig, frame):
    """Handle SIGTSTP (Ctrl+Z) - show message but don't suspend"""
    print("\nShell suspension disabled. Use 'exit' to quit.")


def sigchld_handler(sig, frame):
    """Handle SIGCHLD - clean up terminated background processes"""
    if shell_state is None:
        return

    # Reap terminated child processes
    while True:
        try:
            pid, status = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break  # No more children to reap

            # Remove from background process list
            if pid in shell_state.background_processes:
                shell_state.background_processes.remove(pid)

                # Print completion message (if not in signal context)
                if os.WIFEXITED(status):
                    exit_status = os.WEXITSTATUS(status)
                    print(
                        f"\n[Process {pid}] Done (exit status: {exit_status})")
                elif os.WIFSIGNALED(status):
                    sig_num = os.WTERMSIG(status)
                    print(f"\n[Process {pid}] Terminated by signal {sig_num}")

        except OSError:
            break  # No more children


def handle_background_processes():
    """Check and clean up background processes (called from main loop)"""
    if shell_state is None:
        return

    # Check for completed background processes
    # Copy list for safe iteration
    for pid in shell_state.background_processes[:]:
        try:
            result_pid, status = os.waitpid(pid, os.WNOHANG)
            if result_pid == pid:
                # Process has completed
                shell_state.background_processes.remove(pid)

                if os.WIFEXITED(status):
                    exit_status = os.WEXITSTATUS(status)
                    print(f"[Process {pid}] Done (exit status: {exit_status})")
                elif os.WIFSIGNALED(status):
                    sig_num = os.WTERMSIG(status)
                    print(f"[Process {pid}] Terminated by signal {sig_num}")
        except OSError:
            # Process doesn't exist anymore
            if pid in shell_state.background_processes:
                shell_state.background_processes.remove(pid)


def add_background_process(pid: int):
    """Add a process to the background process list"""
    if shell_state is None:
        return

    shell_state.background_processes.append(pid)
    print(f"[Process {pid}] Started in background")


def print_background_jobs():
    """Print current background jobs"""
    if shell_state is None or not shell_state.background_processes:
        print("No active background jobs.")
        return

    print("Active background jobs:")
    for i, pid in enumerate(shell_state.background_processes):
        try:
            # Check if process still exists
            os.kill(pid, 0)  # Signal 0 checks existence without sending signal
            print(f"[{i + 1}] {pid} Running")
        except (ProcessLookupError, PermissionError):
            print(f"[{i + 1}] {pid} Done")
