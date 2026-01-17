import pandas as pd
import glob
import os

def load_category_data(base_path, category):
    """
    Finds all CSVs in a subfolder (e.g., 'enrolment'), 
    reads them, and returns a single combined DataFrame.
    """
    path = os.path.join(base_path, category, "*.csv")
    files = glob.glob(path)
    
    if not files:
        print(f"Warning: No files found in {category}")
        return pd.DataFrame()
    
    df_list = []
    for file in files:
        temp_df = pd.read_csv(file)
        # Add filename as a reference to track data source/date
        temp_df['source_file'] = os.path.basename(file)
        df_list.append(temp_df)
    
    return pd.concat(df_list, axis=0, ignore_index=True)