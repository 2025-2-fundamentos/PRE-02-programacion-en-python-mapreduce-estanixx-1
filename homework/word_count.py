"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path
import time
import shutil
import re
from itertools import groupby

# from toolz.itertoolz import concat, pluck


def copy_raw_files_to_input_folder(n):
    """Generate n copies of the raw files in the input folder"""
    # Create input directory if it doesn't exist
    input_dir = "files/input"
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    
    # Clear existing files in input directory
    for file in glob.glob(os.path.join(input_dir, "*")):
        os.remove(file)
    
    # Get all raw files
    raw_files = glob.glob("files/raw/*.txt")
    
    # Copy each raw file n times
    for i in range(n):
        for raw_file in raw_files:
            filename = os.path.basename(raw_file)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_{i:04d}{ext}"
            dest_path = os.path.join(input_dir, new_filename)
            shutil.copy2(raw_file, dest_path)


def load_input(input_directory):
    """Funcion load_input"""
    # Get all files in the input directory
    files = glob.glob(os.path.join(input_directory, "*.txt"))
    
    # Read all lines from all files
    lines = []
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines.extend(f.readlines())
    
    return lines


def preprocess_line(x):
    """Preprocess the line x"""
    # Convert to lowercase and remove punctuation, keep only letters and spaces
    x = x.lower()
    x = re.sub(r'[^a-z\s]', '', x)
    # Remove extra whitespace
    x = ' '.join(x.split())
    return x


def map_line(x):
    """Map a line to word-count pairs"""
    # Preprocess the line
    processed = preprocess_line(x)
    # Split into words and create (word, 1) pairs
    words = processed.split()
    return [(word, 1) for word in words if word]


def mapper(sequence):
    """Mapper"""
    # Apply map_line to each line and flatten the results
    result = []
    for line in sequence:
        result.extend(map_line(line))
    return result


def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    # Sort by key (word) to group same words together
    return sorted(sequence, key=lambda x: x[0])


def compute_sum_by_group(group):
    """Compute sum for a group of (word, count) pairs"""
    word = group[0]
    counts = [item[1] for item in group[1]]
    return (word, sum(counts))


def reducer(sequence):
    """Reducer"""
    # Group by word and sum the counts
    grouped = groupby(sequence, key=lambda x: x[0])
    result = []
    for word, group in grouped:
        group_list = list(group)
        total_count = sum(item[1] for item in group_list)
        result.append((word, total_count))
    return result


def create_directory(directory):
    """Create Output Directory"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_output(output_directory, sequence):
    """Save Output"""
    output_file = os.path.join(output_directory, "part-00000")
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, count in sequence:
            f.write(f"{word}\t{count}\n")


def create_marker(output_directory):
    """Create Marker"""
    marker_file = os.path.join(output_directory, "_SUCCESS")
    with open(marker_file, 'w', encoding='utf-8') as f:
        f.write("")


def run_job(input_directory, output_directory):
    """Job"""
    sequence = load_input(input_directory)
    sequence = mapper(sequence)
    sequence = shuffle_and_sort(sequence)
    sequence = reducer(sequence)
    create_directory(output_directory)
    save_output(output_directory, sequence)
    create_marker(output_directory)


if __name__ == "__main__":

    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(
        "files/input",
        "files/output",
    )

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")
