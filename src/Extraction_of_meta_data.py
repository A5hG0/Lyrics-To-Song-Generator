import torchaudio as ta    #Used for generating mel-Spectrogram
import librosa             #Used for F0 Contours
import numpy as np         #Saving the file in npy format
import os                  #Navigating through OS
import torch

input_dir = "Z:\Robotics_Club\DL_MAJOR\Vocals\Done"
ouput_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features"
os.makedirs(ouput_dir,exist_ok=True)

for audiofile in os.listdir(input_dir):  #Traversing the audio files
    if audiofile.endswith(".wav"):
        try:
            #Prerequisites
            utt_id = audiofile.replace(".wav","")  #Just for getting the name of the file
            audio_path = os.path.join(input_dir,audiofile)  #combines input directory with audio file in it
            
            #Extracting data
            waveform, sample_rate = ta.load(audio_path)
            if sample_rate != 44100:
                waveform = ta.transforms.Resample(sample_rate, 44100)(waveform)  #If not available in hires, just typecast it
            mel_transform = ta.transforms.MelSpectrogram(sample_rate=44100, n_fft=2048, hop_length=512, n_mels=80) #Creating mel spectorgam
            mel_spec = torch.log(mel_transform(waveform) + 1e-9)
            np.save(os.path.join(ouput_dir,f"{utt_id}_mel.npy"),mel_spec.numpy())
            #Saving it using numpy!
            
            audio, sr = librosa.load(audio_path, sr = 44100)
            f0, _ , _ = librosa.pyin(audio, fmin = librosa.note_to_hz('C2'), fmax= librosa.note_to_hz('C7'),sr = sr, frame_length= 2048, hop_length= 512)
            f0 = np.nan_to_num(f0)
            np.save(os.path.join(ouput_dir,f"{utt_id}_f0.npy"), f0)
            print("Processed the file : ", utt_id)
        except Exception as e:
            print(e)