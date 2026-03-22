import os
import glob
import csv

ROOT_DIR = r"Z:\Robotics_Club\DL_MAJOR\PJS_corpus_ver1.1"   # ✅ change this to your dataset root
OUT_CSV  = r"Z:\Robotics_Club\DL_MAJOR\PJS_corpus_ver1.1\metadata.csv"  # ✅ output file path

TIME_DIVISOR = 10_000_000  # HTK 100ns -> seconds


def parse_lab_file(lab_path):
    ph_list = []
    dur_list = []

    with open(lab_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 3:
                continue

            start = int(parts[0])
            end = int(parts[1])
            ph = parts[2].strip()

            dur = (end - start) / TIME_DIVISOR
            if dur <= 0:
                continue

            ph_list.append(ph)
            dur_list.append(dur)

    ph_seq = " ".join(ph_list)
    ph_dur = " ".join(f"{d:.4f}" for d in dur_list)

    return ph_seq, ph_dur


def build_csv(root_dir, out_csv):
    # ✅ recursive search for all .lab files in all folders
    lab_files = sorted(glob.glob(os.path.join(root_dir, "**", "*.lab"), recursive=True))

    if not lab_files:
        print("❌ No .lab files found inside:", root_dir)
        return

    with open(out_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "ph_seq", "ph_dur"])

        for lab_path in lab_files:
            # ✅ name = lab filename without extension
            name = os.path.splitext(os.path.basename(lab_path))[0]

            ph_seq, ph_dur = parse_lab_file(lab_path)

            if not ph_seq.strip() or not ph_dur.strip():
                print(f"⚠️ Skipping {name} (empty ph_seq/ph_dur)")
                continue

            if len(ph_seq.split()) != len(ph_dur.split()):
                print(f"⚠️ Skipping {name} mismatch: {len(ph_seq.split())} != {len(ph_dur.split())}")
                continue

            writer.writerow([name, ph_seq, ph_dur])

    print("✅ CSV created:", out_csv)
    print("✅ Total lab files found:", len(lab_files))


if __name__ == "__main__":
    build_csv(ROOT_DIR, OUT_CSV)