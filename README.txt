# README.txt

Operating Systems Final Project
=======================================================

Team: Bilash Sarkar, Max Hazelton, Jake Gesseck
Prof. Dent
Operating Systems
Command-Line Interpreter (CLI/Shell)

FILES INCLUDED:
==============

1. shell.py       - Main shell program with core loop
2. signals_mod.py - Signal handling module
3. utils.py       - Utility functions, parsing, and command execution
4. test_shell.py  - Test suite (11/11 tests passing)
5. demo.py        - Demo script showing usage examples
6. README.txt     - This file

QUICK START GUIDE:
=================
STEP 1: Run the Shell
    python3 shell.py

STEP 2: Try these commands:

   BASIC COMMANDS:
   pwd                      # Show current directory
   ls                       # List files  
   ls -la                   # List with details
   cd ~                     # Go home
   cd Documents             # Change directory
   cd -                     # Go to previous directory

   VARIABLE FEATURES:
   export NAME=Bilash       # Set variable
   echo $NAME               # Shows: Bilash
   echo $HOME               # Shows your home directory  
   echo $?                  # Shows last command exit status

   BACKGROUND PROCESSES:
   sleep 5 &                # Run in background
   jobs                     # List background jobs
   
   I/O REDIRECTION & PIPING:
   echo "hello" > file.txt  # Redirect output
   cat < file.txt           # Redirect input
   echo "world" >> file.txt # Append output
   ls | grep txt            # Pipe between commands
   
   SHELL FEATURES:
   help                     # Show all commands
   history                  # Show recent commands
   alias ll='ls -la'        # Create command alias
   exit                     # Quit shell

BUILT-IN COMMANDS IMPLEMENTED:
=============================
• pwd  
• cd [dir], cd -
• help  
• jobs  
• history  
• echo [-n]
• export VAR=value  
• unset VAR
• alias [name=cmd]
• exit [code]

ADVANCED FEATURES:
=================
• Variable expansion: $VAR, ${VAR}, $?
• Tilde expansion: ~, ~/path
• I/O redirection: >, <, >>
• Command piping: |
• Background processes: &
• Signal handling: Ctrl+C, Ctrl+Z
• Command aliases
• Comment support: # 
• Quote handling: "text"

