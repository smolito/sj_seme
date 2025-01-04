"""
this script crops the audio file into a new audio segment based on the start and end times provided
"""
import parselmouth
import parselmouth.praat
import sys

def crop_audio(input_file, output_file, start_time, end_time):
    try:
        sound = parselmouth.Sound(input_file)
        cropped_sound = sound.extract_part(from_time=start_time, to_time=end_time, preserve_times=True)
        cropped_sound.save(output_file, "WAV")
        print(f"Audio cropped and saved to {output_file}")
    except Exception as e:
        print(f"Error cropping audio: {e}", file=sys.stderr)
        sys.exit(1)
