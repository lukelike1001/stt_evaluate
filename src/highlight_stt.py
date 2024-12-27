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
    ["Maintain FL250, two-five-zero, and RTB by 1930 Zulu. ISR confirms ten-zero enemy movement at grid 43N753E. Engage only with PID and confirm BDA within two-four-hour cycles. ATO specifies 4 CAS sorties for TOT at 1200 Zulu, not fourteen hundred.", "Maintain FL250-250 and RTB by 1930 Zulu. ISR confirms 10-0 enemy movement at Grid 43-N7-F3E. Engage only with PID and confirm BDA within two 4-hour cycles. ATO specifies four CS sorties for 1200 Zulu, not 1400."],
    ["maintain fl250 two five zero and rtb by 1930 zulu isr confirms ten zero enemy movement at grid 43n753e engage only with pid and confirm bda within two four hour cycles ato specifies 4 cas sorties for tot at 1200 zulu not fourteen hundred", "maintain fl250 250 and rtb by 1930 zulu isr confirms 10 0 enemy movement at grid 43 and 73e engage only with pid and confirm bda within two four hour cycles ato specifies four cs sorties for 1200 zulu not 1400"],
    ["'ISR assets confirm target at 35°15'N, 45°30'E,' said the JTAC. 'CAS is cleared hot,' added the AWACS. Pilots, remember: key your radios with the codeword 'Raven.' ECM will jam at 1700 Zulu; adjust ingress timing to meet TOT at 1725.", "ISR assets confirmed target at 35-2-15-N 45-30-E, said the JTAC. CAS is cleared hot, added the AWACUS. Pilots, remember, key your radios with the code word Raven. ECM will jam at 1700 Zulu, adjust ingress timing to meet TOT at 1725."],
    ["isr assets confirm target at 35 15 n 45 30 e said the jtac cas is cleared hot added the awacs pilots remember key your radios with the codeword raven ecm will jam at 1700 zulu adjust ingress timing to meet tot at 1725", "isr assets confirmed target at 35 2 15 n 45 30 e said the jtac cas is cleared hot added the awacs pilots remember key your radios with the code word raven ecm will jam at 1700 zulu adjust ingress timing to meet tot at 1725"],
    ["Sample transcript for F2T2TEA: We have four enemy units to figure out F2T2s for. The expected TTG is going to be comprised of Su-35s, J-11s, and possibly JH-7s. VAQ-135, what do you have for that? We have three EA-18Gs we can use for F2. Great, then we'll put the EA-18Gs on Find and Fix for the Su-35s, and the E-7As in 2 SQN RAAF for the J-11s. The VAQ-141 can find the JH-7s if VAW-125 can then get a", "Sample transcript, we have four enemy units to figure out F2-2s for. The expected TTG is going to be comprised of Su-35s, J11s, and possibly JH-7s. VACU-135, what do you have for that? We have three EA-18Gs we can use for F2. Great, then we'll put the EA-18Gs on Find and Fix for the Su-35s and the E7As in two SQN RAF for the J11s. The VACU-141 can find the JH-7s if VA-day 125 can then get a"],
    ["sample transcript for f2t2tea we have four enemy units to figure out f2t2s for the expected ttg is going to be comprised of su 35s j 11s and possibly jh 7s vaq 135 what do you have for that we have three ea 18gs we can use for f2 great then we ll put the ea 18gs on find and fix for the su 35s and the e 7as in 2 sqn raaf for the j 11s the vaq 141 can find the jh 7s if vaw 125 can then get a", "sample transcript we have four enemy units to figure out f2 2s 4 the expected ttg is going to be comprised of su 35s j 11s and possibly jh 7s vaq 135 what do you have for that we have three ea 18g s we can use for f2 great then we ll put the ea 18g s on find and fix for the su 35s and the e7a s in two sqn raf for the j 11s the vaq 141 can find the jh 7s if v"]
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
