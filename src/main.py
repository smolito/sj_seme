# import feature extractors
import acoustic_features

# import argparse for parsing input args 
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Audio feature extraction using Parselmouth")
    parser.add_argument('-f', '--file', required=True, help="Path to the audio file")
    parser.add_argument('-t', '--task', required=True, choices=[
        "duration", "mean_pitch", "pitch_stddev", "hnr", "jitter", "shimmer"
    ], help="Feature extraction task to perform")
    args = parser.parse_args()

    try:
        sound = acoustic_features.get_sound(args.file)
    except Exception as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.task == "duration":
            result = acoustic_features.get_duration(sound)
            print(f"Duration: {result} seconds")

        elif args.task == "mean_pitch":
            pitch = acoustic_features.get_pitch(sound)
            result = acoustic_features.get_mean_pitch(pitch)
            print(f"Mean pitch: {result} Hz")

        elif args.task == "pitch_stddev":
            pitch = acoustic_features.get_pitch(sound)
            result = acoustic_features.get_pitch_stddev(pitch)
            print(f"Pitch standard deviation: {result} Hz")

        elif args.task == "hnr":
            result = acoustic_features.get_hnr(sound)
            print(f"Harmonics-to-Noise Ratio (HNR): {result}")

        elif args.task == "jitter":
            result = acoustic_features.get_jitter(sound)
            print(f"Jitter measures: {result}")

        elif args.task == "shimmer":
            result = acoustic_features.get_shimmer(sound)
            print(f"Shimmer measures: {result}")

    except Exception as e:
        print(f"Error processing task: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
