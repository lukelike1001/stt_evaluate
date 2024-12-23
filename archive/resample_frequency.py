import torchaudio

# Load the converted WAV file
waveform, sample_rate = torchaudio.load("aerial_acronyms.wav")

# Resample to 16 kHz if needed
target_sample_rate = 16000
if sample_rate != target_sample_rate:
    resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sample_rate)
    waveform = resampler(waveform)

# Save the resampled WAV file
torchaudio.save("audio_6.wav", waveform, target_sample_rate)
