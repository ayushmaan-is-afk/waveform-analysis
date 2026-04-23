import pandas as pd
import numpy as np
from pathlib import Path

DIR = Path('Dataset', 'processed_402_R_faulty.csv')
print(DIR.exists())
path_list = list(DIR.glob('*.csv'))

def crucial_data_extraction(df: pd.DataFrame):
    close_velocity_col_idx = {}
    open_velocity_col_idx = {}

    for col_idx, value in enumerate(df.iloc[0]):
        Channel_no = ''
        if 'Close -Velocity (m/s) :' in str(value):
            actual_velocity = pd.to_numeric(df.iloc[0, col_idx+1], errors='coerce')
            for idx, val in enumerate(df.iloc[:, col_idx]):
                if 'CH' in str(val):
                    Channel_no = val.split()[2]
                    close_velocity_col_idx[Channel_no] = actual_velocity

    for col_idx, value in enumerate(df.iloc[1]):
        Channel_no = ''
        if 'Open -Velocity (m/s) :' in str(value):
            actual_velocity = pd.to_numeric(df.iloc[1, col_idx+1], errors='coerce')
            for idx, val in enumerate(df.iloc[:, col_idx]):
                if 'CH' in str(val):
                    Channel_no = val.split()[2]
                    open_velocity_col_idx[Channel_no] = actual_velocity

    test_run_number = test_run_check(df)
    break_info = break_check(df)

    # df = create_crucial_table(df, close_velocity_col_idx, open_velocity_col_idx, test_run_number, break_info)

    return close_velocity_col_idx, open_velocity_col_idx, test_run_number, break_info, df


def test_run_check(df: pd.DataFrame):
    test_run_number = ''
    try:
        for col_idx, value in enumerate(df.iloc[2]):
            if 'TR' in str(value):
                test_run_number = df.iloc[2, col_idx]
        return test_run_number
    except:
        raise Exception("TEST RUN INFO NOT FOUND!")


def break_check(df: pd.DataFrame):
    rb = {}
    bb = {}
    try:
        rb = resistance_break_check(df)
    except:
        print("⚠️ No RBreak found")
    try:
        bb = bounce_break_check(df)
    except:
        print("⚠️ No BBreak found")
    return rb, bb


def resistance_break_check(df: pd.DataFrame):
    resistance_break_number = {}
    try:
        for col_idx, value in enumerate(df.iloc[3]):
            Channel_no = ''
            if 'RB' in str(value):
                rb_idx = df.iloc[3, col_idx]
                for idx, val in enumerate(df.iloc[:, col_idx]):
                    if 'CH' in str(val):
                        Channel_no = val.split()[2]
                        resistance_break_number[Channel_no] = rb_idx
    except:
        raise Exception("NO SIGNS FOR RESISTANCE BREAK")
    return resistance_break_number


def bounce_break_check(df: pd.DataFrame):
    bounce_break_number = {}
    try:
        for col_idx, value in enumerate(df.iloc[3]):
            Channel_no = ''
            if 'BB' in str(value):
                bb_idx = df.iloc[3, col_idx]
                for idx, val in enumerate(df.iloc[:, col_idx]):
                    if 'CH' in str(val):
                        Channel_no = val.split()[2]
                        bounce_break_number[Channel_no] = bb_idx
    except:
        raise Exception("NO DATA FOR BOUNCE BREAK FOUND!")
    return bounce_break_number


def create_crucial_table(df: pd.DataFrame, close_velocity: dict, open_velocity: dict, test_run: str, break_info: tuple):
    rb, bb = break_info

    for channel in close_velocity.keys():
        current_col_name = f"DCRM Current {channel} in Amp"

        if current_col_name in df.columns:
            insert_pos = df.columns.get_loc(current_col_name) + 1

            if channel in close_velocity:
                df.insert(insert_pos, f"{channel} Close-Velocity (m/s)", close_velocity[channel])
                insert_pos += 1

            if channel in open_velocity:
                df.insert(insert_pos, f"{channel} Open-Velocity (m/s)", open_velocity[channel])
                insert_pos += 1

            df.insert(insert_pos, f"{channel} Test Run", test_run)
            insert_pos += 1

            if channel in rb:
                df.insert(insert_pos, f"{channel} Resistance Break", rb[channel])
                insert_pos += 1

            if channel in bb:
                df.insert(insert_pos, f"{channel} Bounce Break", bb[channel])

    return df

def df_modify(df: pd.DataFrame):
    df.columns = df.iloc[5]
    df = df[5:]
    df.reset_index(drop=True, inplace=True)
    df = df.dropna(axis=1, how='all')
    
    return df

