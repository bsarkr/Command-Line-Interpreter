#ifndef SHELL_H
#define SHELL_H

// Standard C++ includes
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>

// POSIX system includes
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>
#include <pwd.h>
#include <climits>
#include <cstdlib>
#include <cstring>
#include <errno.h>

// Shell configuration
#define MAX_INPUT_SIZE 1024
#define PROMPT_SIZE 256

// Shell state structure
struct ShellState {
    bool running;
    std::string currentDirectory;
    std::string prompt;
    int lastExitStatus;
    std::vector<pid_t> backgroundProcesses;
};

// Global variables
extern ShellState g_shellState;
extern volatile sig_atomic_t g_sigintReceived;
extern volatile sig_atomic_t g_sigtstpReceived;

// Main shell functions (Bilash's responsibility)
void shell_loop();
void display_prompt();
std::string read_input();
void setup_signals();
void cleanup_shell();

// Signal handlers (Bilash's responsibility)  
void sigint_handler(int sig);
void sigtstp_handler(int sig);
void sigchld_handler(int sig);

// Process management (Bilash's responsibility)
void handle_background_processes();
void add_background_process(pid_t pid);
void remove_background_process(pid_t pid);
void print_background_jobs();

// Utility functions
void print_error(const std::string& message);
void print_info(const std::string& message);
std::string get_current_directory();
void set_prompt();

// Integration points for teammates (stub implementations provided)
std::vector<std::string> parse_command(const std::string& input);
int execute_command(const std::vector<std::string>& args, bool background = false);
bool is_builtin_command(const std::string& command);
int execute_builtin(const std::vector<std::string>& args);

#endif // SHELL_H
