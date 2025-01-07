'''
this is a script that gets audio files basic features that may be used for further analysis:
- file metadata (user specifies which data to look for)
- file duration (seconds, minutes, hours, days)
- file size (bytes, kilobytes, megabytes, gigabytes)
'''

import os #used for os.stat()
import sys #used for file I/O
import soundfile as sf #used for audio length
import matplotlib.pyplot as plt #used for visualizing features
import matplotlib
import numpy as np #used for visualizing features

def visualize_feature(data) -> None:
    matplotlib.use('Qt5Agg')
    plt.figure(figsize=(6, 4))
    if isinstance(data, np.ndarray) and data.ndim == 2:
        plt.imshow(data, aspect='auto', origin='lower', cmap='viridis')
        plt.colorbar(label="Intensity")
        plt.xlabel("Time")
        plt.ylabel("Frequency")
    elif isinstance(data, (list, np.ndarray)) and np.ndim(data) == 1:
        plt.plot(data)
        plt.xlabel("Time")
        plt.ylabel("Amplitudey")
    elif isinstance(data, dict):
        plt.bar(*zip(*data.items()))
        plt.xlabel("x")
        plt.ylabel("y")
    elif isinstance(data, (int, float)):
        plt.bar(0, data)
        plt.xticks([0], [''])
        plt.ylabel("Value")
    else:
        print(f"Cannot visualize feature: Unsupported data type {type(data)}", file=sys.stderr)
        return
    plt.show()

def get_file_metadata(file) -> None:
    stats = os.stat(file)
        
    attrs = {
        'File Name': name,
        'Size (KB)': sizeFormat(stats.st_size),
        'Creation Date': timeConvert(stats.st_ctime),
        'Modified Date': timeConvert(stats.st_mtime),
        'Last Access Date': timeConvert(stats.st_atime),        
    }

def get_file_samples(file) -> int:
    f = sf.SoundFile(file)
    return f.frames

def get_file_sample_rate(file) -> int:
    f = sf.SoundFile(file)
    return f.samplerate

def get_file_duration(file) -> int:
    return get_file_samples(file)/get_file_sample_rate(file)

def get_file_size(file) -> None:
    os.stats.st_size(file)
