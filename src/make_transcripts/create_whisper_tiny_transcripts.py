import torchaudio
from torchaudio.functional import resample
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from jiwer import wer
import einops

def evaluate_whisper_tiny(input_audio, input_reference):
    
    # Step 1: Load the audio file
    audio, sr = torchaudio.load(input_audio)

    # Step 2: Resample audio to 16kHz if needed
    if sr != 16000:
        audio = resample(audio, sr, 16000)
        print(f"Resampled audio to 16kHz")

    # Step 3: Load the model and processor
    model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-tiny.en")
    processor = AutoProcessor.from_pretrained("openai/whisper-tiny.en")

    # Step 4: Preprocess the audio
    print("Preprocessing audio...")
    input_features = processor.feature_extractor(audio.squeeze().numpy(), sampling_rate=16000, return_tensors="pt").input_features

    # Step 5: Perform transcription
    print("Transcribing audio...")
    predicted_ids = model.generate(input_features)
    transcription = processor.tokenizer.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    print("Transcription:", transcription)

    # Step 6: Load the reference transcript
    reference_transcript = input_reference.strip()

    # Step 7: Evaluate transcription accuracy
    error_rate = wer(reference_transcript, transcription)
    print(f"Word Error Rate (WER): {error_rate:.2%}")
    
    # Step 8: Return the STT transcript with the WER%
    return transcription, error_rate

if __name__ == "__main__":
    
    # Extract the reference sentences from the txt file
    reference_transcripts = []
    with open("../transcripts/reference_transcripts.txt", "r") as file:
        for line in file:
            stripped_line = line.strip()
            reference_transcripts.append(stripped_line)
    
    # Store the STT-generated transcripts into a txt file
    num_transcripts = len(reference_transcripts)
    stt_transcripts = ["" for i in range(num_transcripts)]
    
    for k in range(num_transcripts):
        curr_transcript, curr_wer = evaluate_whisper_tiny(input_audio=f"../audio/16kHz/audio_{k}.wav", input_reference=reference_transcripts[k])
        stt_transcripts[k] = curr_transcript
    
    # Store the STT-generated transcripts into a TXT file
    with open("../transcripts/whisper_tiny_transcripts.txt", "w") as file:
        file.write("\n".join(stt_transcripts) + "\n")
