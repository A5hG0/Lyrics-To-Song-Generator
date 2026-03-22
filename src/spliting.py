import json
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pandas as pd

def load_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    # Filter valid entries: must have 3 elements, non-empty phoneme, and numeric times
    valid_entries = []
    for entry in data:
        if (len(entry) == 3 and 
            isinstance(entry[0], str) and entry[0].strip() and 
            isinstance(entry[1], (int, float)) and 
            isinstance(entry[2], (int, float)) and 
            entry[2] >= entry[1]):
            valid_entries.append(entry)
        else:
            if entry and len(entry) == 3:  # Log non-empty invalid entries
                print(f"Warning: Skipping invalid JSON entry in {json_path}: {entry}")
    return valid_entries

def remove_silence(audio, silence_thresh=-40, min_silence_len=500):
    # Split audio on silence and keep non-silent segments
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,  # Minimum silence length in ms
        silence_thresh=silence_thresh,    # Silence threshold in dB
        keep_silence=100                  # Keep 100ms of silence for natural transitions
    )
    # Concatenate non-silent chunks
    if not chunks:
        print("Warning: No non-silent audio detected. Using original audio.")
        return audio
    non_silent_audio = sum(chunks)
    return non_silent_audio

def slice_audio_by_phoneme_count(wav_path, json_path, output_dir, phonemes_per_chunk=4, silence_thresh=-40, min_silence_len=500):
    # Load audio and remove silence
    audio = AudioSegment.from_wav(wav_path)
    audio = remove_silence(audio, silence_thresh, min_silence_len)
    song_name = os.path.splitext(os.path.basename(wav_path))[0]
    
    # Load JSON data
    phonemes = load_json(json_path)
    if not phonemes:
        print(f"No valid phonemes found in {json_path}. Skipping.")
        return []
    
    print(f"Processing {song_name}: Found {len(phonemes)} valid phonemes.")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize lists for CSV
    csv_data = []
    
    # Group phonemes into chunks
    for chunk_index, i in enumerate(range(0, len(phonemes), phonemes_per_chunk)):
        chunk_phonemes = phonemes[i:i + phonemes_per_chunk]
        if not chunk_phonemes:
            break
        
        # Determine chunk audio boundaries
        chunk_start = chunk_phonemes[0][1] * 1000  # ph_starttime in ms
        chunk_end = chunk_phonemes[-1][2] * 1000  # ph_endtime in ms
        
        # Export audio chunk
        chunk = audio[max(0, chunk_start):chunk_end]
        chunk_filename = f"{song_name}_chunk_{chunk_index}.wav"
        chunk_path = os.path.join(output_dir, chunk_filename)
        chunk.export(chunk_path, format="wav")
        
        # Collect phoneme sequence and durations
        ph_seq = [ph[0] for ph in chunk_phonemes]  # ph_seq
        ph_dur = [round(ph[2] - ph[1], 3) for ph in chunk_phonemes]  # ph_endtime - ph_starttime
        
        # Verify lengths match
        if len(ph_seq) != len(ph_dur):
            print(f"Warning: Mismatch in {song_name}_chunk_{chunk_index}: "
                  f"ph_seq ({len(ph_seq)}) != ph_dur ({len(ph_dur)})")
            continue
        
        # Create CSV row
        csv_row = {
            'name': f"{song_name}_chunk_{chunk_index}",
            'ph_seq': ' '.join(ph_seq),
            'ph_dur': ' '.join(map(str, ph_dur))
        }
        csv_data.append(csv_row)
        print(f"Created chunk {song_name}_chunk_{chunk_index} with {len(ph_seq)} phonemes.")
    
    # Handle remaining phonemes (if any)
    remaining_phonemes = phonemes[len(csv_data) * phonemes_per_chunk:]
    if remaining_phonemes:
        chunk_index = len(csv_data)
        chunk_start = remaining_phonemes[0][1] * 1000
        chunk_end = remaining_phonemes[-1][2] * 1000
        
        chunk = audio[max(0, chunk_start):chunk_end]
        chunk_filename = f"{song_name}_chunk_{chunk_index}.wav"
        chunk_path = os.path.join(output_dir, chunk_filename)
        chunk.export(chunk_path, format="wav")
        
        ph_seq = [ph[0] for ph in remaining_phonemes]
        ph_dur = [round(ph[2] - ph[1], 3) for ph in remaining_phonemes]
        
        # Verify lengths match
        if len(ph_seq) != len(ph_dur):
            print(f"Warning: Mismatch in {song_name}_chunk_{chunk_index}: "
                  f"ph_seq ({len(ph_seq)}) != ph_dur ({len(ph_dur)})")
        else:
            csv_row = {
                'name': f"{song_name}_chunk_{chunk_index}",
                'ph_seq': ' '.join(ph_seq),
                'ph_dur': ' '.join(map(str, ph_dur))
            }
            csv_data.append(csv_row)
            print(f"Created chunk {song_name}_chunk_{chunk_index} with {len(ph_seq)} phonemes.")
    
    print(f"Total chunks created for {song_name}: {len(csv_data)}")
    return csv_data

def process_multiple_files(input_audio_dir, input_json_dir, output_audio_dir, output_csv, phonemes_per_chunk=4):
    # Ensure output directory exists
    os.makedirs(output_audio_dir, exist_ok=True)
    
    # Initialize list for all CSV data
    all_csv_data = []
    
    # Get list of WAV files
    wav_files = [f for f in os.listdir(input_audio_dir) if f.endswith('.wav')]
    
    for wav_file in wav_files:
        song_name = os.path.splitext(wav_file)[0]
        json_file = os.path.join(input_json_dir, f"{song_name}_phonemes.json")
        
        # Check if corresponding JSON file exists
        if not os.path.exists(json_file):
            print(f"Warning: JSON file not found for {wav_file}. Skipping.")
            continue
        
        wav_path = os.path.join(input_audio_dir, wav_file)
        print(f"Processing {wav_file}...")
        
        # Process the audio and JSON
        csv_data = slice_audio_by_phoneme_count(
            wav_path, 
            json_file, 
            output_dir=output_audio_dir, 
            phonemes_per_chunk=phonemes_per_chunk
        )
        all_csv_data.extend(csv_data)
    
    # Save all data to a single CSV
    if all_csv_data:
        df = pd.DataFrame(all_csv_data)
        df.to_csv(output_csv, index=False)
        print(f"CSV file generated: {output_csv}")
    else:
        print("No data processed. CSV file not generated.")

# Example usage
if __name__ == "__main__":
    input_audio_dir = r"Z:\Robotics_Club\DL_MAJOR\Vocals\wavs_original"
    input_json_dir = r"Z:\Robotics_Club\DL_MAJOR\dataset\Features\jsons"
    output_audio_dir = r"Z:\Robotics_Club\DL_MAJOR\Vocals\Done\wavs_new"
    output_csv = r"Z:\Robotics_Club\DL_MAJOR\Vocals\Done\Transcriptions_new.csv"
    phonemes_per_chunk = 10  # Number of phonemes per chunk
    
    process_multiple_files(input_audio_dir, input_json_dir, output_audio_dir, output_csv, phonemes_per_chunk)