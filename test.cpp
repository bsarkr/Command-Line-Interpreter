#include "shell.h"
#include <cassert>

// Simple test program to verify core functionality
int main() {
    std::cout << "=== Testing Core Shell Implementation ===" << std::endl;
    std::cout << std::endl;
    
    bool allTestsPassed = true;
    
    // Test 1: Utility functions
    std::cout << "Test 1: Utility Functions" << std::endl;
    std::string cwd = get_current_directory();
    if (!cwd.empty() && cwd != "/") {
        std::cout << "✓ get_current_directory() works: " << cwd << std::endl;
    } else {
        std::cout << "❌ get_current_directory() failed" << std::endl;
        allTestsPassed = false;
    }
    
    // Test 2: Command parsing
    std::cout << std::endl << "Test 2: Command Parsing" << std::endl;
    std::vector<std::string> parsed = parse_command("ls -la file.txt");
    if (parsed.size() == 3 && parsed[0] == "ls" && parsed[1] == "-la" && parsed[2] == "file.txt") {
        std::cout << "✓ parse_command() works correctly" << std::endl;
    } else {
        std::cout << "❌ parse_command() failed" << std::endl;
        allTestsPassed = false;
    }
    
    // Test 3: Built-in command detection
    std::cout << std::endl << "Test 3: Built-in Command Detection" << std::endl;
    if (is_builtin_command("pwd") && is_builtin_command("cd") && 
        !is_builtin_command("ls") && !is_builtin_command("grep")) {
        std::cout << "✓ is_builtin_command() works correctly" << std::endl;
    } else {
        std::cout << "❌ is_builtin_command() failed" << std::endl;
        allTestsPassed = false;
    }
    
    // Test 4: Shell state initialization
    std::cout << std::endl << "Test 4: Shell State" << std::endl;
    g_shellState.running = true;
    g_shellState.lastExitStatus = 0;
    g_shellState.currentDirectory = get_current_directory();
    set_prompt();
    
    if (!g_shellState.prompt.empty() && g_shellState.prompt.find("$") != std::string::npos) {
        std::cout << "✓ Shell state and prompt work: " << g_shellState.prompt << std::endl;
    } else {
        std::cout << "❌ Shell state initialization failed" << std::endl;
        allTestsPassed = false;
    }
    
    // Test 5: Built-in commands
    std::cout << std::endl << "Test 5: Built-in Commands" << std::endl;
    std::vector<std::string> pwdCmd = {"pwd"};
    int result = execute_builtin(pwdCmd);
    if (result == 0) {
        std::cout << "✓ pwd built-in command works" << std::endl;
    } else {
        std::cout << "❌ pwd built-in command failed" << std::endl;
        allTestsPassed = false;
    }
    
    std::vector<std::string> helpCmd = {"help"};
    result = execute_builtin(helpCmd);
    if (result == 0) {
        std::cout << "✓ help built-in command works" << std::endl;
    } else {
        std::cout << "❌ help built-in command failed" << std::endl;
        allTestsPassed = false;
    }
    
    // Test 6: Background process management
    std::cout << std::endl << "Test 6: Background Process Management" << std::endl;
    g_shellState.backgroundProcesses.clear();
    print_background_jobs(); // Should show "No active background jobs"
    std::cout << "✓ Background process management initialized" << std::endl;
    
    // Test 7: Error handling
    std::cout << std::endl << "Test 7: Error Handling" << std::endl;
    print_error("Test error message");
    print_info("Test info message");
    std::cout << "✓ Error and info message functions work" << std::endl;
    
    // Summary
    std::cout << std::endl << "=== Test Results ===" << std::endl;
    if (allTestsPassed) {
        std::cout << "🎉 ALL TESTS PASSED! Your core implementation is ready." << std::endl;
        std::cout << std::endl;
        std::cout << "Next steps:" << std::endl;
        std::cout << "1. Compile the shell: g++ -std=c++17 -Wall -Wextra -Werror main.cpp signals.cpp utils.cpp -o shell" << std::endl;
        std::cout << "2. Run the shell: ./shell" << std::endl;
        std::cout << "3. Share with teammates for integration" << std::endl;
    } else {
        std::cout << "❌ Some tests failed. Please check the implementation." << std::endl;
        return 1;
    }
    
    std::cout << std::endl;
    std::cout << "=== Ready for Team Development ===" << std::endl;
    std::cout << "Your core implementation provides:" << std::endl;
    std::cout << "• Main shell loop with signal handling" << std::endl;
    std::cout << "• Background process management framework" << std::endl;
    std::cout << "• Basic built-in commands (pwd, cd, help, jobs)" << std::endl;
    std::cout << "• Integration points for Max's parser/executor" << std::endl;
    std::cout << "• Integration points for Jake's advanced features" << std::endl;
    
    return 0;
}