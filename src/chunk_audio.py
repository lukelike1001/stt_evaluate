import os
from pydub import AudioSegment

def split_audio_to_wav(file_path, output_dir, chunk_length=30):
    # Load the audio file
    audio = AudioSegment.from_file(file_path)
    chunk_length_ms = chunk_length * 1000  # Convert to milliseconds

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Split the audio into chunks
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    # Save each chunk as a .wav file
    base_name = os.path.splitext(os.path.basename(file_path))[0]  # Extract base name of the file
    for idx, chunk in enumerate(chunks):
        chunk_name = f"{base_name}_chunk{idx + 1}.wav"  # Name the chunk
        output_path = os.path.join(output_dir, chunk_name)
        chunk.export(output_path, format="wav")
        print(f"Saved: {output_path}")

    return len(chunks)  # Return the number of chunks created

if __name__ == "__main__":
    input_path = "crete_persia.wav"
    output_path = "chunk/"
    num_chunks = split_audio_to_wav(file_path=input_path, output_dir=output_path)