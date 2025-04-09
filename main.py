# Main file to launch the application

import controller as c
import sys # Needed for clearing screen based on OS, but for simplicity using ANSI escape code

def main():
    # Clear screen at the beginning
    print("\033[H\033[J", end="")
    
    try:
        # Initialize and run the controller
        c.run()
    except KeyboardInterrupt:
        # Handle graceful exit on Ctrl+C
        # The controller's quit_application should handle saving data if needed
        pass # Exit gracefully

if __name__ == "__main__":
    main()