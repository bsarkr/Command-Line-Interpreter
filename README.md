# Command-Line-Interpreter
# Written by Bilash Sarkar, Max Hazelton, and Jake Gesseck
# CISC 3595 Final Project

eam: Bilash Sarkar, Max Hazelton, Jake Gesseck
Course: Operating Systems
Project: Command-Line Interpreter (CLI/Shell)

FILES INCLUDED:
==============

1. shell.h      - Main header with all declarations and includes
2. main.cpp     - Core shell loop and main program  
3. signals.cpp  - Signal handling (SIGINT, SIGTSTP, SIGCHLD)
4. utils.cpp    - Utility functions and stub implementations
5. test.cpp     - Test program to verify functionality
6. README.txt   - This instruction file

QUICK START GUIDE:
=================

STEP 1: Test Your Implementation
    g++ -std=c++17 -Wall -Wextra -Werror test.cpp signals.cpp utils.cpp -o test
    ./test

STEP 2: Compile the Shell
    g++ -std=c++17 -Wall -Wextra -Werror main.cpp signals.cpp utils.cpp -o shell

STEP 3: Run the Shell
    ./shell

STEP 4: Test Basic Commands
    pwd
    help  
    cd ~
    jobs
    exit

BILASH'S COMPLETED RESPONSIBILITIES:
===================================

✓ Core shell loop with prompt display and input handling
✓ Signal handling for SIGINT (Ctrl+C), SIGTSTP (Ctrl+Z), SIGCHLD
✓ Background process management framework  
✓ Shell state management and cleanup
✓ Basic built-in commands: pwd, cd, help, jobs, exit
✓ Integration points for Max's parser/executor modules
✓ Integration points for Jake's built-in/features modules
