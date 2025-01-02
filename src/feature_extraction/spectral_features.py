"""
spectral features - untested
"""
import soundfile as sf

def load_audio(file_path):
    signal, sampling_rate = sf.read(file_path)
    return signal, sampling_rate

def spectral_centroid(file_path, frame_size=1024, hop_size=512):
    signal, sampling_rate = load_audio(file_path)
    centroids = []
    for start in range(0, len(signal) - frame_size, hop_size):
        frame = signal[start:start + frame_size]
        spectrum = np.abs(np.fft.rfft(frame))
        freqs = np.fft.rfftfreq(len(frame), 1 / sampling_rate)
        centroid = np.sum(freqs * spectrum) / np.sum(spectrum)
        centroids.append(centroid)
    return np.array(centroids)

def spectral_rolloff(file_path, rolloff_percentage=0.85, frame_size=1024, hop_size=512):
    signal, sampling_rate = load_audio(file_path)
    rolloffs = []
    for start in range(0, len(signal) - frame_size, hop_size):
        frame = signal[start:start + frame_size]
        spectrum = np.abs(np.fft.rfft(frame))
        cumulative_energy = np.cumsum(spectrum)
        threshold = rolloff_percentage * cumulative_energy[-1]
        rolloff_freq = np.argmax(cumulative_energy >= threshold)
        freqs = np.fft.rfftfreq(len(frame), 1 / sampling_rate)
        rolloffs.append(freqs[rolloff_freq])
    return np.array(rolloffs)

def spectral_bandwidth(file_path, frame_size=1024, hop_size=512):
    signal, sampling_rate = load_audio(file_path)
    bandwidths = []
    for start in range(0, len(signal) - frame_size, hop_size):
        frame = signal[start:start + frame_size]
        spectrum = np.abs(np.fft.rfft(frame))
        freqs = np.fft.rfftfreq(len(frame), 1 / sampling_rate)
        centroid = np.sum(freqs * spectrum) / np.sum(spectrum)
        bandwidth = np.sqrt(np.sum(((freqs - centroid) ** 2) * spectrum) / np.sum(spectrum))
        bandwidths.append(bandwidth)
    return np.array(bandwidths)

def chromagram(file_path, frame_size=2048, hop_size=1024):
    signal, sampling_rate = load_audio(file_path)
    chroma = []
    for start in range(0, len(signal) - frame_size, hop_size):
        frame = signal[start:start + frame_size]
        spectrum = np.abs(np.fft.rfft(frame))
        freqs = np.fft.rfftfreq(len(frame), 1 / sampling_rate)
        chroma_frame = np.zeros(12)
        for i, f in enumerate(freqs):
            if f > 0:
                pitch_class = int(round(12 * np.log2(f / 440.0) + 69) % 12)
                chroma_frame[pitch_class] += spectrum[i]
        chroma.append(chroma_frame)
    return np.array(chroma).T

def mel_spectrogram(file_path, n_mels=128, frame_size=2048, hop_size=1024):
    signal, sampling_rate = load_audio(file_path)
    mel_filter_bank = np.zeros((n_mels, frame_size // 2 + 1))
    mel_min = 0
    mel_max = 2595 * np.log10(1 + (sampling_rate / 2) / 700)
    mel_points = np.linspace(mel_min, mel_max, n_mels + 2)
    hz_points = 700 * (10 ** (mel_points / 2595) - 1)
    bin_points = np.floor((frame_size + 1) * hz_points / sampling_rate).astype(int)
    for i in range(1, n_mels + 1):
        mel_filter_bank[i - 1, bin_points[i - 1]:bin_points[i]] = np.linspace(0, 1, bin_points[i] - bin_points[i - 1])
        mel_filter_bank[i - 1, bin_points[i]:bin_points[i + 1]] = np.linspace(1, 0, bin_points[i + 1] - bin_points[i])
    mel_spectrogram = []
    for start in range(0, len(signal) - frame_size, hop_size):
        frame = signal[start:start + frame_size]
        spectrum = np.abs(np.fft.rfft(frame)) ** 2
        mel_frame = mel_filter_bank.dot(spectrum)
        mel_spectrogram.append(mel_frame)
    return np.array(mel_spectrogram).T

def mfcc(file_path, n_mfcc=13, n_mels=128, frame_size=2048, hop_size=1024):
    signal, sampling_rate = load_audio(file_path)
    mel_spec = mel_spectrogram(signal, sampling_rate, n_mels, frame_size, hop_size)
    log_mel_spec = np.log(mel_spec + 1e-9)
    mfccs = np.fft.dct(log_mel_spec, type=2, axis=0, norm='ortho')[:n_mfcc]
    return mfccs
