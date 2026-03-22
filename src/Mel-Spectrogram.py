import os
import numpy as np
import librosa
import json
import torchaudio


output_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features"
audio_dir = "Z:\Robotics_Club\DL_MAJOR\Vocals\Done"

for audio in os.listdir(output_dir):
    if audio.endswith(".wav"):
        try:
            utt_id = audio.replace(".wav","")
            audio_path = os.path.join(audio_dir,audio)
            
            #Load waveform
            waveform, sr = torchaudio.load(audio_path)
            if sr != 44100:
                waveform = torchaudio.transforms.Resample(sr, 44100)(waveform)
            
            #Compute the mel-spectrogram
            
        except Exception as e:
            print(f"{e}")