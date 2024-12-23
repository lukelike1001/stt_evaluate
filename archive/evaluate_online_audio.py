import requests
import torchaudio
from torchaudio.functional import resample
from transformers import AutoModelForSpeechSeq2Seq, PreTrainedTokenizerFast
from jiwer import wer

# Step 1: Download the audio file
audio_url = "https://www.example.com/sample_audio.wav"  # Replace with a valid URL
audio_file = "sample_audio.wav"

response = requests.get(audio_url)
if response.status_code == 200:
    with open(audio_file, "wb") as f:
        f.write(response.content)
    print(f"Downloaded audio file: {audio_file}")
else:
    print(f"Failed to download audio file: {response.status_code}")
    exit(1)

# Step 2: Load the audio file
audio, sr = torchaudio.load(audio_file)

# Step 3: Resample audio to 16kHz if needed
if sr != 16000:
    audio = resample(audio, sr, 16000)
    print(f"Resampled audio to 16kHz")

# Step 4: Load the model and tokenizer
model = AutoModelForSpeechSeq2Seq.from_pretrained("usefulsensors/moonshine-base", trust_remote_code=True)
tokenizer = PreTrainedTokenizerFast.from_pretrained("usefulsensors/moonshine-base")

# Step 5: Perform transcription
print("Transcribing audio...")
tokens = model(audio)
transcription = tokenizer.decode(tokens[0], skip_special_tokens=True)
print("Transcription:", transcription)

# Step 6: Load the reference transcript
reference_transcript = """
This is a placeholder for the reference transcript.
Replace this with the true text of the audio file.
"""  # Replace with actual reference text
reference_transcript = reference_transcript.strip()

# Step 7: Evaluate transcription accuracy
error_rate = wer(reference_transcript, transcription)
print(f"Word Error Rate (WER): {error_rate:.2%}")
