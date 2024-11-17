from genericpath import isdir
import os
import shutil
import stat  
from colorama import Fore


VS_CODE_RED = "\033[38;5;196m"


COMMANDS_HELP = {
    "ls": "NAME\n    ls - List directory contents.\n\nSYNOPSIS\n    ls [-l] [-a]",
    "cp": "NAME\n    cp - Copy files and directories.\n\nSYNOPSIS\n    cp [source] [destination]",
    "mv": "NAME\n    mv - Move or rename files.\n\nSYNOPSIS\n    mv [source] [destination]",
    "rm": "NAME\n    rm - Remove files or directories.\n\nSYNOPSIS\n    rm [-r] [-f] [file/directory]",
    "cat": "NAME\n    cat - Display or concatenate file contents.\n\nSYNOPSIS\n    cat [file1] [file2] ... [> or >>] [target_file]",
}
COMMANDS_MANUAL = {
    "ls": """NAME
    ls - List directory contents.

SYNOPSIS
    ls [-l] [-a]

DESCRIPTION
    The `ls` command lists files and directories in the current working directory.
    Options:
      -l   Display detailed information about each file.
      -a   Include hidden files.""",

    "cp": """NAME
    cp - Copy files and directories.

SYNOPSIS
    cp [source] [destination]

DESCRIPTION
    Copy files or directories from a source to a destination.
    Options:
      -i   Prompt before overwrite.
      -v   Display verbose output.""",

    "mv": """NAME
    mv - Move or rename files.

SYNOPSIS
    mv [source] [destination]

DESCRIPTION
    Move or rename files and directories.
    Options:
      -i   Prompt before overwrite.
      -v   Display verbose output.""",

    "rm": """NAME
    rm - Remove files or directories.

SYNOPSIS
    rm [-r] [-f] [file/directory]

DESCRIPTION
    Remove files or directories.
    Options:
      -r   Remove directories recursively.
      -f   Force removal without confirmation.""",

    "cat": """NAME
    cat - Display or concatenate file contents.

SYNOPSIS
    cat [file1] [file2] ... [> or >>] [target_file]

DESCRIPTION
    View or concatenate file contents.
    Options:
      file1, file2 ...         Specify one or more source files.
      >                        Overwrite the target file.
      >>                       Append to the target file.""",
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
    
    
    try:
        if not args:
            home_dir = os.path.expanduser("~")  # Handle home directory
            if os.path.isdir(home_dir):
                os.chdir(home_dir)
            else:
                print(f"Error: Home directory '{home_dir}' does not exist.")
        
        elif args[0] == "-":
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

def isItAFile(filename):
    if os.path.isfile(filename):
        return True
    else:
        print(Fore.RED + f"Warning: {filename} is not a file or does not exist.")
        return False


import os
from colorama import Fore

def isItAFile(filename):
    if os.path.isfile(filename):
        return True
    elif os.path.isdir(filename):
        print(Fore.RED + f"Warning: {filename} is a directory.")
        return False
    else:
        print(Fore.RED + f"Warning: {filename} dosent exist.")
        return False

def handle_cat(parts):
    if len(parts) < 2:
        print(Fore.RED + "Usage: cat [FileName]")
        return


    command = parts[0]  
    args = parts[1:]    


    overwrite = ">" in args
    txtAppend = ">>" in args


    compteur = 0  # Number of files before '>' or '>>'
    compteur2 = 0  # Number of files after '>' or '>>'
    cond = False

    for p in args:
        if cond:
            compteur2 += 1
        elif p != ">" and p != ">>":
            compteur += 1
        else:
            cond = True


    args = [p for p in args if p not in (">", ">>")]


    if len(args) == 1:
        filename = args[0]
        if isItAFile(filename):
            try:
                with open(filename, "r") as file:
                    for line in file:
                        print(line, end="")
            except Exception as e:
                print(Fore.RED + f"Error reading file '{filename}': {e}")

    # Case 2: Concatenate files into one
    elif len(args) > 1:
        if compteur2 == 1:  
            target = args[compteur]

            if overwrite:  
                if os.path.exists(target):
                    os.remove(target)

                for i in range(compteur):
                    source = args[i]
                    if isItAFile(source):
                        try:
                            with open(source, "r") as sourceFile:
                                with open(target, "a") as targetFile:
                                    for line in sourceFile:
                                        targetFile.write(line)
                        except Exception as e:
                            print(Fore.RED + f"Error copying from {source} to {target}: {e}")

            elif txtAppend:  
                for i in range(compteur):
                    source = args[i]
                    if isItAFile(source):
                        try:
                            with open(source, "r") as sourceFile:
                                with open(target, "a") as targetFile:
                                    for line in sourceFile:
                                        targetFile.write(line)
                        except Exception as e:
                            print(Fore.RED + f"Error appending from {source} to {target}: {e}")

            else:
                print(Fore.RED + "Error: Use '>' or '>>'.")

        else:
            print(Fore.RED + "Usage: cat file1 ... fileN (> or >>) target_file (one target file only)")

    else:
        print(Fore.RED + "Usage: cat [FileName]")
