import os
import json

# Function to process only scores.rank_0.json files and extract scores
def process_json_files_in_folder(folder_path):
    all_results = []  # Collect results from all folders

    for root, _, files in os.walk(folder_path):
        for filename in files:
            # Only process files exactly named "scores.rank_0.json"
            if filename == "scores.rank_0.json":
                file_path = os.path.join(root, filename)

                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)

                        # Extract aggregate_score, ptm, and iptm
                        aggregate_score = data.get('aggregate_score')
                        ptm = data.get('ptm')
                        iptm = data.get('iptm')

                        # Safe rounding helper
                        def safe_round(value):
                            return round(value, 2) if isinstance(value, (int, float)) else value

                        all_results.append({
                            'folder': root,
                            'file': file_path,
                            'aggregate_score': safe_round(aggregate_score),
                            'ptm': safe_round(ptm),
                            'iptm': safe_round(iptm)
                        })

                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {file_path}")
                except Exception as e:
                    print(f"An error occurred while processing {file_path}: {e}")

    # Sort results alphabetically by folder path
    all_results.sort(key=lambda x: x['folder'].lower())

    # Print sorted results
    for result in all_results:
        print(f"\nResults for folder: {result['folder']}")
        print(f"File: {result['file']}")
        print(f"Aggregate Score: {result['aggregate_score']}")
        print(f"PTM: {result['ptm']}")
        print(f"IPTM: {result['iptm']}")
        print("-" * 30)


# Define the root directory to start the search
root_directory = '.'  # Change this to your target directory

# Process all scores.rank_0.json files within the root directory and its subfolders
process_json_files_in_folder(root_directory)
