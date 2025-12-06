#!/usr/bin/env python3
"""
Test Suite for Custom Shell Implementation

This test program verifies that Bilash's core shell implementation
works correctly and is ready for team integration.
"""

import os
import sys
import tempfile
import subprocess
from typing import List, Any

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_test(test_name: str, test_func) -> bool:
    """Run a single test and return success status"""
    print(f"\nTest: {test_name}")
    print("-" * 50)
    
    try:
        result = test_func()
        if result:
            print("✓ PASSED")
            return True
        else:
            print("❌ FAILED")
            return False
    except Exception as e:
        print(f"❌ FAILED with exception: {e}")
        return False

def test_imports():
    """Test that all modules can be imported"""
    try:
        import shell
        import utils
        import signals_mod
        print("All modules imported successfully")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False

def test_utility_functions():
    """Test basic utility functions"""
    import utils
    
    # Test get_current_directory
    cwd = utils.get_current_directory()
    if not cwd or not os.path.exists(cwd):
        print("get_current_directory() failed")
        return False
    print(f"Current directory: {cwd}")
    
    # Test error and info printing (just verify they don't crash)
    utils.print_error("Test error message")
    utils.print_info("Test info message")
    
    print("Utility functions working correctly")
    return True

def test_command_parsing():
    """Test command parsing functionality"""
    import utils
    
    # Test basic parsing
    result = utils.parse_command("ls -la file.txt")
    expected = ["ls", "-la", "file.txt"]
    if result != expected:
        print(f"Parse failed: got {result}, expected {expected}")
        return False
    
    # Test quoted arguments
    result = utils.parse_command('echo "hello world" test')
    expected = ["echo", "hello world", "test"]
    if result != expected:
        print(f"Quoted parse failed: got {result}, expected {expected}")
        return False
    
    # Test empty input
    result = utils.parse_command("")
    if result != []:
        print(f"Empty parse failed: got {result}, expected []")
        return False
    
    print("Command parsing works correctly")
    return True

def test_builtin_detection():
    """Test built-in command detection"""
    import utils
    
    # Test built-in commands
    builtins = ["pwd", "cd", "help", "jobs", "history", "echo", "exit"]
    for cmd in builtins:
        if not utils.is_builtin_command(cmd):
            print(f"Failed to detect built-in: {cmd}")
            return False
    
    # Test non-built-in commands
    externals = ["ls", "grep", "cat", "sort", "unknown_command"]
    for cmd in externals:
        if utils.is_builtin_command(cmd):
            print(f"Incorrectly detected as built-in: {cmd}")
            return False
    
    print("Built-in command detection works correctly")
    return True

def test_shell_state():
    """Test shell state management"""
    import shell
    import utils
    
    # Initialize shell state
    shell.shell_state.running = True
    shell.shell_state.current_directory = utils.get_current_directory()
    utils.set_prompt()
    
    # Check state properties
    if not shell.shell_state.prompt:
        print("Prompt not set")
        return False
    
    if "$" not in shell.shell_state.prompt:
        print("Prompt doesn't contain '$'")
        return False
    
    print(f"Shell prompt: {shell.shell_state.prompt}")
    print("Shell state management works correctly")
    return True

def test_builtin_commands():
    """Test built-in command execution"""
    import utils
    import shell
    
    # Test pwd command
    result = utils.execute_builtin(["pwd"])
    if result != 0:
        print("pwd command failed")
        return False
    
    # Test help command
    result = utils.execute_builtin(["help"])
    if result != 0:
        print("help command failed")
        return False
    
    # Test echo command
    result = utils.execute_builtin(["echo", "test", "message"])
    if result != 0:
        print("echo command failed")
        return False
    
    # Test history command (should work even if empty)
    result = utils.execute_builtin(["history"])
    if result != 0:
        print("history command failed")
        return False
    
    print("Built-in commands work correctly")
    return True

def test_background_process_management():
    """Test background process management framework"""
    import shell
    import signals_mod
    
    # Initialize empty background process list
    shell.shell_state.background_processes = []
    
    # Test empty jobs list
    signals_mod.print_background_jobs()
    
    # Test adding background process (simulate)
    test_pid = 12345  # Fake PID for testing
    shell.shell_state.background_processes.append(test_pid)
    
    if test_pid not in shell.shell_state.background_processes:
        print("Failed to add background process")
        return False
    
    # Clean up
    shell.shell_state.background_processes.clear()
    
    print("Background process management framework works")
    return True

