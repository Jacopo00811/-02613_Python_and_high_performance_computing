import pandas as pd

def reduce_dmi_df(df):
    df['created'] = pd.to_datetime(df['created'], format='ISO8601')
    df['observed'] = pd.to_datetime(df['observed'], format='ISO8601')
    df['parameterId'] = df['parameterId'].astype('category')
    # df['stationId'] = df['stationId'].astype('category')
    return df

def summarize_columns(df):
    print(pd.DataFrame([
        (
            c,
            df[c].dtype,
            len(df[c].unique()),
            df[c].memory_usage(deep=True) // (1024**2)
        ) for c in df.columns
    ], columns=['name', 'dtype', 'unique', 'size (MB)']))
    print('Total size:', df.memory_usage(deep=True).sum() / 1024**2, 'MB')


if __name__ == '__main__':
    path = '/dtu/projects/02613_2025/data/dmi/2023_01.csv.zip'
    df = pd.read_csv(path)
    summarize_columns(df)
    df_reduced = reduce_dmi_df(df)
    summarize_columns(df_reduced)
