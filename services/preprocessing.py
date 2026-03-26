import pandas as pd
import numpy as np
from pathlib import Path
# import logging

# logging.basicConfig(level=logging.INFO)
STORE_PROCESSED_BAD_DATA = Path('.','Dataset','pre-processed','402_faulty')
# STORE_PROCESSED_GOOD_DATA = Path('.','Dataset','processed_good_data.csv')
BAD_DATA_PATH = Path('.', 'Dataset', 'bad', '402_R_faulty.csv')
# DATA_PATH = Path('.', 'Dataset', 'good', '410')
# good_list = list(DATA_PATH.glob('*.csv'))
sub_dir = '402_faulty'

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

    df.columns = df.iloc[4]
    df = df[5:]
    df.reset_index(drop=True, inplace=True)
    df = df.dropna(axis=1, how='all')

    df = create_crucial_table(df, close_velocity_col_idx, open_velocity_col_idx, test_run_number, break_info)

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


def data_preprocessing(filepath, phase='Unknown'):
    # Check if already processed
    processed_dir = Path('.', 'Dataset', 'pre-processed', sub_dir)
    processed_files = list(processed_dir.glob('processed_*.csv'))
    if any(filepath.stem in f.name for f in processed_files):
        print(f"⚠️ {filepath.name} already processed, skipping!")
        return None, None, None, None, None

    df = pd.read_csv(filepath, header=None)
    close_velocity = {}
    open_velocity = {}
    test_run = ''
    resistance_break = {}

    try:
        if df.iloc[0].astype(str).str.contains('Close -Velocity (m/s) :', regex=False).any() and \
           df.iloc[1].astype(str).str.contains('Open -Velocity (m/s) :', regex=False).any():
            print("Crucial data found. Proceeding with extraction.")
            close_velocity, open_velocity, test_run, resistance_break, df = crucial_data_extraction(df)
        elif df.iloc[0].astype(str).str.contains('Close -Velocity (m/s) :', regex=False).any():
            print("Only Close Velocity found.")
            close_velocity, open_velocity, test_run, resistance_break, df = crucial_data_extraction(df)
        elif df.iloc[1].astype(str).str.contains('Open -Velocity (m/s) :', regex=False).any():
            print("Only Open Velocity found.")
            close_velocity, open_velocity, test_run, resistance_break, df = crucial_data_extraction(df)
    except Exception as e:
        raise Exception(f"UNABLE TO FIND CHANNEL SPECIFIC DATA: {e}")

    # Add phase instead of label
    df['phase'] = phase

    save_path = Path('.', 'Dataset', 'pre-processed',sub_dir, f'processed_{filepath.stem}.csv')
    df.to_csv(save_path, index=False)
    print(f"✅ Saved: {save_path.name}")

    return close_velocity, open_velocity, test_run, resistance_break, df


def process_all_files():
    all_dfs = []

    # Process bad file
    print("\n--- Processing BAD file ---")
    result = data_preprocessing(BAD_DATA_PATH, phase='R')
    if result[4] is not None:
        result[4]['status'] = 'faulty'   # ← use status instead of label
        all_dfs.append(result[4])

    # # Process all good files
    # print("\n--- Processing GOOD files ---")
    # for file in good_list:
    #     try:
    #         # Extract phase from filename
    #         try:
    #             phase = file.stem.split('-')[1].split(' ')[0]
    #         except:
    #             phase = 'Unknown'

    #         result = data_preprocessing(file, phase=phase)
    #         if result[4] is not None:
    #             result[4]['status'] = 'good'  # ← use status instead of label
    #             all_dfs.append(result[4])
    #         print(f"✅ Done: {file.name}")
    #     except Exception as e:
    #         print(f"❌ Failed: {file.name} → {e}")
    
    # Combine all
    # if all_dfs:
    #     final_df = pd.concat(all_dfs, ignore_index=True)
    #     final_df.to_csv(STORE_PROCESSED_GOOD_DATA, index=False)
    #     print(f"\n✅ Final dataset saved!")
    #     print(f"Total rows  : {len(final_df)}")
    #     print(f"Good rows   : {len(final_df[final_df['status']=='good'])}")
    #     print(f"Faulty rows : {len(final_df[final_df['status']=='faulty'])}")
    #     print(f"Phases      : {final_df['phase'].unique()}")
    #     return final_df
    # else:
    #     print("❌ No files processed!")
        return None


# Run everything
final_df = process_all_files()
