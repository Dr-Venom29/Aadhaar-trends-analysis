import pandas as pd

def clean_columns(df):
    """Standardizes column names to lowercase and removes spaces."""
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df

def create_master_record(df_enrol, df_demo, df_bio):
    """
    Merges the three categories on Date, State, and District.
    """
    # 1. Standardize all
    df_enrol = clean_columns(df_enrol)
    df_demo = clean_columns(df_demo)
    df_bio = clean_columns(df_bio)

    # 2. Aggregate counts to avoid duplicates during merge
    # We group by the unique identifiers of a record
    group_keys = ['date', 'state', 'district']
    
    enrol_grp = df_enrol.groupby(group_keys).sum(numeric_only=True).reset_index()
    demo_grp = df_demo.groupby(group_keys).sum(numeric_only=True).reset_index()
    bio_grp = df_bio.groupby(group_keys).sum(numeric_only=True).reset_index()

    # 3. Outer Merge to ensure no data loss
    master = pd.merge(enrol_grp, demo_grp, on=group_keys, how='outer', suffixes=('_enrol', '_demo'))
    master = pd.merge(master, bio_grp, on=group_keys, how='outer')
    
    # Fill NaN with 0 for districts that had no activity in one category
    return master.fillna(0)