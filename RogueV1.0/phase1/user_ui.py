import os
import sys
import time
from colorama import init, Fore
import phase2.file_management


init(autoreset=True)


banner_file = os.path.join("phase1", "banner.txt")  

# Custom color
VS_CODE_RED = "\033[38;5;196m"  

# Commands help text dictionary (more detailed)
COMMANDS_HELP = {
    "ls": "NAME\n    ls - List directory contents.\n\nSYNOPSIS\n    ls [-l] [-a]\n\nDESCRIPTION\n    -l: Long listing format.\n    -a: Include hidden files.",
    "cp": "NAME\n    cp - Copy files and directories.\n\nSYNOPSIS\n    cp [source] [destination]\n\nDESCRIPTION\n    -i: Interactive mode (prompt before overwrite).\n    -v: Verbose mode (show what is being done).",
    "mv": "NAME\n    mv - Move or rename files.\n\nSYNOPSIS\n    mv [source] [destination]\n\nDESCRIPTION\n    -i: Interactive mode (prompt before overwrite).\n    -v: Verbose mode (show what is being done).",
    "rm": "NAME\n    rm - Remove files or directories.\n\nSYNOPSIS\n    rm [-r] [-f] [file/directory]\n\nDESCRIPTION\n    -r: Recursive removal.\n    -f: Forced removal (no prompts).",
    "cat": "NAME\n    cat - Display or concatenate file contents.\n\nSYNOPSIS\n    cat [file1] [file2] ... [> or >>] [target_file]\n\nDESCRIPTION\n    View or concatenate file contents.",
}

# Detailed man pages
COMMANDS_MANUAL = {
    "ls": """NAME
    ls - List directory contents.

SYNOPSIS
    ls [-l] [-a]

DESCRIPTION
    The `ls` command displays the contents of the current directory.
    Options:
      -l   Long listing format, showing file details.
      -a   Include hidden files, which start with a dot (.) in their names.""",

    "cp": """NAME
    cp - Copy files and directories.

SYNOPSIS
    cp [source] [destination]

DESCRIPTION
    The `cp` command copies files or directories from a source to a destination.
    Options:
      -i   Interactive mode (prompt before overwrite).
      -v   Verbose mode (display details of the copying process).""",

    "mv": """NAME
    mv - Move or rename files.

SYNOPSIS
    mv [source] [destination]

DESCRIPTION
    The `mv` command moves or renames files and directories.
    Options:
      -i   Interactive mode (prompt before overwrite).
      -v   Verbose mode (display details of the moving process).""",

    "rm": """NAME
    rm - Remove files or directories.

SYNOPSIS
    rm [-r] [-f] [file/directory]

DESCRIPTION
    The `rm` command removes files or directories.
    Options:
      -r   Recursive mode to remove directories and their contents.
      -f   Force mode to bypass confirmation prompts.""",

    "cat": """NAME
    cat - Display or concatenate file contents.

SYNOPSIS
    cat [file1] [file2] ... [> or >>] [target_file]

DESCRIPTION
    The `cat` command is used to view or concatenate file contents. It can read multiple files and output them to the terminal or redirect to a file.
    Options:
      file1, file2 ...         Specify one or more source files.
      >                        Overwrite the target file with the contents.
      >>                       Append the contents to the target file.""",
}

def display_banner():
    if os.path.exists(banner_file):
        with open(banner_file, "r") as f:
            banner_content = f.read()
            print(Fore.GREEN + banner_content)  # Display the banner in green
    else:
        print(VS_CODE_RED + "Banner file 'banner.txt' not found!")

def display_prompt():
    user = os.getlogin()
    machine = "localhost"
    current_path = os.getcwd()
    dir_name = current_path.split(os.sep)[-1]
    print(f"{Fore.GREEN}{user}@{machine}:{Fore.CYAN}{current_path}\\{Fore.RED}{dir_name}$", end =" ")




def process_command(command):
    """Process the entered command with options."""
    parts = command.split()
    cmd = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []


    if "--help" in args:  # Check for `--help` 
        print(Fore.WHITE + COMMANDS_HELP.get(cmd, f"No help available for '{cmd}'"))
    elif cmd == "man" and args: # Check for `man` 
        show_manual(args[0])
    elif cmd == "ls":
        phase2.file_management.list_directory_contents(parts)
    elif cmd == "cd":
        phase2.file_management.handle_cd(args)
    elif cmd == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
    elif cmd == "exit":
        print(VS_CODE_RED + "Exiting RogueV1.0...")
        time.sleep(1)
        sys.exit(0)
    elif cmd == "cp":
        phase2.file_management.handle_cp(parts)
    elif cmd == "mv":
        phase2.file_management.handle_mv(parts)
    elif cmd == "rm":
        phase2.file_management.handle_rm(parts)
    elif cmd == "cat":
        phase2.file_management.handle_cat(parts)
    else:
        print(Fore.WHITE + f"Command '{command}' not found.")


def show_manual(command):

    manual_text = COMMANDS_MANUAL.get(command, f"No manual entry for '{command}'")
    print(Fore.WHITE + manual_text)

def run_terminal():

    display_banner()

    while True:
    
        display_prompt()

        command = input().strip()

        process_command(command)