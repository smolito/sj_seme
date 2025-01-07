# import feature extractors
import feature_extraction.acoustic_features as acoustic_features
import feature_extraction.basic_features as basic_features
import feature_extraction.features_over_time as features_over_time
import feature_extraction.spectral_features as spectral_features

# import basic audio manipulation 
import audio_manipulation.audio_parser as audio_parser
import audio_manipulation.simple_crop as simple_crop

# import speech splitting
from audio_manipulation.speech_splitter import SpeechSplitter

# import argparse for parsing input args 
import argparse
import sys

import numpy as np

def process_features(sound, tasks, visual, f_path):
    results = []
    for task in tasks:
        try:
            if task == "duration":
                result = acoustic_features.get_file_duration(sound)
                print(result)
            elif task == "mean_pitch":
                pitch = acoustic_features.get_file_pitch(sound)
                result = acoustic_features.get_file_mean_pitch(pitch)
                print(result)
            elif task == "pitch_stddev":
                pitch = acoustic_features.get_file_pitch(sound)
                result = acoustic_features.get_file_pitch_stddev(pitch)
                print(result)
            elif task == "hnr":
                result = acoustic_features.get_file_hnr(sound)
                print(result)
            elif task == "jitter":
                result = acoustic_features.get_file_jitter(sound)
                print(result)
            elif task == "shimmer":
                result = acoustic_features.get_file_shimmer(sound)
                print(result)
            elif task == "spectral_centroid":
                result = spectral_features.spectral_centroid(f_path)
                print(*result)
            elif task == "spectral_rolloff":
                result = spectral_features.spectral_rolloff(f_path)
                print(*result)
            elif task == "spectral_bandwidth":
                result = spectral_features.spectral_bandwidth(f_path)
                print(*result)
            elif task == "chromagram":
                result = spectral_features.chromagram(f_path)
                print(spectral_features.format(result))
            elif task == "mel_spectrogram":
                result = spectral_features.mel_spectrogram(f_path)
                print(spectral_features.format(result))
            elif task == "mfcc":
                result = spectral_features.mfcc(f_path)
                print(spectral_features.format(result))
            else:
                print(f"Unsupported task: {task}", file=sys.stderr)
                continue

            results.append(result)


        except Exception as e:
            print(f"Error processing task '{task}': {e}", file=sys.stderr)
    if visual and len(results) > 1:
        basic_features.visualize_feature(results)
    elif visual and len(results) == 1:
        basic_features.visualize_feature(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Audio processing and feature extraction")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    feature_parser = subparsers.add_parser("features", help="Extract audio features")
    feature_parser.add_argument('-f', '--file', required=True, help="Path to the audio file")
    feature_parser.add_argument("-v", "--visual", action="store_true", help="Visualize the spectrogram or feature.")
    feature_parser.add_argument('-t', '--task', nargs="+", required=True, choices=[
        "duration", "mean_pitch", "pitch_stddev", "hnr", "jitter", "shimmer", "spectral_centroid", "spectral_rolloff", "spectral_bandwidth", "chromagram", "mel_spectrogram", "mfcc"
    ], help="Feature extraction task to perform")

    speech_split_parser = subparsers.add_parser("speech_split", help="Split speech into words")
    speech_split_parser.add_argument("-f", "--file", required=True, help="Input audio file")

    crop_parser = subparsers.add_parser("crop", help="Crop audio file")
    crop_parser.add_argument("-f", "--file", required=True, help="Input audio file")
    crop_parser.add_argument("-o", "--output", required=True, help="Output audio file")
    crop_parser.add_argument("-s", "--start", type=float, required=True, help="Start time (in seconds)")
    crop_parser.add_argument("-e", "--end", type=float, required=True, help="End time (in seconds)")

    """
    numpy_to_audio_parser = subparsers.add_parser("numpy_to_audio", help="Save NumPy array to audio file")
    numpy_to_audio_parser.add_argument("-n", "--numpy", required=True, help="Path to NumPy array file")
    numpy_to_audio_parser.add_argument("-o", "--output", required=True, help="Output audio file")

    audio_to_numpy_parser = subparsers.add_parser("audio_to_numpy", help="Convert audio to NumPy array")
    audio_to_numpy_parser.add_argument("-f", "--file", required=True, help="Input audio file")
    audio_to_numpy_parser.add_argument("-o", "--output", required=False, help="Output NumPy array file")
    """


    args = parser.parse_args()

    if args.command == "features":
        try:
            sound = acoustic_features.get_file_sound(args.file)
        except Exception as e:
            print(f"Error loading file: {e}", file=sys.stderr)
            sys.exit(1)
        process_features(sound, args.task, args.visual, args.file)
    elif args.command == "crop":
        simple_crop.crop_audio(args.file, args.output, args.start, args.end)
    elif args.command == "split":
        speech_splitter = SpeechSplitter()
        words_info_list = speech_splitter.split2words("example/harvard.wav")
        for w in words_info_list:
            print(w)
        """
    elif args.command == "numpy_to_audio":
        array = np.load(args.numpy)
        audio_parser.save_arr_to_audio(array, args.output)
    elif args.command == "audio_to_numpy":
        array = audio_parser.audio_from_arr(args.file)
        np.save(args.output, array)
        print(f"NumPy array saved to {args.output}")
        """
    else:
        parser.print_help()
        sys.exit(1)

