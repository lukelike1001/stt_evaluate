import difflib
import gradio as gr
from jiwer import wer

def highlight_differences(reference, transcription):
    """Highlight word-level differences using difflib."""
    diff = difflib.ndiff(reference.split(), transcription.split())
    highlighted = []
    
    for word in diff:
        if word.startswith("+ "):  # Insertions
            highlighted.append(f"<span style='color: green; font-weight: bold;'>{word[2:]}</span>")
        elif word.startswith("- "):  # Deletions
            highlighted.append(f"<span style='color: red; text-decoration: line-through;'>{word[2:]}</span>")
        elif word.startswith("? "):  # Metadata (ignorable in simple diffs)
            continue
        else:  # Matches and substitutions
            highlighted.append(word[2:])
    
    return " ".join(highlighted)

def compare_and_calculate(reference, transcription):
    """Generate a visual representation of differences and calculate WER."""
    highlighted = highlight_differences(reference, transcription)
    error_rate = wer(reference, transcription) * 100  # Convert to percentage
    return highlighted, f"{error_rate:.2f}%"

# Example sentences
examples = [
    ["It's difficult to say whether its impact will last long-term. They're considering their options carefully, but we can't be sure. The sight of the site left everyone in awe, though, and we know it's memorable.", "It's difficult to say whether its impact will last long term. They're considering their options carefully, but we can't be sure. The sight of the site left everyone in awe, though, and we know it's memorable."],
    ["Out of 250 participants, only 42 completed the survey within 48 hours. Imagine earning $3,000, but spending $2,750 on essentials. After 90 days, you'll have less than $300 if your daily expenses are $15.", "Out of 250 participants, only 42 completed the survey within 48 hours. Imagine earning $3,000, but spending $2,750 on essentials. After 90 days, you'll have less than $300 if your daily expenses are $15."],
    ["Dr. Adams's talk on the Adams apple in relation to Adams Peak in Sri Lanka was fascinating. Meanwhile, Sophia's thesis discussed Plato's Academy near the Acropolis. Both ideas were presented at Stanford's seminar.", "Dr. Adams's talk on the Adams' Apple in relation to Adams' peak in Sri Lanka was fascinating. Meanwhile, Sophia's thesis discussed Plato's academy near the Acropolis. Both ideas were presented at Stanford's seminar."],
    ["I scream, you scream, we all scream for ice cream. If you think I saw a bear, you might misunderstand—I saw a bare rock near the stream. The answer depends entirely on the way you phrase it.", "I scream, you scream, we all scream for ice cream. If you think I saw a bear, you might misunderstand. I saw a bear rock near the stream. The answer depends entirely on the way you phrase it."],
    ["The manager said, 'Budget cuts are unavoidable,' but added, 'We'll prioritize customer satisfaction.' He emphasized, 'Our profit goal is $1.5 million.' Still, the feedback forms read, 'This change feels rushed.'", "The manager said budget cuts are unavoidable but added will prioritize customer satisfaction. He emphasized our profit goal is $1.5 million. Still, the feedback forms read, this change feels rushed."],
    ["Y'all aren't gonna believe what happened! That doggone tractor jus' up and broke down again. Folks keep askin', 'Why don'tcha get a new one?' Well, lemme tell ya, fixin' it's cheaper than buyin'.", "Y'all aren't gonna believe what happened. That doggone tractor just up and broke down again. Folks keep asking, why don't you get a new one? Well, let me tell ya, fixin', it's cheaper than buyin'."],
    ["Maintain FL250, two-five-zero, and RTB by 1930 Zulu. ISR confirms ten-zero enemy movement at grid 43N753E. Engage only with PID and confirm BDA within two-four-hour cycles. ATO specifies 4 CAS sorties for TOT at 1200 Zulu, not fourteen hundred.", "Maintain fl-250-250 and rtb by 1930 Zulu. Isr confirms 10-0 enemy movement at grid 43n73e. Engage only with pid and confirm bda within 2-4-hour cycles. Ato specifies 4 cs sorties for 1200 Zulu, not 1400."],
    ["'ISR assets confirm target at 35°15'N, 45°30'E,' said the JTAC. 'CAS is cleared hot,' added the AWACS. Pilots, remember: key your radios with the codeword 'Raven.' ECM will jam at 1700 Zulu; adjust ingress timing to meet TOT at 1725.", "ISR assets confirm target at 35-15 N, 45-30 E, said the JTAC. \"CAS is cleared hot,\" added the AWACS. Pilots remember: \"Key your radios with the code word Raven. ECM will jam at 1700 Zulu, a just ingress timing to meet TOT at 1725."]
]

# Create Gradio interface
iface = gr.Interface(
    fn=compare_and_calculate,
    inputs=[
        gr.Textbox(lines=5, placeholder="Enter the reference transcript here"),
        gr.Textbox(lines=5, placeholder="Enter the STT transcription here"),
    ],
    outputs=[
        gr.HTML(label="Highlighted Differences"),
        gr.Textbox(label="Word Error Rate (WER%)"),
    ],
    examples=examples,
    title="Speech-to-Text (STT) Model Transcript Evaluation",
    description=(
        "This tool highlights differences between the reference transcript and the STT model transcription. "
        "Insertions are green, deletions are red (strikethrough), and substitutions are yellow. "
        "It also calculates the Word Error Rate (WER) percentage as the evaluation metric."
    ),
)

# Launch the app
iface.launch()
