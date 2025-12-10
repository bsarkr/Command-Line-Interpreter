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
5. README.txt

QUICK START GUIDE:
=================
STEP 1: Run the Shell
    python3 shell.py

Step 2: Try these commands:

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


