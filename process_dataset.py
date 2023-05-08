import os
import hashlib

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()
        hash = hashlib.sha256(content).hexdigest()
        return hash

def filter_unique_files(directory):
    file_hashes = {}
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(subdir, file)
            file_hash = get_file_hash(filepath)
            if file_hash in file_hashes:
                os.remove(filepath)  # remove duplicate file
                print(f'Removed duplicate file {filepath}')
            else:
                file_hashes[file_hash] = filepath

if __name__ == '__main__':
    filter_unique_files('dataset')
