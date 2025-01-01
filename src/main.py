# import feature extractors
import feature_extraction.acoustic_features as acoustic_features
import feature_extraction.basic_features as basic_features
import feature_extraction.features_over_time as features_over_time

# import basic audio manipulation 
import audio_manipulation.audio_parser as audio_parser
import audio_manipulation.simple_crop as simple_crop

# import argparse for parsing input args 
import argparse
import sys

import numpy as np

def main():
    parser = argparse.ArgumentParser(description="Audio processing and feature extraction")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    feature_parser = subparsers.add_parser("features", help="Extract audio features")
    feature_parser.add_argument('-f', '--file', required=True, help="Path to the audio file")
    feature_parser.add_argument('-t', '--task', required=True, choices=[
        "duration", "mean_pitch", "pitch_stddev", "hnr", "jitter", "shimmer"
    ], help="Feature extraction task to perform")

    crop_parser = subparsers.add_parser("crop", help="Crop audio file")
    crop_parser.add_argument("-f", "--file", required=True, help="Input audio file")
    crop_parser.add_argument("-o", "--output", required=True, help="Output audio file")
    crop_parser.add_argument("-s", "--start", type=float, required=True, help="Start time (in seconds)")
    crop_parser.add_argument("-e", "--end", type=float, required=True, help="End time (in seconds)")

    numpy_to_audio_parser = subparsers.add_parser("numpy_to_audio", help="Save NumPy array to audio file")
    numpy_to_audio_parser.add_argument("-n", "--numpy", required=True, help="Path to NumPy array file")
    numpy_to_audio_parser.add_argument("-o", "--output", required=True, help="Output audio file")

    audio_to_numpy_parser = subparsers.add_parser("audio_to_numpy", help="Convert audio to NumPy array")
    audio_to_numpy_parser.add_argument("-f", "--file", required=True, help="Input audio file")
    audio_to_numpy_parser.add_argument("-o", "--output", required=True, help="Output NumPy array file")

    plot_parser = subparsers.add_parser("plot_features", help="Extract features for plotting")
    plot_parser.add_argument("-f", "--file", required=True, help="Input audio file")

    args = parser.parse_args()

    if args.command == "features":
        try:
            sound = acoustic_features.get_sound(args.file)
        except Exception as e:
            print(f"Error loading file: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            if args.task == "duration":
                result = acoustic_features.get_file_duration(sound)
                print(f"Duration: {result} seconds")

            elif args.task == "mean_pitch":
                pitch = acoustic_features.get_file_pitch(sound)
                result = acoustic_features.get_file_mean_pitch(pitch)
                print(f"Mean pitch: {result} Hz")

            elif args.task == "pitch_stddev":
                pitch = acoustic_features.get_file_pitch(sound)
                result = acoustic_features.get_file_pitch_stddev(pitch)
                print(f"Pitch standard deviation: {result} Hz")

            elif args.task == "hnr":
                result = acoustic_features.get_file_hnr(sound)
                print(f"Harmonics-to-Noise Ratio (HNR): {result}")

            elif args.task == "jitter":
                result = acoustic_features.get_file_jitter(sound)
                print(f"Jitter measures: {result}")

            elif args.task == "shimmer":
                result = acoustic_features.get_file_shimmer(sound)
                print(f"Shimmer measures: {result}")

        except Exception as e:
            print(f"Error processing task: {e}", file=sys.stderr)
            sys.exit
    elif args.command == "crop":
        simple_crop.crop_audio(args.file, args.output, args.start, args.end)
    elif args.command == "numpy_to_audio":
        array = np.load(args.numpy)
        audio_parser.save_arr_to_audio(array, args.output)
    elif args.command == "audio_to_numpy":
        array = audio_parser.audio_from_arr(args.file)
        np.save(args.output, array)
        print(f"NumPy array saved to {args.output}")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
