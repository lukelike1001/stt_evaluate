from pathlib import Path
from jiwer import wer

# Easily load lines from a file
def load_lines_from_file(filepath):
    lines = []
    with open(filepath, "r") as file:
        for line in file:
            stripped_line = line.strip()
            lines.append(stripped_line)
    return lines
    
# Evaluate the WER% between a reference transcript and its STT variant
def evaluate_wer(ref_transcripts, stt_transcripts):
    
    # Verify that we have an equal number of both transcripts
    if len(ref_transcripts) != len(stt_transcripts):
        print("Mismatched number of transcripts")
        return
    
    # Keep track of the error rates over time
    # Rounded to 4 digits after the decimal point to make sure they aren't incredibly long.
    error_rates = ["" for _ in range(len(ref_transcripts))]
    for i, (ref_transcript, stt_transcript) in enumerate(zip(ref_transcripts, stt_transcripts)):
        error_rate = wer(ref_transcript, stt_transcript)
        error_rates[i] = round(error_rate, 4)
    return error_rates

if __name__ == "__main__":
    
    # Access the current (src/wer) and parent (src/) directory via Pathlib
    curr_dir = Path(__file__).resolve().parent
    parent_dir = curr_dir.parent
    
    # Access the reference transcripts
    ref_path = parent_dir / "transcripts/reference_transcripts.txt"
    
    # Then, access the STT transcriptions we'd like to evaluate
    whisper_base_path = parent_dir / "transcripts/whisper_base_transcripts.txt"
    whisper_tiny_path = parent_dir / "transcripts/whisper_tiny_transcripts.txt"
    moonshine_path = parent_dir / "transcripts/moonshine_transcripts.txt"
    
    # Load the lines from each path
    ref_transcripts = load_lines_from_file(ref_path)
    whisper_base_transcripts = load_lines_from_file(whisper_base_path)
    whisper_tiny_transcripts = load_lines_from_file(whisper_tiny_path)
    moonshine_transcripts = load_lines_from_file(moonshine_path)
    
    # Evaluate the WER between each transcript with one another
    whisper_base_error = evaluate_wer(ref_transcripts, whisper_base_transcripts)
    whisper_tiny_error = evaluate_wer(ref_transcripts, whisper_tiny_transcripts)
    moonshine_error = evaluate_wer(ref_transcripts, moonshine_transcripts)
    
    # Store the errors into a file
    whisper_base_str = f"whisper_base_error = {whisper_base_error}\n"
    whisper_tiny_str = f"whisper_tiny_error = {whisper_tiny_error}\n"
    moonshine_str = f"moonshine_error = {moonshine_error}\n"
    
    file_lines = [whisper_base_str, whisper_tiny_str, moonshine_str]
    output_path = parent_dir / "wer/wer_results.txt"
    with open(output_path, "w") as file:
        file.writelines(file_lines)
    