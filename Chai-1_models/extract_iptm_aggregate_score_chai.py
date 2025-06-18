import os
import json

# Function to process the files and extract scores
def process_json_files_in_folder(folder_path):
    # Dictionary to store files and their aggregate_score, ptm, and iptm
    results = []
    
    # Iterate over all files and subdirectories in the folder
    for root, _, files in os.walk(folder_path):
        folder_results = []  # Store results for the current folder
        
        for filename in files:
            # Check if the file has a .json extension
            if filename.endswith('.json'):
                # Construct the full path to the JSON file
                file_path = os.path.join(root, filename)
                
                try:
                    # Open and load the JSON file
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        
                        # Extract aggregate_score, ptm, and iptm
                        aggregate_score = data.get('aggregate_score')
                        ptm = data.get('ptm')
                        iptm = data.get('iptm')
                        
                        # Append the results to the list for the current folder
                        folder_results.append({
                            'file': file_path,
                            'aggregate_score': aggregate_score,
                            'ptm': ptm,
                            'iptm': iptm
                        })
                
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {file_path}")
                except Exception as e:
                    print(f"An error occurred while processing the file {file_path}: {e}")
        
        # Sort the results within the folder by aggregate_score
        if folder_results:
            folder_results.sort(key=lambda x: x['aggregate_score'], reverse=True)
            
            # Print sorted results for the current folder
            print(f"\nResults for folder: {root}")
            for result in folder_results:
                print(f"File: {result['file']}")
                print(f"Aggregate Score: {result['aggregate_score']}")
                print(f"PTM: {result['ptm']}")
                print(f"IPTM: {result['iptm']}")
                print("-" * 30)

# Define the root directory to start the search
root_directory = '.'  # Change this to the specific directory you want to search from

# Process all .json files within the root directory and its subfolders
process_json_files_in_folder(root_directory)
