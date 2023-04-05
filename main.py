import calculate
import pandas as pd

dataset = "DataScientist.csv"
df = pd.read_csv(dataset, index_col = 0)

def main(df):
    calculate.clean_dataset(df)
    #calculate.transform_dataset(df)
    #calculate.top_10_words_in_column(df)
    #alculate.plot_graphs(df)
    return df
if __name__ == "__main__":
    main(df)
    
print(df["Size"].head(10))