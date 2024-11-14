import os
import sys
import time
from colorama import init, Fore
from phase2.file_management import handle_cp, handle_mv, handle_rm, list_directory_contents

# Initialize colorama
init(autoreset=True)

# Paths to important files
banner_file = os.path.join("phase1", "banner.txt")  # Ensure correct path to banner.txt

# Custom color
VS_CODE_RED = "\033[38;5;196m"  # Bright red similar to VS Code

# Commands help text dictionary (more detailed)
COMMANDS_HELP = {
    "ls": "Usage: ls [-l] [-a]\n\nList directory contents. Use -l for long listing format and -a for including hidden files.",
    "cp": "Usage: cp [source] [destination]\n\nCopy files from source to destination. Use -i for interactive mode, and -v for verbose output.",
    "mv": "Usage: mv [source] [destination]\n\nMove files from source to destination. Use -i for interactive mode, and -v for verbose output.",
    "rm": "Usage: rm [-r] [-f] [file/directory]\n\nRemove a file or directory. Use -r for recursive removal and -f for forced removal.",
}

# Detailed man pages
COMMANDS_MANUAL = {
    "ls": """ls - List directory contents
    Options:
    -l: Long listing format
    -a: Show all files, including hidden ones
    """,
    "cp": """cp - Copy files and directories
    Usage: cp [source] [destination]
    Options:
    -i: Interactive mode (prompt before overwrite)
    -v: Verbose mode (show what is being done)
    """,
    "mv": """mv - Move or rename files
    Usage: mv [source] [destination]
    Options:
    -i: Interactive mode (prompt before overwrite)
    -v: Verbose mode (show what is being done)
    """,
    "rm": """rm - Remove files or directories
    Usage: rm [-r] [-f] [file/directory]
    Options:
    -r: Remove directories recursively
    -f: Force removal (no prompts)
    """
}

def display_banner():
    if os.path.exists(banner_file):
        with open(banner_file, "r") as f:
            banner_content = f.read()
            print(Fore.GREEN + banner_content)  # Display the banner in green
    else:
        print(VS_CODE_RED + "Banner file 'banner.txt' not found!")

def display_prompt():
    """Displays a custom Linux-like terminal prompt."""
    user = os.getlogin()
    machine = "localhost"
    current_path = os.getcwd()
    dir_name = current_path.split(os.sep)[-1]
    print(f"{Fore.GREEN}{user}@{machine}:{Fore.CYAN}{current_path}\\{Fore.RED}{dir_name}$", end =" ")

from phase2.file_management import handle_cp, handle_mv, handle_rm, list_directory_contents, handle_cd

# Your other imports and code remain the same...

def process_command(command):
    """Process the entered command with options."""
    parts = command.split()
    cmd = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []

    # Check for `--help` or `man`
    if "--help" in args:
        print(Fore.WHITE + COMMANDS_HELP.get(cmd, f"No help available for '{cmd}'"))
    elif cmd == "man" and args:
        show_manual(args[0])
    elif cmd == "ls":
        list_directory_contents(parts)
    elif cmd == "cd":
        handle_cd(args)
    elif cmd == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
    elif cmd == "exit":
        print(VS_CODE_RED + "Exiting RogueV1.0...")
        time.sleep(1)
        sys.exit(0)
    elif cmd == "cp":
        handle_cp(parts)
    elif cmd == "mv":
        handle_mv(parts)
    elif cmd == "rm":
        handle_rm(parts)
    else:
        print(Fore.WHITE + f"Command '{command}' not found.")


def show_manual(command):
    """Display command manual information."""
    manual_text = COMMANDS_MANUAL.get(command, f"No manual entry for '{command}'")
    print(Fore.WHITE + manual_text)

def run_terminal():
    """Run the terminal loop for the entire process."""
    display_banner()

    while True:
        # Display the custom prompt
        display_prompt()

        # Capture user input
        command = input().strip()

        # Process the entered command
        process_command(command)
