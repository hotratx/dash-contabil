import pandas as pd


def create_df(datas: list):
    """Monta o DataFrame com os dados do banco"""
    df = pd.DataFrame()
    for data in datas:
        df0 = pd.DataFrame(data.dict(), index=[0])
        df0.set_index("tri", inplace=True)
        df = pd.concat([df, df0])
    return df, list(set(df.index.year.values))
