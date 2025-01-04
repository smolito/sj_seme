"""
this script allows user to create a audio file from a text file or to get values of a audio file
"""
import parselmouth
import sys

def audio_from_arr(array, sampling_frequency=44100.0, start_time=0.0):
    try:
        sound = parselmouth.Sound(array, sampling_frequency, start_time)
        return sound
    except Exception as e:
        print(f"Error creating Sound from NumPy array: {e}", file=sys.stderr)
        sys.exit(1)

def save_arr_to_audio(array, output_file, sampling_frequency=44100.0):
    try:
        sound = audio_from_arr(array, sampling_frequency)
        sound.save(output_file, "WAV")
        print(f"Audio saved to {output_file}")
    except Exception as e:
        print(f"Error saving NumPy array to audio file: {e}", file=sys.stderr)
        sys.exit(1)

def audio_to_arr(input_file):
    try:
        sound = parselmouth.Sound(input_file)
        return sound.values
    except Exception as e:
        print(f"Error converting audio to NumPy array: {e}", file=sys.stderr)
        sys.exit(1)
