import pandas as pd
import numpy as np
from pathlib import Path
import logging
from sklearn.utils import compute_class_weight

logging.basicConfig(level=logging.INFO)
STORE_PROCESSED_DATA = Path('..','Dataset','processed_data.csv')
BAD_DATA_PATH = Path('..', 'Dataset', 'bad', '402_R_faulty.csv')
DATA_PATH = Path('..', 'Dataset', 'good')

def crucial_data_extraction(df: pd.DataFrame):
    close_velocity_col_idx = {}
    
    for col_idx, value in enumerate(df.iloc[0]):
        Channel_no = ''
        if 'Close -Velocity (m/s) :' in str(value):
            actual_velocity_col_idx = pd.to_numeric(df.iloc[0, col_idx+1], errors='coerce')
            for idx, val in enumerate(df.iloc[:,col_idx]):
                if 'CH' in str(val): 
                    Channel_no = val.split()[2]
                    Channel_no = f"{Channel_no} Close -Velocity (m/s)"
                    col_idx+=1 
                    close_velocity_col_idx[Channel_no] = actual_velocity_col_idx
                                
    open_velocity_col_idx = {}
    
    for col_idx, value in enumerate(df.iloc[1]):
        Channel_no = ''
        if 'Open -Velocity (m/s) :' in str(value):
            actual_velocity_col_idx = pd.to_numeric(df.iloc[1, col_idx+1], errors='coerce')
            for idx, val in enumerate(df.iloc[:,col_idx]):
                if 'CH' in str(val): 
                    Channel_no = val.split()[2]
                    Channel_no = f"{Channel_no} Open -Velocity (m/s)"
                    col_idx+=1 
                    open_velocity_col_idx[Channel_no] = actual_velocity_col_idx                
                    
    test_run_number = test_run_check(df)
    break_info = break_check(df)
      
    return close_velocity_col_idx, open_velocity_col_idx, test_run_number, break_info   

def test_run_check(df: pd.DataFrame):
    test_run_number = ''
    try:
        for col_idx, value in enumerate(df.iloc[2]):
            Channel_no = ''
            if 'TR' in str(value):
                actual_TR_number =df.iloc[2,col_idx]
                test_run_number = actual_TR_number
        
        return test_run_number    
    
    except:
        raise Exception("TEST RUN INFO NOT FOUND!")


def break_check(df: pd.DataFrame):
    try:
        rb = resistance_break_check(df)
    except:
        raise Exception("NO BOUNCE DATA FOUND!")
    else:
        bb = bounce_break_check(df)
        
    return rb, bb
    
def resistance_break_check(df: pd.DataFrame):
    resistance_break_number = {}
    try:
        for col_idx, value in enumerate(df.iloc[3]):
            Channel_no = ''
            if 'RB' in str(value):
                rb_idx = df.iloc[3, col_idx]
                for idx, val in enumerate(df.iloc[:,col_idx]):
                    if 'CH' in str(val): 
                        Channel_no = val.split()[2]
                        resistance_break_number[Channel_no] = rb_idx     
    except:
        raise Exception("NO SIGNS FOR RESISTANCE BREAK, CHECKING FOR BOUNCE BREAK")
    
    return resistance_break_number
    

def bounce_break_check(df: pd.DataFrame):
    bounce_break_number = {}
    try:
        for col_idx, value in enumerate(df.iloc[3]):
            Channel_no = ''
            if 'BB' in str(value):
                bb_idx = df.iloc[3, col_idx]
                for idx, val in enumerate(df.iloc[:,col_idx]):
                    if 'CH' in str(val): 
                        Channel_no = val.split()[2]
                        bounce_break_number[Channel_no] = bb_idx 
    except:
        raise Exception("NO DATA FOR BOUNCE BREAK FOUND!") 

    return bounce_break_number
    
    
def data_initialization(df: pd.DataFrame):
    close_velocity = {}
    open_velocity = {}
    test_run = ''
    resistance_break = {}
    try:
        if df.iloc[0].astype(str).str.contains('Close -Velocity (m/s) :', regex=False).any() and df.iloc[1].astype(str).str.contains('Open -Velocity (m/s) :', regex=False).any():
            print("Crucial data found. Proceeding with extraction.")
            close_velocity, open_velocity, test_run, resistance_break = crucial_data_extraction(df)
        elif df.iloc[0].astype(str).str.contains('Close -Velocity (m/s) :', regex=False).any():
            print("Only 'Close -Velocity (m/s) :' found. Proceeding with extraction.")
            close_velocity, open_velocity, test_run, resistance_break = crucial_data_extraction(df)
        elif df.iloc[1].astype(str).str.contains('Open -Velocity (m/s) :', regex=False).any():
            print("Only 'Open -Velocity (m/s) :' found. Proceeding with extraction.")
            close_velocity, open_velocity, test_run, resistance_break = crucial_data_extraction(df)
    except:
        e = "UNABLE TO FIND CHANNEL SPECIFIC DATA, INITIALIZING PROCESSING WITH METHOD 2"
        raise Exception(e) 
    
    df.columns = df.iloc[4]
    df = df[5:]
    df.reset_index(drop=True, inplace=True)
    df = df.dropna(axis=1, how='all')
    
    df.to_csv(STORE_PROCESSED_DATA, index=False)


def data_preprocessing(filepath):
    df = pd.read_csv(filepath, header=None)
    data_initialization(df)




file_path = BAD_DATA_PATH
data_preprocessing(file_path)
