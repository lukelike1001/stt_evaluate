import torchaudio
from torchaudio.functional import resample
from transformers import AutoModelForSpeechSeq2Seq, PreTrainedTokenizerFast
from jiwer import wer
import einops

def evaluate_moonshine(input_audio="16kHz/audio_0.wav", input_reference=""):
    
    # Step 1: Load the audio file
    audio, sr = torchaudio.load(input_audio)

    # Step 2: Resample audio to 16kHz if needed
    if sr != 16000:
        audio = resample(audio, sr, 16000)
        print(f"Resampled audio to 16kHz")

    # Step 3: Load the model and tokenizer
    model = AutoModelForSpeechSeq2Seq.from_pretrained("usefulsensors/moonshine-base", trust_remote_code=True)
    tokenizer = PreTrainedTokenizerFast.from_pretrained("usefulsensors/moonshine-base")

    # Step 4: Perform transcription
    print("Transcribing audio...")
    tokens = model(audio)
    transcription = tokenizer.decode(tokens[0], skip_special_tokens=True)
    print("Transcription:", transcription)

    # Step 5: Load the reference transcript
    reference_transcript = input_reference.strip()

    # Step 6: Evaluate transcription accuracy
    error_rate = wer(reference_transcript, transcription)
    print(f"Word Error Rate (WER): {error_rate:.2%}")
    
    # Step 7: Return the STT transcript with the WER%
    return transcription, error_rate

if __name__ == "__main__":
    
    msg = ["" for i in range(12)]
    msg[0] = "It's difficult to say whether its impact will last long-term. They're considering their options carefully, but we can't be sure. The sight of the site left everyone in awe, though, and we know it's memorable."
    msg[1] = "Out of 250 participants, only 42 completed the survey within 48 hours. Imagine earning $3,000, but spending $2,750 on essentials. After 90 days, you'll have less than $300 if your daily expenses are $15."
    msg[2] = "Dr. Adams's talk on the Adams apple in relation to Adams Peak in Sri Lanka was fascinating. Meanwhile, Sophia's thesis discussed Plato's Academy near the Acropolis. Both ideas were presented at Stanford's seminar."
    msg[3] = "I scream, you scream, we all scream for ice cream. If you think I saw a bear, you might misunderstand—I saw a bare rock near the stream. The answer depends entirely on the way you phrase it."
    msg[4] = "The manager said, 'Budget cuts are unavoidable,' but added, 'We'll prioritize customer satisfaction.' He emphasized, 'Our profit goal is $1.5 million.' Still, the feedback forms read, 'This change feels rushed.'"
    msg[5] = "Y'all aren't gonna believe what happened! That doggone tractor jus' up and broke down again. Folks keep askin', 'Why don'tcha get a new one?' Well, lemme tell ya, fixin' it's cheaper than buyin'."
    
    msg[6] = "We're taking a different route to minimize ALR, ensuring RPA overwatch. They're checking their RWR and ECM systems to avoid triggering the IADS. It's critical that we don't expose the AO during ingress. We've ensured all FLOT markers are accurate and synced with GPS."
    msg[7] = "Maintain FL250, two-five-zero, and RTB by 1930 Zulu. ISR confirms ten-zero enemy movement at grid 43N753E. Engage only with PID and confirm BDA within two-four-hour cycles. ATO specifies 4 CAS sorties for TOT at 1200 Zulu, not fourteen hundred."
    msg[8] = "Colonel Maddox briefed on OP Thunderstrike, highlighting the E-8C JSTARS tracking MTIs near OBJ Falcon. Captain Hargrove noted terrain masking south of Mount Hesper may interfere with JTAC comms. Recalibrate IFF and TACAN if comms degrade."
    msg[9] = "The recon RPA identified an ice storm—or maybe it was a nice, stable AO. Either way, CAS should proceed under the ROE. If hostile troops are ID'd, submit a 9-line CAS request. ATO lists all assets cleared for CAS along the FLOT near OBJ Eagle."
    msg[10] = "'ISR assets confirm target at 35°15'N, 45°30'E,' said the JTAC. 'CAS is cleared hot,' added the AWACS. Pilots, remember: key your radios with the codeword 'Raven.' ECM will jam at 1700 Zulu; adjust ingress timing to meet TOT at 1725."
    msg[11] = "Alright, uh, y'all listen up. We've got a couple jets ready for CAS, so, uhhh, let's not waste time. ISR reports enemy near the FLOT, but, uh, the AO's clear for now. If you see anything, hit your comms and, uh, confirm with the JTAC before engaging, okay?"

    # Evaluate all of the inputs
    wer_array, wer_mean = [], 0
    for k in range(len(msg)):
        curr_transcript, curr_wer = evaluate_moonshine(input_audio=f"16kHz/audio_{k}.wav", input_reference=msg[k])
        wer_array.append(curr_wer)
        wer_mean += curr_wer
    
    # Print the wer array and the mean
    wer_mean /= len(msg)
    print(f"wer_array: {wer_array}")
    print(f"wer_mean: {wer_mean}")