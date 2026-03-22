import os
import glob
import shutil

PARENT_DIR = r"Z:\Robotics_Club\DL_MAJOR\PJS_corpus_ver1.1"      # change this
DEST_DIR   = r"Z:\Robotics_Club\DL_MAJOR\PJS_corpus_ver1.1\dataset\wavs"         # change this

# If True: copied wav will be renamed as <foldername>.wav
RENAME_USING_FOLDER = True

os.makedirs(DEST_DIR, exist_ok=True)

folders = [f for f in os.listdir(PARENT_DIR) if os.path.isdir(os.path.join(PARENT_DIR, f))]

copied = 0
skipped = 0

for folder in folders:
    folder_path = os.path.join(PARENT_DIR, folder)

    # find wav(s) in this folder
    wav_files = glob.glob(os.path.join(folder_path, "*.wav"))

    if len(wav_files) == 0:
        print(f"⚠️ No wav found in: {folder_path}")
        skipped += 1
        continue

    # if multiple wav files exist, pick the first one
    wav_path = wav_files[0]

    if RENAME_USING_FOLDER:
        out_name = folder + ".wav"
    else:
        out_name = os.path.basename(wav_path)

    dest_path = os.path.join(DEST_DIR, out_name)

    # copy wav
    shutil.copy2(wav_path, dest_path)
    copied += 1

print("\n✅ Done!")
print("Copied:", copied)
print("Skipped:", skipped)
print("Output folder:", DEST_DIR)