def data_preprocessing(filepath, phase='Unknown'):
    # Check if already processed
    # processed_files = list(DIR.glob('processed_*.csv'))
    # if any(filepath.stem in f.name for f in processed_files):
    #     print(f"⚠️ {filepath.name} already processed, skipping!")
    #     return None, None, None, None, None

    df = pd.read_csv(filepath, header=None)

    try:
        if df.iloc[0].astype(str).str.contains('Close -Velocity (m/s) :', regex=False).any() and \
           df.iloc[1].astype(str).str.contains('Open -Velocity (m/s) :', regex=False).any():
            print("Crucial data found. Proceeding with extraction.")
            close_velocity, open_velocity, test_run, resistance_break, df = crucial_data_extraction(df)
            df = df_modify(df)
        elif df.iloc[0].astype(str).str.contains('Close -Velocity (m/s) :', regex=False).any():
            print("Only Close Velocity found.")
            close_velocity, open_velocity, test_run, resistance_break, df = crucial_data_extraction(df)
            df = df_modify(df)
        elif df.iloc[1].astype(str).str.contains('Open -Velocity (m/s) :', regex=False).any():
            print("Only Open Velocity found.")
            close_velocity, open_velocity, test_run, resistance_break, df = crucial_data_extraction(df)
            df = df_modify(df)
        elif df.iloc[0].astype(str).str.contains('Coil Current (A) ', regex=False).any():
            print("Coil current found. File is already pre-processed.")
            
    except Exception as e:
        raise Exception(f"UNABLE TO FIND CHANNEL SPECIFIC DATA: {e}")

    # Add phase
    df['phase'] = phase
    
    # save_path = Path('.', 'Dataset', 'pre-processed', f'processed_{filepath.stem}.csv')
    # df.to_csv(save_path, index=False)
    # print(f"✅ Saved: {save_path.name}")
    
    cols = ['Coil Current C1 (A)', 'Coil Current C2 (A)', 'Coil Current C3 (A)',
       'Coil Current C4 (A)', 'Coil Current C5 (A)', 'Coil Current C6 (A)',
       'Contact Travel T1 (mm)', 'Contact Travel T2 (mm)',
       'Contact Travel T3 (mm)', 'Contact Travel T4 (mm)',
       'Contact Travel T5 (mm)', 'Contact Travel T6 (mm)',
       'DCRM Res CH1 in uOhm', 'DCRM Current CH1 in Amp',
       'CH1 Close-Velocity (m/s)', 'CH1 Open-Velocity (m/s)', 'CH1 Test Run',
       'DCRM Res CH2 in uOhm', 'DCRM Current CH2 in Amp',
       'CH2 Close-Velocity (m/s)', 'CH2 Open-Velocity (m/s)', 'CH2 Test Run',
       'DCRM Res CH3 in uOhm', 'DCRM Current CH3 in Amp',
       'CH3 Close-Velocity (m/s)', 'CH3 Open-Velocity (m/s)', 'CH3 Test Run',
       'DCRM Res CH4 in uOhm', 'DCRM Current CH4 in Amp',
       'CH4 Close-Velocity (m/s)', 'CH4 Open-Velocity (m/s)', 'CH4 Test Run',
       'DCRM Res CH5 in uOhm', 'DCRM Current CH5 in Amp',
       'CH5 Close-Velocity (m/s)', 'CH5 Open-Velocity (m/s)', 'CH5 Test Run',
       'DCRM Res CH6 in uOhm', 'DCRM Current CH6 in Amp',
       'CH6 Close-Velocity (m/s)', 'CH6 Open-Velocity (m/s)', 'CH6 Test Run',
       'phase', 'CH3 Resistance Break', 'CH4 Resistance Break',
       'CH3 Bounce Break', 'CH4 Bounce Break', 'breaker_id',
       'CH1 Resistance Break', 'CH2 Resistance Break', 'CH1 Bounce Break',
       'CH2 Bounce Break']
    
    df.columns = df.iloc[0]
    df = df.drop(index=0)
    df = df.reset_index(drop=True)
    
    
    for col in cols:
        if col not in df.columns:
            df[col] = np.nan
   
    # if df.columns.str.contains('Unknown').any():
    #     df = df.drop(columns=df.columns[df.columns.str.contains('Unknown')])
            
    
    # print("*"*70)        
    # print(df.columns)
    # print("*"*70)
    # print(df.head())
    # print("*"*70)  
    # print("*"*70)
    # print("Look here")  
    # print(list(set(cols) - set(df.columns)))
    # print(df.columns)
    return df



def process_all_files(filepath):
    all_dfs = []

    # Process bad file
    print("\n--- Processing BAD file ---")
    result = data_preprocessing(filepath, phase='R')
    if result[4] is not None:
        result[4]['status'] = 'faulty'   # ← use status instead of label
        all_dfs.append(result[4])

    # Process all good files
    print("\n--- Processing GOOD files ---")
    for file in path_list:
        try:
            # Extract phase from filename
            try:
                phase = file.stem.split('-')[1].split(' ')[0]
            except:
                phase = 'Unknown'

            result = data_preprocessing(file, phase=phase)
            if result[4] is not None:
                result[4]['status'] = 'good'  # ← use status instead of label
                all_dfs.append(result[4])
            print(f"✅ Done: {file.name}")
        except Exception as e:
            print(f"❌ Failed: {file.name} → {e}")
    
    # Combine all
    
    if all_dfs:
        final_df = pd.concat(all_dfs, ignore_index=True)
        final_df.to_csv(STORE_PROCESSED_GOOD_DATA, index=False)
        print(f"\n✅ Final dataset saved!")
        print(f"Total rows  : {len(final_df)}")
        print(f"Good rows   : {len(final_df[final_df['status']=='good'])}")
        print(f"Faulty rows : {len(final_df[final_df['status']=='faulty'])}")
        print(f"Phases      : {final_df['phase'].unique()}")
        return final_df
    else:
        print("❌ No files processed!")
        return None


# # Run everything
# # final_df = process_all_files(DIR)
# df = pd.read_csv(DIR)
# close_velocity_col_idx, open_velocity_col_idx, test_run_number, break_info, df1 = crucial_data_extraction(df)



data_preprocessing(DIR)
