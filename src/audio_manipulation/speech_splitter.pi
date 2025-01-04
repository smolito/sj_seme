from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, Wav2Vec2CTCTokenizer, Wav2Vec2FeatureExtractor
import torch
import librosa
import soundfile as sf
import os

# STABLE wav2vec2 base: facebook/wav2vec2-base-960h
# multilingual: facebook/wav2vec2-large-xlsr-53

class SpeechSplitter():
    def __init__(self, model_name="facebook/wav2vec2-base-960h", target_sr=16000):
        self.tokenizer = Wav2Vec2CTCTokenizer.from_pretrained(model_name)
        self.processor = Wav2Vec2Processor(feature_extractor=Wav2Vec2FeatureExtractor.from_pretrained(model_name), tokenizer=self.tokenizer)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)
        self.target_sr = target_sr

    """
    Splits the audio file into individual word segments and saves them to "example/[sound_file_name]"

    Parameters:
    ----------
    file_path : str
        path to the audio file to be split

    Returns:
    -------
    list of dict
        a list of dictionaries containing word information - word transcription, start time, end time, and file path
    """
    def split2words(self, file_path):
        speech, sr = librosa.load(file_path, sr=None)
        
        # if fs isn't 16k Hz resample
        if sr != self.target_sr:
            speech = librosa.resample(speech, orig_sr=sr, target_sr=self.target_sr)
            sr = self.target_sr
        
        print(len(speech))

        input_values = self.processor(speech, return_tensors="pt", padding="longest").input_values

        with torch.no_grad():
            logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]

        word_timestamps = self.processor.tokenizer.decode(predicted_ids[0], output_word_offsets=True)

        # adjust timestamps to match audio duration
        total_duration_s = len(speech) / sr
        word_offsets = word_timestamps["word_offsets"]
        for i in range(len(word_offsets)):
            word_offsets[i]["start_offset"] = (word_offsets[i]["start_offset"] / word_offsets[-1]["end_offset"]) * total_duration_s
            word_offsets[i]["end_offset"] = (word_offsets[i]["end_offset"] / word_offsets[-1]["end_offset"]) * total_duration_s

        output_dir = os.path.join("example", os.path.splitext(os.path.basename(file_path))[0])
        os.makedirs(output_dir, exist_ok=True)

        padding_ms = 0.05  # for better sounding words
        word_info_list = []

        for i, word_info in enumerate(word_timestamps["word_offsets"]):
            start_time = word_info["start_offset"] - padding_ms
            end_time = word_info["end_offset"] + padding_ms
            word = word_info["word"]
            # print(f"Word {i + 1}: {word} - start: {round(start_time, 6)} s, end: {round(end_time, 6)} s")

            # handle padding at edges
            start_time = max(0, start_time)
            end_time = min(total_duration_s, end_time)

            segment = speech[int(start_time * sr):int(end_time * sr)]

            sf.write(os.path.join(output_dir, f"{i}_{word}.wav"), segment, sr)

            word_info_list.append({
                "word": word,
                "start_time": round(start_time, 6),
                "end_time": round(end_time, 6),
                "file_path": os.path.join(output_dir, f"{i}_{word}.wav")
            })

        return word_info_list