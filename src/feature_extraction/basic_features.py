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
import numpy as np #used for visualizing features

def visualize_feature(data, feature_name="creature feature") -> None:
    plt.figure(figsize=(10, 6))
    if isinstance(data, np.ndarray) and data.ndim == 2:
        plt.imshow(data, aspect='auto', origin='lower', cmap='viridis')
        plt.colorbar(label="Intensity")
        plt.title(f"{feature_name} Visualization")
        plt.xlabel("Time")
        plt.ylabel("Frequency")
    elif isinstance(data, (list, np.ndarray)) and np.ndim(data) == 1:
        plt.plot(data)
        plt.title(f"{feature_name} Visualization")
        plt.xlabel("Time")
        plt.ylabel("Value")
    else:
        print(f"Cannot visualize feature: Unsupported data type {type(data)}", file=sys.stderr)
        return
    plt.show()

def get_file_metadata() -> None:
    stats = os.stat(filepath)
        
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

def get_file_size() -> None:
    pass

def get_file_volume(file) -> int:
    pass

def get_file_volume_over_time(file) -> int:
    pass
