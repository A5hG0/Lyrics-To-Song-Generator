# import sys
# print(sys.executable)
import textgrid
import os
import json

#Directories
textgrid_dir = "Z:\Robotics_Club\DL_MAJOR\mfa_output_new_v2"
output_dir = "Z:\Robotics_Club\DL_MAJOR\dataset\Features"

#Create the output directory
os.makedirs(output_dir,exist_ok=True)

#Parsing the textgrid files
for tgfile in os.listdir(textgrid_dir) :
    if tgfile.endswith(".TextGrid"):
        try:
            tgfile_path = os.path.join(textgrid_dir,tgfile)  #We get something like \mfa_output_new_v2\Starboy
            tg = textgrid.TextGrid.fromFile(tgfile_path)
            
            #Extract phoneme tiers
            phoneme_tier = next((tier for tier in tg if tier.name == 'phones'),None)
            if not phoneme_tier:
                print(f"There is no phonemes here")
                continue
            
            #Extract phonemes and timings
            phonemes = [(interval.mark,interval.minTime,interval.maxTime) for interval in phoneme_tier]
            #Where interval.text is 'AIE' , and xmin and xmax are time in seconds!
            #mark = text, minTime = xmin and maxTime = xmax in textgrid... It is inbuilt and parses in the library
            
            #Saving these values as JSON
            utt_id = tgfile.replace(".TextGrid","")  #Utterrance id
            with open(os.path.join(output_dir,f"{utt_id}_phonemes.json"),"w") as f:
                json.dump(phonemes,f)
        except Exception as e:
            print(f"Error Processing {tgfile} : {e}")