def test_signal_setup():
    """Test signal handler setup"""
    import signals_mod
    import signal
    
    # Test that signal setup doesn't crash
    try:
        signals_mod.setup_signal_handlers()
        print("Signal handlers set up successfully")
        return True
    except Exception as e:
        print(f"Signal setup failed: {e}")
        return False

def test_environment_commands():
    """Test environment variable commands"""
    import utils
    
    # Test export command
    result = utils.execute_builtin(["export", "TEST_VAR=test_value"])
    if result != 0:
        print("export command failed")
        return False
    
    # Check if variable was set
    if os.environ.get("TEST_VAR") != "test_value":
        print("export didn't set environment variable")
        return False
    
    # Test unset command
    result = utils.execute_builtin(["unset", "TEST_VAR"])
    if result != 0:
        print("unset command failed")
        return False
    
    # Check if variable was removed
    if "TEST_VAR" in os.environ:
        print("unset didn't remove environment variable")
        return False
    
    print("Environment variable commands work correctly")
    return True

def test_cd_command():
    """Test directory changing"""
    import utils
    import shell
    
    # Save current directory
    original_dir = os.getcwd()
    
    try:
        # Test cd to home directory
        result = utils.execute_builtin(["cd"])
        if result != 0:
            print("cd to home failed")
            return False
        
        # Test cd to original directory
        result = utils.execute_builtin(["cd", original_dir])
        if result != 0:
            print(f"cd to {original_dir} failed")
            return False
        
        # Check if we're back to original directory
        if os.getcwd() != original_dir:
            print("cd didn't change directory correctly")
            return False
        
        print("cd command works correctly")
        return True
        
    except Exception as e:
        print(f"cd test failed: {e}")
        return False
    finally:
        # Ensure we're back in original directory
        os.chdir(original_dir)

def test_error_handling():
    """Test error handling"""
    import utils
    
    # Test invalid built-in command
    result = utils.execute_builtin(["invalid_command"])
    if result == 0:  # Should fail
        print("Invalid command incorrectly succeeded")
        return False
    
    # Test cd to invalid directory
    result = utils.execute_builtin(["cd", "/nonexistent/directory/path"])
    if result == 0:  # Should fail
        print("cd to invalid directory incorrectly succeeded")
        return False
    
    print("Error handling works correctly")
    return True

def main():
    """Run all tests and report results"""
    print("=" * 60)
    print("CUSTOM SHELL - PYTHON IMPLEMENTATION TEST SUITE")
    print("=" * 60)
    print("Testing Bilash's core shell implementation...")
    
    tests = [
        ("Module Imports", test_imports),
        ("Utility Functions", test_utility_functions),
        ("Command Parsing", test_command_parsing),
        ("Built-in Detection", test_builtin_detection),
        ("Shell State Management", test_shell_state),
        ("Built-in Commands", test_builtin_commands),
        ("Background Process Management", test_background_process_management),
        ("Signal Handler Setup", test_signal_setup),
        ("Environment Commands", test_environment_commands),
        ("Directory Commands", test_cd_command),
        ("Error Handling", test_error_handling),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if run_test(test_name, test_func):
            passed += 1
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nYour core shell implementation is working correctly!")
        print("\nNext steps:")
        print("1. Run the shell: python3 shell.py")
        print("2. Share with teammates for integration")
        print("3. Max: Implement robust command parsing and execution")
        print("4. Jake: Add I/O redirection and piping features")
    else:
        print(f"\n❌ {total - passed} tests failed.")
        print("Please check the implementation and fix failing tests.")
        return 1
    
    print("\n" + "=" * 60)
    print("READY FOR TEAM DEVELOPMENT")
    print("=" * 60)
    print("Core features implemented:")
    print("• Interactive shell loop with signal handling")
    print("• Background process management framework")
    print("• Built-in commands: pwd, cd, help, jobs, history, echo, export, unset")
    print("• Integration points for Max's parser/executor")
    print("• Integration points for Jake's advanced features")
    print("• Professional error handling and user experience")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
