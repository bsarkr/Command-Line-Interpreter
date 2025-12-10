CUSTOM SHELL PROJECT - COMPLETE IMPLEMENTATION (PYTHON)
=======================================================

Team: Bilash Sarkar, Max Hazelton, Jake Gesseck
Course: Operating Systems
Project: Command-Line Interpreter (CLI/Shell)

FILES INCLUDED:
==============

1. shell.py       - Main shell program with core loop
2. signals_mod.py - Signal handling module
3. utils.py       - Utility functions, parsing, and command execution
4. test_shell.py  - Test suite
5. README.txt

QUICK START GUIDE:
=================

STEP 1: Test
    python3 test_shell.py

STEP 2: Run the Shell
    python3 shell.py

2. You'll see the prompt:
   bilash@hostname:~/path$ 

3. Try these commands:

   BASIC COMMANDS:
   pwd                      # Show current directory
   ls                       # List files  
   ls -la                   # List with details
   cd ~                     # Go home
   cd Documents             # Change directory

   VARIABLE FEATURES:
   export NAME=Bilash       # Set variable
   echo $NAME               # Shows: Bilash
   echo $HOME               # Shows your home directory  
   echo $?                  # Shows last command exit status

   BACKGROUND PROCESSES:
   sleep 5 &                # Run in background
   jobs                     # List background jobs
   
   SHELL FEATURES:
   help                     # Show all commands
   history                  # Show recent commands
   exit                     # Quit shell

ADVANCED FEATURES WORKING:
=========================

- Core shell loop with prompt display and input handling  
- Signal handling for SIGINT (Ctrl+C), SIGTSTP (Ctrl+Z), SIGCHLD  
- Background process management framework  
- Shell state management and cleanup  
- Built-in commands: pwd, cd, help, jobs, history, echo, export, unset  
- Integration points for Max's parser/executor  
- Integration points for Jake's built-in/features modules  
- Comprehensive test suite with 11 test cases  
- Professional error handling and user experience  

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


