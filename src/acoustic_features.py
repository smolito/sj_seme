'''
this is a script that wraps around parselmouth functions to get acoustic features such as pitch and HNR
'''

import parselmouth
from parselmouth.praat import call

def get_sound(file_path):
    return parselmouth.Sound(file_path)

def get_duration(sound):
    return call(sound, "Get total duration")

def get_pitch(sound, f0min=75, f0max=300):
    return call(sound, "To Pitch", 0.0, f0min, f0max)

def get_mean_pitch(pitch, unit="Hertz"):
    return call(pitch, "Get mean", 0, 0, unit)

def get_pitch_stddev(pitch, unit="Hertz"):
    return call(pitch, "Get standard deviation", 0, 0, unit)

def get_hnr(sound, f0min=75):
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0)
    return call(harmonicity, "Get mean", 0, 0)

def get_jitter(sound, f0min=75, f0max=300):
    point_process = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    local_jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    rap_jitter = call(point_process, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    return {"local_jitter": local_jitter, "rap_jitter": rap_jitter}

def get_shimmer(sound, f0min=75, f0max=300):
    point_process = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    local_shimmer = call([sound, point_process], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3_shimmer = call([sound, point_process], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    return {"local_shimmer": local_shimmer, "apq3_shimmer": apq3_shimmer}
