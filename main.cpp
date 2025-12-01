/*
===============================================================================
CUSTOM SHELL PROJECT - BILASH'S CORE IMPLEMENTATION
===============================================================================

Team: Bilash Sarkar, Max Hazelton, Jake Gesseck
Course: Operating Systems (CISC 3595)
Project: Command-Line Interpreter (CLI/Shell)

===============================================================================
PURE C++ FILES INCLUDED:
===============================================================================

1. shell.h      - Main header with all declarations and includes
2. main.cpp     - Core shell loop and main program (THIS FILE)
3. signals.cpp  - Signal handling (SIGINT, SIGTSTP, SIGCHLD)
4. utils.cpp    - Utility functions and stub implementations
5. test.cpp     - Test program to verify functionality

*/

#include "shell.h"

int main()
{
    // Display startup message
    std::cout << "=== Custom Shell v1.0 ===" << std::endl;
    std::cout << "Team: Bilash, Max, Jake" << std::endl;
    std::cout << "Type 'help' for commands or 'exit' to quit." << std::endl;
    std::cout << std::endl;

    // Initialize shell state
    g_shellState.running = true;
    g_shellState.lastExitStatus = 0;
    g_shellState.currentDirectory = get_current_directory();

    // Setup signal handlers
    setup_signals();

    // Set initial prompt
    set_prompt();

    // Enter main shell loop
    shell_loop();

    // Cleanup and exit
    cleanup_shell();

    return g_shellState.lastExitStatus;
}

void shell_loop()
{
    while (g_shellState.running)
    {
        try
        {
            // Handle background processes
            handle_background_processes();

            // Check for received signals
            if (g_sigintReceived)
            {
                g_sigintReceived = 0;
                std::cout << std::endl;
                continue;
            }

            if (g_sigtstpReceived)
            {
                g_sigtstpReceived = 0;
                std::cout << std::endl
                          << "Use 'exit' to quit the shell." << std::endl;
                continue;
            }

            // Display prompt and read input
            display_prompt();
            std::string input = read_input();

            // Skip empty input
            if (input.empty())
            {
                continue;
            }

            // Parse command
            std::vector<std::string> args = parse_command(input);
            if (args.empty())
            {
                continue;
            }

            // Check for background execution
            bool background = false;
            if (!args.empty() && args.back() == "&")
            {
                background = true;
                args.pop_back();
            }

            if (args.empty())
            {
                continue;
            }

            // Handle exit command specially
            if (args[0] == "exit")
            {
                if (args.size() > 1)
                {
                    try
                    {
                        g_shellState.lastExitStatus = std::stoi(args[1]);
                    }
                    catch (const std::exception &e)
                    {
                        print_error("Invalid exit code: " + args[1]);
                        g_shellState.lastExitStatus = 1;
                    }
                }
                g_shellState.running = false;
                break;
            }

            // Execute command (built-in or external)
            int status;
            if (is_builtin_command(args[0]))
            {
                status = execute_builtin(args);
                g_shellState.lastExitStatus = status;
            }
            else
            {
                status = execute_command(args, background);
                if (!background)
                {
                    g_shellState.lastExitStatus = status;
                }
            }

            // Update current directory and prompt
            g_shellState.currentDirectory = get_current_directory();
            set_prompt();
        }
        catch (const std::exception &e)
        {
            print_error("Shell error: " + std::string(e.what()));
        }
    }
}

void display_prompt()
{
    std::cout << g_shellState.prompt << " ";
    std::cout.flush();
}

std::string read_input()
{
    std::string input;

    if (!std::getline(std::cin, input))
    {
        if (std::cin.eof())
        {
            // Handle Ctrl+D
            std::cout << std::endl;
            g_shellState.running = false;
            return "";
        }

        if (std::cin.fail())
        {
            std::cin.clear();
            print_error("Error reading input");
            return "";
        }
    }

    return input;
}

void setup_signals()
{
    struct sigaction sa_int, sa_tstp, sa_chld;

    // SIGINT handler (Ctrl+C)
    sa_int.sa_handler = sigint_handler;
    sigemptyset(&sa_int.sa_mask);
    sa_int.sa_flags = SA_RESTART;
    if (sigaction(SIGINT, &sa_int, nullptr) == -1)
    {
        perror("sigaction SIGINT");
        exit(1);
    }

    // SIGTSTP handler (Ctrl+Z)
    sa_tstp.sa_handler = sigtstp_handler;
    sigemptyset(&sa_tstp.sa_mask);
    sa_tstp.sa_flags = SA_RESTART;
    if (sigaction(SIGTSTP, &sa_tstp, nullptr) == -1)
    {
        perror("sigaction SIGTSTP");
        exit(1);
    }

    // SIGCHLD handler (background process cleanup)
    sa_chld.sa_handler = sigchld_handler;
    sigemptyset(&sa_chld.sa_mask);
    sa_chld.sa_flags = SA_RESTART | SA_NOCLDSTOP;
    if (sigaction(SIGCHLD, &sa_chld, nullptr) == -1)
    {
        perror("sigaction SIGCHLD");
        exit(1);
    }
}

void cleanup_shell()
{
    std::cout << "Cleaning up shell resources..." << std::endl;

    // Wait for background processes
    if (!g_shellState.backgroundProcesses.empty())
    {
        std::cout << "Terminating background processes..." << std::endl;
        for (pid_t pid : g_shellState.backgroundProcesses)
        {
            int status;
            if (waitpid(pid, &status, WNOHANG) == 0)
            {
                kill(pid, SIGTERM);
                usleep(100000); // 100ms grace period
                if (waitpid(pid, &status, WNOHANG) == 0)
                {
                    kill(pid, SIGKILL);
                }
            }
        }
    }

    std::cout << "Shell exited with status: " << g_shellState.lastExitStatus << std::endl;
}
