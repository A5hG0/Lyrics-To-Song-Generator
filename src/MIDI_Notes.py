import os
import json
import numpy as np
import librosa

output_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features"
audio_dir = "Z:\Robotics_Club\DL_MAJOR\Vocals\Done"

for audio in os.listdir(audio_dir):     #for iterating over the folder
    if audio.endswith(".wav"):          #Only considering the wav files
        try:
            utt_id = audio.replace(".wav","")      #Just give the audio file name
            f0 = np.load(os.path.join(output_dir,f"{utt_id}_f0.npy"))    #Here we are loading the F0 contours that we generated earlier
            with open(os.path.join(output_dir,f"{utt_id}_phonemes.json"),"r") as f:
                phonemes = json.load(f)
            #Now phonemes basically is dict data type and now we can do phonemes[starttime] and we get starttime, etc...
            
            notes = []
            note_duration = []
            for phoneme,start,end in phonemes:
                #44100 --- Sampling rate        512    ---- hop length
                frame_start = int(start * 44100 / 512)
                frame_end = int(end * 44100 / 512)
                segment_f0 = f0[frame_start : frame_end]          #Slicing the from start to end and storing the f0
                voiced_f0 = segment_f0[segment_f0 > 0]         #Basically returns a bool value
                midi_note = 0
                if len(voiced_f0) > 0:
                    avg_f0 = np.mean(voiced_f0)
                    midi_note = int(round(librosa.hz_to_midi(avg_f0))) if avg_f0 > 0 else 0
                notes.append(midi_note)
                note_duration.append(end - start)
            note_data = [(p[0],n,d) for p,n,d in zip(phonemes, notes, note_duration)]
            with open(os.path.join(output_dir,f"{utt_id}_notes.json"),"w") as f :
                json.dump(note_data, f)
            print(f"Generated notes for {utt_id}")
        except Exception as e:
            print(f"{e}")

print("Done")