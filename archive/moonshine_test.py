from transformers import AutoModelForSpeechSeq2Seq, AutoConfig, PreTrainedTokenizerFast

import torchaudio
import sys

audio, sr = torchaudio.load(sys.argv[1])
if sr != 16000:
  audio = torchaudio.functional.resample(audio, sr, 16000)

model = AutoModelForSpeechSeq2Seq.from_pretrained('usefulsensors/moonshine-base', trust_remote_code=True)
tokenizer = PreTrainedTokenizerFast.from_pretrained('usefulsensors/moonshine-base')

tokens = model(audio)
print(tokenizer.decode(tokens[0], skip_special_tokens=True))
