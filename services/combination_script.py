import pandas as pd
from pathlib import Path

files = 'final_breaker_data'
save_file_name = 'final_preprocessed_good_data.csv'
PRE_PROCESSED_DATA_PATH = Path('.', 'Dataset','pre-processed',files)
PRE_PROCESSED_DATA_SAVE_PATH = Path('.', 'Dataset', 'pre-processed', save_file_name)

pre_processed_list = [
    f for f in PRE_PROCESSED_DATA_PATH.glob('*.csv') 
    if f.name != save_file_name
]

all_dfs = []

for i in pre_processed_list:
    print(f"File Name: {i.name}")
          
for file in pre_processed_list:
    try:
        df = pd.read_csv(file)
        all_dfs.append(df)
        print(f"✅ Loaded: {file.name}")
    except Exception as e:
        print(f"❌ Failed to load: {file.name} → {e}")
    
            
if all_dfs:
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df.to_csv(PRE_PROCESSED_DATA_SAVE_PATH, index=False)
    print(final_df['phase'].value_counts())
    print(f"\n✅ Final preprocessed dataset saved!")
    print(f"Total rows  : {len(final_df)}")
    
else:
    print("❌ No preprocessed files found to combine!")     