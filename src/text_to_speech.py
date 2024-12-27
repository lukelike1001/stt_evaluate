from openai import OpenAI
from pydub import AudioSegment
import torchaudio
import os

# Remember to not leave this in the open.
os.environ["OPENAI_API_KEY"] = ""

# This helper function generates an audio file given an input model, voice, and an input sentence.
# Here, I save the output as a .wav file for lossless audio
def text_to_speech(model="tts-1", voice="alloy", input="Hello World!", filename="output"):
    
    # OpenAI's TTS model generates audio at 24 kHz
    # Our SST model demands 16 kHz audio for its input.
    temp_filename = f"{filename}_24kHz.mp3"
    
    # Generate the audio stream into a temporary file
    client = OpenAI()
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=input,
    )

    # Write the streamed content to a temporary file
    with open(temp_filename, "wb") as file:
        for chunk in response.iter_bytes():  # Stream the response content in chunks
            file.write(chunk)
            
    # Convert the file into a .wav file for the SST model.
    mp3_audio = AudioSegment.from_file(temp_filename, format="mp3")
    wav_filename = f"{filename}_24kHz.wav"
    mp3_audio.export(wav_filename, format="wav")

    # Resample the audio to 16 kHz as requested
    waveform, sample_rate = torchaudio.load(wav_filename)
    target_sample_rate = 16000
    if sample_rate != target_sample_rate:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sample_rate)(waveform)
    torchaudio.save(f"{filename}.wav", waveform, target_sample_rate)

    # Remove the temporary file
    os.remove(temp_filename)

"""

Each message is designed to evaluate a speech-to-text (STT) model's performance on the following:
audio_0 = Homopohones and Contractions
audio_1 = Numbers and Contextual Meaning
audio_2 = Proper Nouns and Unusual Phrasing
audio_3 = Ambiguous Word Boundaries
audio_4 = Quotations and Special Characters
audio_5 = Accent and Colloquial Speech

"""
if __name__ == "__main__":
    
    # Generate the messages
    msg = ["" for i in range(13)]
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

    msg[12] = """
    Sample transcript for F2T2TEA:
    We have four enemy units to figure out F2T2s for. The expected TTG is going to be comprised of Su-35s, J-11s, and possibly JH-7s. VAQ-135, what do you have for that?
    We have three EA-18Gs we can use for F2.
    Great, then we'll put the EA-18Gs on Find and Fix for the Su-35s, and the E-7As in 2 SQN RAAF for the J-11s.
    The VAQ-141 can find the JH-7s if VAW-125 can then get a fix on them.
    VAW-125 can fix and track the JH-7s. 
    Still need someone to track the J-11s.
    7FS can do that.
    Okay, what kind of firepower do we need for the TTG? 
    The F-22As and F-35As both have enough.
    VFA-147, you'll target and engage the SU-35s with your F-35s. Can you assess?
    We can assess after we take them out, yes.
    Okay, 7FS will target and engage the J-11s and JH-7s—can the F-22As assess?
    No, we'll need someone else to do that.
    What kind of visual range do the B-1Bs have? Enough to see a wreckage on the water?
    Yeah, that should be fine.
    Okay, then 34BS will do assessment for the J-11s and JH-7s. 
    Who is going to handle the CH-SA-21?
    VFA-147 can take the CH-SA-21 with the F-35s, and CVW-5 can do the F2T.
    """

    # Generate the .wav files
    voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    for i in range(1):
        text_to_speech(voice=voices[i%6], input=msg[i], filename=f"audio_{i}")
