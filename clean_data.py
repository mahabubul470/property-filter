import os

substring = "branch"  # replace with your desired substring
directory = "dataset"  # replace with the directory containing subdirectories with images

for root, dirs, files in os.walk(directory):
    for filename in files:
        if substring in filename or filename.lower().endswith('.gif'):
            os.remove(os.path.join(root, filename))
            print(f"{filename} deleted from {root}")
