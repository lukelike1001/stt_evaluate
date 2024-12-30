import openai
import os

def evaluate_transcripts_with_llm_judge(transcript_a, transcript_b):
    """
    Evaluates two transcripts using gpt-4o-mini, comparing readability, level of detail, and conciseness.

    Args:
        transcript_a (str): The human-written reference transcript.
        transcript_b (str): The STT-generated transcript written from the audio.

    Returns:
        dict: A dictionary with gpt-4o-mini's evaluation.
    """
    # Insert the OpenAI API Key
    # NOTE: Don't leave this laying around...
    openai.api_key = ""

    # Tell gpt-4o-mini to compare the two transcripts and output the better one.
    # To reduce bias, we don't tell which one was written by a human or a STT model.
    # Consequently, we use "Transcript A" and "Transcript B" instead.
    prompt = (
        "You are a language model tasked with evaluating two transcripts. Compare them based on the following criteria, using a Likert scale ranging from 1 (lowest) to 5 (highest): "
        "1. Readability: How easy is it to read and understand? "
        "2. Level of Detail: How well do they capture key points and nuances? "
        "3. Conciseness: Are they clear and to the point without unnecessary verbosity?\n\n"
        "---\n"
        "Transcript A:\n"
        f"{transcript_a}\n\n"
        "Transcript B:\n"
        f"{transcript_b}\n\n"
        "Provide a detailed evaluation for each criterion and select which transcript is better overall. If they are equally good, specify that."
    )

    # Call gpt-4o-mini model to find the "better" transcript
    # When the code was first written, gpt-4o-mini-2024-07-18 was the latest version of gpt-4o-mini available
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    # Extract the response from gpt-4o-mini, then return the evaluation result
    evaluation = response['choices'][0]['message']['content']
    return {
        "evaluation": evaluation
    }

# Example arrays of transcripts
transcripts_a = [
    "This is an example of a well-written transcript with clear points and structure.",
    "Here is another example of a structured and detailed transcript."
]
transcripts_b = [
    "this is an example of a stt generated transcript with some errors and less structure",
    "another stt example with some inconsistencies and lack of details"
]

# Folder to save results
output_folder = "evaluations"
os.makedirs(output_folder, exist_ok=True)

# Evaluate each pair of transcripts and save results to text files
for i, (transcript_a, transcript_b) in enumerate(zip(transcripts_a, transcripts_b)):
    result = evaluate_transcripts_with_llm_judge(transcript_a, transcript_b)
    file_path = os.path.join(output_folder, f"evaluation_result_{i+1}.txt")
    with open(file_path, "w") as file:
        file.write(result)
    print(f"Evaluation {i+1} completed and saved to {file_path}")
