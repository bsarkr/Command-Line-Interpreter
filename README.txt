CUSTOM SHELL PROJECT - (PYTHON)
=============================================================

Team: Bilash Sarkar, Max Hazelton, Jake Gesseck
Course: Operating Systems
Project: Command-Line Interpreter (CLI/Shell)

FILES INCLUDED:
==============

1. shell.py       - Main shell program with core loop (265+ lines)
2. signals_mod.py - Signal handling module (120+ lines)  
3. utils.py       - Utility functions, parsing, and command execution (260+ lines)
4. test_shell.py  - Comprehensive test suite (380+ lines)
5. README.txt     - This instruction file

Total: 1000+ lines of production-ready Python code

QUICK START GUIDE:
=================

STEP 1: Test Your Implementation
    python3 test_shell.py

STEP 2: Run the Shell
    python3 shell.py

STEP 3: Try Basic Commands
    pwd
    help
    cd ~
    echo "Hello World"
    export TEST_VAR=value
    jobs
    history
    exit

BILASH'S COMPLETED RESPONSIBILITIES:
===================================

✓ Core shell loop with prompt display and input handling  
✓ Signal handling for SIGINT (Ctrl+C), SIGTSTP (Ctrl+Z), SIGCHLD  
✓ Background process management framework  
✓ Shell state management and cleanup  
✓ Built-in commands: pwd, cd, help, jobs, history, echo, export, unset  
✓ Integration points for Max's parser/executor  
✓ Integration points for Jake's built-in/features modules  
✓ Comprehensive test suite with 11 test cases  
✓ Professional error handling and user experience  

TEAM INTEGRATION POINTS:
=======================

FOR MAX (Parser & Executor):  
Completed and integrated in utils.py:

• parse_command(input_str) → List[str]  
  Handles:
  - Quotes  
  - Escaping  
  - Comments (#)  
  - Variable expansion ($VAR, ${VAR}, $?)  
  - Tilde expansion (~, ~user)  
  - Preserves operators (> < >> | &)  

• execute_command(args, background=False) → int  
  Fully implemented using:
  - fork()  
  - execvp()  
  - waitpid()  
  - Background job registration  
  - Proper exit status propagation  

FOR JAKE (Built-ins & Features):
• is_builtin_command(command)  
• execute_builtin(args)  
• I/O redirection (>, <, >>)  
• Piping (|)  
• Alias support  
• Advanced job control  

PYTHON ADVANTAGES OVER C++:
===========================

✓ Cleaner, more readable code  
✓ Automatic memory management  
✓ Rich standard library: os, signal, subprocess  
✓ Easier parsing with shlex  
✓ Exception handling  
✓ Faster development / debugging  
✓ Cross-platform compatibility  
✓ No compilation required  

ARCHITECTURE HIGHLIGHTS:
=======================

• Modular design:  
  - shell.py: Main shell loop  
  - utils.py: Parsing, execution, built-ins  
  - signals_mod.py: Signal handling + background jobs  
  - test_shell.py: Automated testing  

• Professional Python practices:  
  - Type hints  
  - Docstrings  
  - PEP 8 style  
  - Error handling  
  - Clean separation of concerns  

BUILT-IN COMMANDS IMPLEMENTED:
=============================

• pwd  
• cd [dir]  
• help  
• jobs  
• history  
• echo  
• export VAR=value  
• unset VAR  
• exit [code]  

==========================================
INTERACTIVE TESTING & FEATURE DEMONSTRATION
==========================================

The following examples allow you to manually test shell behavior,
parsing logic, variable expansion, background processes, and OS-level
execution.

------------------------------------------
1. BASIC NAVIGATION & BUILT-INS
------------------------------------------
pwd  
cd ~  
cd Desktop  
pwd  
history  
help  

------------------------------------------
2. EXTERNAL COMMAND EXECUTION
------------------------------------------
ls  
ls -la  
echo Hello World  

------------------------------------------
3. QUOTE & WHITESPACE PARSING
------------------------------------------
echo "hello world"  
echo   spaced    out   tokens  
echo "multi-word argument" test  

------------------------------------------
4. VARIABLE EXPANSION
------------------------------------------
export NAME=Max  
echo $NAME  
echo $HOME  
echo $?  
unset NAME  

------------------------------------------
5. TILDE EXPANSION
------------------------------------------
echo ~  
echo ~/Documents  
cd ~  
pwd  

------------------------------------------
6. COMMENT HANDLING
------------------------------------------
echo hello world   # ignored by parser  
echo "a # b"       # # inside quotes preserved  

------------------------------------------
7. BACKGROUND JOBS
------------------------------------------
sleep 5 &  
jobs       # should show process as Running  

After 5 seconds:  
[Process XXXX] Done (exit status: 0)

------------------------------------------
8. SIGNAL HANDLING (FOREGROUND)
------------------------------------------
sleep 100  
(Press Ctrl+C)  

Output:
Use 'exit' to quit the shell.

Shell remains active.

------------------------------------------
9. ERROR HANDLING
------------------------------------------
nosuchcommand  
→ shell: error: nosuchcommand: command not found  

cd /nonexistent  
→ shell: error: cd: [Errno 2] No such file or directory  

------------------------------------------
10. EXIT BEHAVIOR
------------------------------------------
exit  
exit 0  
exit 5  

Shell prints cleanup messages and exits with specified status.  

PROJECT STATUS:
==============

✓ Core shell foundation  
✓ Max’s parser and executor fully integrated  
✓ Jake’s built-in enhancements ready for extension  
✓ All tests pass (11/11)  
✓ Ready for final submission and presentation  


