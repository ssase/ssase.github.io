#!/usr/bin/env python3

import os
from datetime import datetime, timedelta
import argparse
import subprocess
import shutil

from string import ascii_lowercase
from slugify import slugify
from pathlib import Path

# Get current date and time and format them
now = datetime.now()- timedelta(days=0)
date_str = now.strftime('%Y-%m-%d')
time_str = now.strftime('%Y-%m-%d %H:%M:%S')

project_dir = Path(__file__).resolve().parent.parent
posts_dir = project_dir.joinpath("_posts")
img_dir = project_dir.joinpath(f"assets/img/{date_str}")
scripts_dir = project_dir.joinpath("tools/scripts/generate_img_lqip.js")
post_ext = 'md'

os.makedirs(posts_dir, exist_ok=True)
os.makedirs(img_dir, exist_ok=True)
destination_img_name = 'cover.png'

def get_stdin(prompt):
    return input(prompt).strip()

def ask(prompt, valid_options=None):
    while True:
        response = get_stdin(f"{prompt} [{'/'.join(valid_options)}] ")
        if not valid_options or response.lower() in valid_options:
            return response.lower()
        print(f"Invalid option. Please choose from {', '.join(valid_options)}.")

def lqip(img_path):
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

        # Print the command's standard error (if any)
        if result.stderr:
            print("Command Error:")
            print(result.stderr)
        
         # Print the command's standard output
        print("Command Output:")
        print("-----------------")
        print(result.stdout.replace("\n", ""))
        print("-----------------")
        return result.stdout.replace("\n", "")

    except subprocess.CalledProcessError as e:
        # If the command returns a non-zero exit code, catch the exception
        print(f"Command failed with return code {e.returncode}")
        print("Command Output:")
        print(e.stdout)
        print("Command Error:")
        print(e.stderr)

def create_new_post(posts_dir, new_post_ext, title, img_path):

    # Create the filename using the date and slugified title
    safe_title = slugify(title)
    filename = f"{date_str}-{safe_title}.{new_post_ext}"
    filepath = os.path.join(posts_dir, filename)
    imglqip = ''
    if img_path:
        imglqip = lqip(img_path)

    # Check if the file already exists and ask whether to overwrite it
    if os.path.exists(filepath):
        if ask(f"{filepath} already exists. Do you want to overwrite?", ['y', 'n']) == 'n':
            print("Operation cancelled.")
            return

    # YAML front matter template
    front_matter_template = f"""---
layout: post
title: {title.replace('&', '&amp;')}
date: {time_str} +0800
published: true
categories: [Animal, Insect]
tags: [bee]
# The categories of each post are designed to contain up to two elements, and the number of elements in tags can be zero to infinity.
# TAG names should always be lowercase
author: min
toc: false
comments: false
math: false
mermaid: false
# Mermaid is a great diagram generation tool
media_subpath: /assets/img/{date_str}
"""

    if imglqip:
        append_image_info = f"""image:
  path: {destination_img_name}
  lqip: {imglqip}
  alt: {title.replace('&', '&amp;')}
"""
        front_matter_template += append_image_info

    front_matter_template += "---"

    try:
        # Write the front matter and content to the file
        with open(filepath, 'w', encoding='utf-8') as post_file:
            post_file.write(front_matter_template)

        print(f"Creating new post: {filepath}")
    except Exception as e:
        # Handle any I/O errors that may occur during file writing
        print(f"An error occurred while creating the post: {e}")

parser = argparse.ArgumentParser(description="Create a new blog post.")
parser.add_argument('--title', type=str, help='The title of the new post')
parser.add_argument('--img', type=str, help='The cover img path of the new post')
args = parser.parse_args()

title = args.title if args.title else get_stdin("Enter a title for your post: ")
img_path = args.img if args.img else get_stdin("Enter a cover image's path for your post: ")
img_path = img_path.replace("'", "")

destination_img_path = img_dir.joinpath(destination_img_name)
img_num = 0
while os.path.exists(destination_img_path):
    img_num += 1;
    destination_img_name = 'cover' + f'{img_num}' + '.png'
    destination_img_path = img_dir.joinpath(destination_img_name)

# Move origin image to our blog's destination.
if img_path:
    shutil.move(img_path, destination_img_path)
    img_path = destination_img_path

create_new_post(posts_dir, post_ext, title, img_path)
