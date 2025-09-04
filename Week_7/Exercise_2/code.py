import pandas as pd

def df_memsize(df):
    return df.memory_usage(deep=True).sum()

if __name__ == '__main__':
    path = '/dtu/projects/02613_2025/data/dmi/2023_01.csv.zip'
    df = pd.read_csv(path)
    print("Memory size of the dataframe: ", df_memsize(df))