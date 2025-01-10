import openai
import json
from openai import AsyncOpenAI, OpenAI
import os

# Evaluate each pair of transcripts and save results to text files
def evaluate_transcript_batch(transcripts_a, transcripts_b, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for i, (transcript_a, transcript_b) in enumerate(zip(transcripts_a, transcripts_b)):
        result = evaluate_with_llm_judge(transcript_a, transcript_b)
        file_path = os.path.join(output_folder, f"evaluation_result_{i+1}.txt")
        with open(file_path, "w") as file:
            file.write(result)
        print(f"Evaluation {i+1} completed and saved to {file_path}")
        

def evaluate_with_llm_judge(transcript_a, transcript_b):
    """
    Evaluates two transcripts using gpt-4o-mini, comparing readability, level of detail, and conciseness.

    Args:
        transcript_a (str): The human-written reference transcript.
        transcript_b (str): The STT-generated transcript written from the audio.

    Returns:
        dict: A dictionary with gpt-4o-mini's evaluation.
    """
    # Insert the OpenAI API Key
    # NOTE: Don't leave this laying around... please use the env variable
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("The OPENAI_API_KEY environment variable is not set.")
    
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
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            { "role": "developer", "content": "You are a helpful assistant."},
            { "role": "user", "content": prompt },
        ],
    )

    # Extract the response from gpt-4o-mini, then return the evaluation result
    evaluation = response.choices[0].message
    return f"evaluation: {evaluation}"


# Evaluate each pair of transcripts and save results to text files
def evaluate_transcript_batch_with_meta_prompting(transcripts_a, transcripts_b, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for i, (transcript_a, transcript_b) in enumerate(zip(transcripts_a, transcripts_b)):
        result = evaluate_with_meta_prompting(transcript_a, transcript_b)
        file_path = os.path.join(output_folder, f"evaluation_result_{i+1}.txt")
        with open(file_path, "w") as file:
            file.write(result)
        print(f"Evaluation {i+1} completed and saved to {file_path}")


def evaluate_with_meta_prompting(transcript_a, transcript_b):
    """
    Evaluates two transcripts using meta-prompting with gpt-4o-mini and o1 models.
    Transcript comparison considers readability, level of detail, and conciseness.

    Args:
        transcript_a (str): The human-written reference transcript.
        transcript_b (str): The STT-generated transcript written from the audio.

    Returns:
        dict: A detailed evaluation with feedback from both models.
    """

    # Insert the OpenAI API Key
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("The OPENAI_API_KEY environment variable is not set.")
    
    # Step 1: Use o1 to refine the evaluation prompt
    meta_prompt = (
        "You are a meta-evaluator assistant tasked with refining a prompt for transcript comparison. "
        "Given two transcripts, we aim to compare them on Readability, Level of Detail, and Conciseness. "
        "Rank Readability, Level of Detail, and Conciseness using a Likert scale from 1 to 5. (X/5)"
        "Provide the total score of each transcript out of 15 points. (X/15)"
        "Consider ways to ensure the comparison is unbiased and clearly identifies the strengths of each transcript. "
        "Provide a concise, improved evaluation prompt tailored for gpt-4o-mini."
    )
    
    client = OpenAI()
    meta_response = client.chat.completions.create(
        model="o1-mini-2024-09-12",
        messages=[
            {"role": "user", "content": meta_prompt},
        ],
    )
    refined_prompt = meta_response.choices[0].message

    # Step 2: Use gpt-4o-mini for evaluation
    evaluation_prompt = (
        f"{refined_prompt}\n\n"
        "---\n"
        "Transcript A:\n"
        f"{transcript_a}\n\n"
        "Transcript B:\n"
        f"{transcript_b}\n\n"
        "Provide a detailed evaluation for each criterion and select which transcript is better overall. "
        "If they are equally good, specify that."
    )
    gpt4o_response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a language model tasked with transcript evaluation."},
            {"role": "user", "content": evaluation_prompt},
        ],
    )
    
    # Step 3: Extract and return evaluation results
    evaluation = gpt4o_response.choices[0].message
    return str({
        "meta_refinement": refined_prompt,
        "evaluation": evaluation
    })
    

# Easily load lines from a file
def load_lines_from_file(filepath):
    lines = []
    with open(filepath, "r") as file:
        for line in file:
            stripped_line = line.strip()
            lines.append(stripped_line)
    return lines
