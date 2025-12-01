#include "shell.h"

// Global variable definitions
ShellState g_shellState;
volatile sig_atomic_t g_sigintReceived = 0;
volatile sig_atomic_t g_sigtstpReceived = 0;

void print_error(const std::string& message) {
    std::cerr << "shell: error: " << message << std::endl;
}

void print_info(const std::string& message) {
    std::cout << "shell: " << message << std::endl;
}

std::string get_current_directory() {
    char cwd[PATH_MAX];
    if (getcwd(cwd, sizeof(cwd)) != nullptr) {
        return std::string(cwd);
    } else {
        perror("getcwd");
        return "/";
    }
}

void set_prompt() {
    std::string cwd = g_shellState.currentDirectory;
    
    // Get home directory for path shortening
    const char* home = getenv("HOME");
    if (home == nullptr) {
        struct passwd* pw = getpwuid(getuid());
        if (pw != nullptr) {
            home = pw->pw_dir;
        }
    }
    
    // Shorten path if it starts with home
    if (home != nullptr) {
        std::string homeDir(home);
        if (cwd == homeDir) {
            cwd = "~";
        } else if (cwd.length() > homeDir.length() && 
                   cwd.substr(0, homeDir.length()) == homeDir) {
            cwd = "~" + cwd.substr(homeDir.length());
        }
    }
    
    // Get username
    std::string username = "user";
    const char* user = getenv("USER");
    if (user != nullptr) {
        username = user;
    } else {
        struct passwd* pw = getpwuid(getuid());
        if (pw != nullptr) {
            username = pw->pw_name;
        }
    }
    
    // Get hostname
    char hostname[HOST_NAME_MAX + 1];
    if (gethostname(hostname, sizeof(hostname)) != 0) {
        strcpy(hostname, "localhost");
    }
    
    // Create prompt: user@host:path$
    g_shellState.prompt = username + "@" + hostname + ":" + cwd + "$";
}

// Temporary implementations for teammate integration
// These will be replaced by Max and Jake

std::vector<std::string> parse_command(const std::string& input) {
    // Simple tokenizer - Max will replace with robust parser
    std::vector<std::string> tokens;
    std::istringstream iss(input);
    std::string token;
    
    while (iss >> token) {
        tokens.push_back(token);
    }
    
    return tokens;
}

int execute_command(const std::vector<std::string>& args, bool background) {
    // Placeholder implementation - Max will replace with fork/exec
    if (args.empty()) {
        return 1;
    }
    
    std::cout << "DEBUG: Would execute '" << args[0] << "'";
    for (size_t i = 1; i < args.size(); ++i) {
        std::cout << " '" << args[i] << "'";
    }
    if (background) {
        std::cout << " &";
    }
    std::cout << std::endl;
    
    return 0; // Success for now
}

bool is_builtin_command(const std::string& command) {
    // Basic built-ins - Jake will expand this
    return (command == "exit" || command == "cd" || command == "pwd" || 
            command == "help" || command == "jobs" || command == "history");
}

int execute_builtin(const std::vector<std::string>& args) {
    // Basic built-in implementations - Jake will enhance these
    if (args.empty()) {
        return 1;
    }
    
    const std::string& command = args[0];
    
    if (command == "pwd") {
        std::cout << get_current_directory() << std::endl;
        return 0;
        
    } else if (command == "cd") {
        std::string dir = (args.size() > 1) ? args[1] : "";
        
        if (dir.empty()) {
            // Go to home directory
            const char* home = getenv("HOME");
            if (home != nullptr) {
                dir = home;
            } else {
                print_error("HOME environment variable not set");
                return 1;
            }
        }
        
        if (chdir(dir.c_str()) != 0) {
            perror("cd");
            return 1;
        }
        
        g_shellState.currentDirectory = get_current_directory();
        return 0;
        
    } else if (command == "help") {
        std::cout << "Available commands:" << std::endl;
        std::cout << "  exit [code] - Exit the shell" << std::endl;
        std::cout << "  cd [dir]    - Change directory" << std::endl;
        std::cout << "  pwd         - Print working directory" << std::endl;
        std::cout << "  help        - Show this help" << std::endl;
        std::cout << "  jobs        - List background jobs" << std::endl;
        std::cout << "  history     - Command history (not yet implemented)" << std::endl;
        return 0;
        
    } else if (command == "jobs") {
        print_background_jobs();
        return 0;
        
    } else if (command == "history") {
        std::cout << "Command history feature will be implemented by Jake." << std::endl;
        return 0;
    }
    
    print_error("Unknown built-in command: " + command);
    return 1;
}
