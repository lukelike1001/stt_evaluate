import torchaudio
from torchaudio.functional import resample
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from jiwer import wer
from pathlib import Path
import einops

def evaluate_whisper_base(input_audio, input_reference):
    
    # Step 1: Load the audio file
    audio, sr = torchaudio.load(input_audio)

    # Step 2: Resample audio to 16kHz if needed
    if sr != 16000:
        audio = resample(audio, sr, 16000)
        print(f"Resampled audio to 16kHz")

    # Step 3: Load the model and processor
    model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-base.en")
    processor = AutoProcessor.from_pretrained("openai/whisper-base.en")

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
    
    # Access the current (src/make_transcripts) and parent (src/) directory via Pathlib
    curr_dir = Path(__file__).resolve().parent
    parent_dir = curr_dir.parent
    
    # Access the reference transcripts
    ref_path = parent_dir / "transcripts/reference_transcripts.txt"
    
    # Extract the reference sentences from the txt file
    reference_transcripts = []
    with open(ref_path, "r") as file:
        for line in file:
            stripped_line = line.strip()
            reference_transcripts.append(stripped_line)
    
    # Store the STT-generated transcripts into a txt file
    num_transcripts = len(reference_transcripts)
    stt_transcripts = ["" for i in range(num_transcripts)]
    
    # Iterate through all the transcripts
    for k in range(num_transcripts):
        input_path = parent_dir / f"audio/16kHz/audio_{k}.wav"
        curr_transcript, curr_wer = evaluate_whisper_base(input_audio=input_path, input_reference=reference_transcripts[k])
        stt_transcripts[k] = curr_transcript
    
    # Store the STT-generated transcripts into a TXT file
    output_path = parent_dir / "transcripts/whisper_base_transcripts.txt"
    with open(output_path, "w") as file:
        file.write("\n".join(stt_transcripts) + "\n")
