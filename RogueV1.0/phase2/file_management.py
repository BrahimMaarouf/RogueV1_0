# file_management.py
import os
from colorama import Fore

# Custom VS Code-like color
VS_CODE_RED = "\033[38;5;196m"

# Commands help text dictionary (move the 'cd' entry here too)
COMMANDS_HELP = {
    "ls": "Usage: ls [-l] [-a]",
    "cp": "Usage: cp [source] [destination]",
    "mv": "Usage: mv [source] [destination]",
    "rm": "Usage: rm [-r] [-f] [file/directory]",
    "cd": "Usage: cd [path] or cd .. or cd -"
}

def list_directory_contents(parts):
    """List contents of the current directory with options for long format and hidden files."""
    long_format = "-l" in parts
    show_all = "-a" in parts
    files = os.listdir(os.getcwd())

    if not show_all:
        files = [f for f in files if not f.startswith(".")]  # Exclude hidden files by default

    if long_format:
        for file in files:
            file_path = os.path.join(os.getcwd(), file)
            file_stats = os.stat(file_path)
            perms = stat.filemode(file_stats.st_mode)  # Get file permissions
            size = file_stats.st_size
            print(f"{perms} {size:>10} {file}")
    else:
        output = [
            (Fore.YELLOW + file if os.path.isdir(file) else Fore.WHITE + file)
            for file in files
        ]
        print(" ".join(output))

def handle_cp(parts):
    """Handle the 'cp' (copy) command with options."""
    interactive = "-i" in parts
    verbose = "-v" in parts

    # Remove options from parts to get correct source and destination
    parts = [p for p in parts if p not in ("-i", "-v")]

    if len(parts) != 3:
        print(VS_CODE_RED + COMMANDS_HELP["cp"])
        return

    source, destination = parts[1], parts[2]
    
    if interactive:
        confirm = input(f"Are you sure you want to overwrite {destination}? (y/n): ").lower()
        if confirm != 'y':
            print(Fore.YELLOW + "Aborted.")
            return
    
    try:
        shutil.copy(source, destination)
        if verbose:
            print(Fore.GREEN + f"Copied {source} to {destination}")
    except Exception as e:
        print(VS_CODE_RED + f"Error copying file: {e}")

def handle_mv(parts):
    """Handle the 'mv' (move) command with options."""
    interactive = "-i" in parts
    verbose = "-v" in parts

    # Remove options from parts to get correct source and destination
    parts = [p for p in parts if p not in ("-i", "-v")]

    if len(parts) != 3:
        print(VS_CODE_RED + COMMANDS_HELP["mv"])
        return

    source, destination = parts[1], parts[2]

    if interactive:
        confirm = input(f"Are you sure you want to overwrite {destination}? (y/n): ").lower()
        if confirm != 'y':
            print(Fore.YELLOW + "Aborted.")
            return

    try:
        shutil.move(source, destination)
        if verbose:
            print(Fore.GREEN + f"Moved {source} to {destination}")
    except Exception as e:
        print(VS_CODE_RED + f"Error moving file: {e}")

def handle_rm(parts):
    """Handle the 'rm' (remove) command with options."""
    recursive = "-r" in parts
    force = "-f" in parts

    # Remove options from parts to get correct target
    parts = [p for p in parts if p not in ("-r", "-f")]

    if len(parts) != 2:
        print(VS_CODE_RED + COMMANDS_HELP["rm"])
        return

    target = parts[1]

    try:
        if os.path.isdir(target):
            if recursive:
                shutil.rmtree(target)  # Remove directory and contents recursively
                print(Fore.GREEN + f"Removed directory {target}")
            else:
                print(VS_CODE_RED + f"Error: {target} is a directory. Use -r to remove it.")
        elif os.path.isfile(target):
            os.remove(target)  # Remove file
            print(Fore.GREEN + f"Removed file {target}")
        else:
            print(VS_CODE_RED + f"Error: {target} is neither a file nor a directory.")
    except Exception as e:
        if force:
            print(Fore.YELLOW + f"Force removal failed for {target}. Error: {e}")
        else:
            print(VS_CODE_RED + f"Error removing {target}: {e}")





# Global variables to store the last visited directories
prev_dir = None  # Stores the previous directory for cd -
next_dir = None  # Stores the current directory for cd +

def handle_cd(args):
    global prev_dir, next_dir
    
    """Handle the 'cd' (change directory) command."""
    try:
        if not args:
            # No path given, go to the home directory
            home_dir = os.path.expanduser("~")  # Handle home directory
            if os.path.isdir(home_dir):
                os.chdir(home_dir)
            else:
                print(f"Error: Home directory '{home_dir}' does not exist.")
        
        elif args[0] == "-":
            # Change to the previous directory or the one stored by cd +
            if next_dir:
                os.chdir(next_dir)
                prev_dir, next_dir = next_dir, prev_dir  # Swap the dirs for correct flow
            elif prev_dir:
                os.chdir(prev_dir)
            else:
                print("No previous directory to return to.")
        
        elif args[0] == "+":
            # Store the current directory for "cd +"
            next_dir = os.getcwd()
            print(f"Next directory stored: {next_dir}")
        
        elif args[0] == "\\":
            # Change to the root of the current drive (e.g., C:\ or D:\)
            drive, _ = os.path.splitdrive(os.getcwd())
            if drive:
                os.chdir(drive + "\\")  # Navigate to the root of the current drive
            else:
                print("Error: No drive detected.")
        
        elif args[0] == "~":
            # Change to the home directory of the current user (e.g., C:\Users\<username>)
            home_dir = os.path.expanduser("~")
            if os.path.isdir(home_dir):
                os.chdir(home_dir)
            else:
                print(f"Error: Home directory '{home_dir}' does not exist.")
        
        else:
            # Handle normal path change
            os.chdir(args[0])
        
        # Update the previous directory after successful change
        prev_dir = os.getcwd()
    
    except Exception as e:
        print(f"Error: {e}")