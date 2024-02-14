#include <iostream>
#include <unordered_set>

// Function to perform the Collatz Conjecture and print the sequence
void collatzConjecture(int num) {
    std::unordered_set<int> visited; // Set to store visited numbers

    while (num != 1) {
        std::cout << num << " "; // Print the current number

        // Check for repeat points
        if (visited.find(num) != visited.end()) {
            std::cout << "(Repeat Point)" << std::endl;
            return;
        }

        visited.insert(num); // Mark the current number as visited

        // Update the current number based on Collatz Conjecture rules
        if (num % 2 == 0) {
            num /= 2;
        } else {
            num = 3 * num + 1;
        }
    }

    std::cout << 1 << std::endl; // Print the final number in the sequence (1)
}

int main() {
    int userInput;

    // Get user input for the starting number
    std::cout << "Enter a positive integer: ";
    std::cin >> userInput;

    // Validate user input
    if (userInput <= 0) {
        std::cerr << "Invalid input. Please enter a positive integer." << std::endl;
        return 1;
    }

    // Perform Collatz Conjecture and print the sequence
    std::cout << "Collatz Conjecture sequence: ";
    collatzConjecture(userInput);

    return 0;
}

