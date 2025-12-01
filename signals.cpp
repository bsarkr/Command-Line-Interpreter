#include "shell.h"

void sigint_handler(int sig) {
    (void)sig; // Suppress unused parameter warning
    
    // Set flag for main loop to handle
    g_sigintReceived = 1;
    
    // Use write() as it's async-signal-safe
    const char* message = "\n";
    ssize_t result = write(STDERR_FILENO, message, 1);
    (void)result; // Suppress unused result warning
}

void sigtstp_handler(int sig) {
    (void)sig; // Suppress unused parameter warning
    
    // Set flag for main loop to handle
    g_sigtstpReceived = 1;
    
    // Show message using async-signal-safe function
    const char* message = "\nShell suspension disabled. Use 'exit' to quit.\n";
    ssize_t result = write(STDERR_FILENO, message, strlen(message));
    (void)result; // Suppress unused result warning
}

void sigchld_handler(int sig) {
    (void)sig; // Suppress unused parameter warning
    
    // Reap terminated child processes
    pid_t pid;
    int status;
    
    while ((pid = waitpid(-1, &status, WNOHANG)) > 0) {
        // Remove from background process list
        remove_background_process(pid);
    }
    
    // Restore errno
    errno = 0;
}

void handle_background_processes() {
    auto it = g_shellState.backgroundProcesses.begin();
    
    while (it != g_shellState.backgroundProcesses.end()) {
        pid_t pid = *it;
        int status;
        
        pid_t result = waitpid(pid, &status, WNOHANG);
        
        if (result == pid) {
            // Process completed
            if (WIFEXITED(status)) {
                std::cout << "[Process " << pid << "] Done (exit status: " 
                         << WEXITSTATUS(status) << ")" << std::endl;
            } else if (WIFSIGNALED(status)) {
                std::cout << "[Process " << pid << "] Terminated by signal " 
                         << WTERMSIG(status) << std::endl;
            }
            it = g_shellState.backgroundProcesses.erase(it);
        } else if (result == 0) {
            // Process still running
            ++it;
        } else {
            // Error or already reaped
            it = g_shellState.backgroundProcesses.erase(it);
        }
    }
}

void add_background_process(pid_t pid) {
    g_shellState.backgroundProcesses.push_back(pid);
    std::cout << "[Process " << pid << "] Started in background" << std::endl;
}

void remove_background_process(pid_t pid) {
    auto it = std::find(g_shellState.backgroundProcesses.begin(), 
                       g_shellState.backgroundProcesses.end(), pid);
    if (it != g_shellState.backgroundProcesses.end()) {
        g_shellState.backgroundProcesses.erase(it);
    }
}

void print_background_jobs() {
    if (g_shellState.backgroundProcesses.empty()) {
        std::cout << "No active background jobs." << std::endl;
        return;
    }
    
    std::cout << "Active background jobs:" << std::endl;
    for (size_t i = 0; i < g_shellState.backgroundProcesses.size(); ++i) {
        pid_t pid = g_shellState.backgroundProcesses[i];
        
        int status;
        pid_t result = waitpid(pid, &status, WNOHANG);
        
        if (result == 0) {
            std::cout << "[" << (i + 1) << "] " << pid << " Running" << std::endl;
        } else {
            std::cout << "[" << (i + 1) << "] " << pid << " Done" << std::endl;
        }
    }
}
