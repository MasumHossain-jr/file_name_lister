import os
from collections import defaultdict
from pathlib import Path

def get_unique_filename(base_name):
    """Generate a unique filename by adding incrementing numbers if needed"""
    counter = 0
    name, ext = os.path.splitext(base_name)
    while True:
        if counter == 0:
            test_name = f"{name}{ext}"
        else:
            test_name = f"{name}_{counter}{ext}"
        if not os.path.exists(test_name):
            return test_name
        counter += 1

def analyze_files():
    file_counts = defaultdict(int)
    total_files = 0
    
    # Get unique output filename
    output_file = get_unique_filename('file_analysis.txt')
    
    with open(output_file, 'w') as f:
        # Write the tree structure
        f.write("File Tree Structure:\n")
        f.write("===================\n\n")
        
        # First collect all root files and directories
        root_files = []
        root_dirs = []
        for item in os.listdir('.'):
            if os.path.isfile(item):
                root_files.append(item)
            elif os.path.isdir(item):
                root_dirs.append(item)
        
        # Process directories first with tree structure
        for dir_name in root_dirs:
            f.write(f"{dir_name}/\n")
            for root, dirs, files in os.walk(dir_name):
                level = root.replace(dir_name, '').count(os.sep)
                indent = ' ' * 4 * (level + 1)
                for file in files:
                    f.write(f"{indent}{file}\n")
                    _, ext = os.path.splitext(file)
                    ext = ext.lower()
                    file_counts[ext] += 1
                    total_files += 1
            f.write("\n")
        
        # Process root files with spacing between each
        for file in root_files:
            f.write(f"{file}\n\n")
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            file_counts[ext] += 1
            total_files += 1
        
        # Write the file type summary
        f.write("\nFile Type Summary:\n")
        f.write("=================\n")
        f.write(f"Total files: {total_files}\n\n")
        f.write("Extension | Count\n")
        f.write("--------- | -----\n")
        
        # Sort extensions by count (descending)
        for ext, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True):
            ext_display = ext if ext else 'no extension'
            f.write(f"{ext_display:9} | {count:5}\n")
    
    print(f"File analysis saved to {output_file}")

if __name__ == "__main__":
    analyze_files()
