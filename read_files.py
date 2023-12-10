import os

directory_path = r"C:\Nikil\Python\PROJECTS\P0 - Terminal Gamedev\SoR_v1\smooth_console"

# List all files in the directory
files = os.listdir(directory_path)

# Iterate over the files and read them
for file_name in files:
    file_path = os.path.join(directory_path, file_name)

    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            # Process the content as needed
            print(f"Content of {file_name} : \n{content}")
