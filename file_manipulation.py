import pandas as pd
import glob, os, json

def mergeJsonToDf(json_dir):
    #json_dir = 'data/json_files_dir'
    json_pattern = os.path.join(json_dir, '*.json')
    file_list = glob.glob(json_pattern)

    dfs = []
    for file in file_list:
        with open(file) as f:
            json_data = pd.json_normalize(json.loads(f.read()))
            json_data['site'] = file.rsplit("/", 1)[-1]
        dfs.append(json_data)
    df = pd.concat(dfs)
    return df

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   mergeJsonToDf()
