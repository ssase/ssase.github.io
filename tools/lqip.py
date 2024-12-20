#!/usr/bin/env python3

import subprocess
import argparse
from pathlib import Path

def get_stdin(prompt):
    return input(prompt).strip()

project_dir = Path(__file__).resolve().parent.parent
scripts_dir = project_dir.joinpath("tools/scripts/generate_img_lqip.js")

parser = argparse.ArgumentParser(description="Create a new blog post.")
parser.add_argument('--img', type=str, help='The cover img path of the new post')
args = parser.parse_args()

img_path = args.img if args.img else get_stdin("Enter a cover image's path for your post: ")
img_path = img_path.replace("'", "")

# Move origin image to our blog's destination.
if not img_path:
    print("The image path is empty, please enter a real image path.")
    exit(-1)

print("-----------------")
print(img_path)
print("-----------------")

# Define the command and its arguments
command = [
    "node",  # The command to execute (Node.js)
    scripts_dir,  # The script to run
    img_path  # The image file path
]

# Execute the command and capture the output
try:
    result = subprocess.run(
        command,  # The command and its arguments
        capture_output=True,  # Capture standard output and standard error
        text=True,  # Return the output as strings (not bytes)
        check=True  # Raise an exception if the command returns a non-zero exit code
    )

    # Print the command's standard output
    print("Command Output:")
    print("-----------------")
    print(result.stdout)
    print("-----------------")

    # Print the command's standard error (if any)
    if result.stderr:
        print("Command Error:")
        print(result.stderr)
except subprocess.CalledProcessError as e:
    # If the command returns a non-zero exit code, catch the exception
    print(f"Command failed with return code {e.returncode}")
    print("Command Output:")
    print(e.stdout)
    print("Command Error:")
    print(e.stderr)