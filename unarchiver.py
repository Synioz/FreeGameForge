import os
import rarfile
import re
from tqdm import tqdm

def extract_part_number(filename):
    match = re.search(r'part(\d+)', filename, re.IGNORECASE)
    return int(match.group(1)) if match else float('inf')

def sort_files_by_part_number(file_list):
    return sorted(file_list, key=extract_part_number)

def sort_files_by_date(file_list, directory_path):
    file_list.sort(key=lambda x: os.path.getmtime(os.path.join(directory_path, x)))
    return file_list

def extract_rar_file(rar_path, target_directory):
    try:
        with rarfile.RarFile(rar_path) as rf:
            print(f"\nExtracting {os.path.basename(rar_path)}...")
            total_size = sum(f.file_size for f in rf.infolist())
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(rar_path)) as pbar:
                for member in rf.infolist():
                    file_path = os.path.join(target_directory, member.filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    if os.path.isfile(file_path) and os.path.getmtime(file_path) >= member.date_time.timestamp():
                        continue
                    with rf.open(member) as source, open(file_path, 'wb') as target:
                        while True:
                            buf = source.read(4096)
                            if not buf:
                                break
                            target.write(buf)
                            pbar.update(len(buf))
            print("\nSuccessfully extracted.")
    except rarfile.NeedFirstVolume:
        print(f"\nError extracting {os.path.basename(rar_path)}: Missing the first volume required.")
    except rarfile.BadRarFile:
        print(f"\n{os.path.basename(rar_path)} is an invalid RAR file.")
    except FileNotFoundError as e:
        print(f"\nError extracting {os.path.basename(rar_path)}: File not found - {e}")
    except Exception as e:
        print(f"\nError extracting {os.path.basename(rar_path)}: {e}")

def unarchive():
    base_directory = os.getcwd()
    sub_directory = r'Games'
    directory_path = os.path.join(base_directory, sub_directory)
    if not os.path.exists(directory_path):
        print(f"The specified directory does not exist: {directory_path}")
        return

    rar_files = [f for f in os.listdir(directory_path) if f.endswith('.rar')]
    if not rar_files:
        print("No RAR files found.")
        return

    rar_files = sort_files_by_date(rar_files, directory_path)
    part_files = [f for f in rar_files if 'part' in f.lower()]
    non_part_files = [f for f in rar_files if 'part' not in f.lower()]

    # Extract non-part files
    if non_part_files:
        print("Extracting non-part files...")
        for filename in non_part_files:
            rar_path = os.path.join(directory_path, filename)
            if not os.path.isfile(rar_path):
                print(f"File not found: {rar_path}")
                continue
            extract_rar_file(rar_path, directory_path)

    # Extract part files
    if part_files:
        print("Extracting part files...")
        part_files = sort_files_by_part_number(part_files)

        # Determine the base name for the output directory
        base_name = re.sub(r'\.part\d+\.rar$', '', part_files[0])
        target_directory = os.path.join(directory_path, base_name)
        os.makedirs(target_directory, exist_ok=True)

        for filename in part_files:
            rar_path = os.path.join(directory_path, filename)
            if not os.path.isfile(rar_path):
                print(f"File not found: {rar_path}")
                continue
            extract_rar_file(rar_path, target_directory)

    print("All files successfully extracted and updated!")