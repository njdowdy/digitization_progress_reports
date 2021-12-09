import os
import pandas as pd


def import_data(path: str):
    df = pd.read_csv(path)
    return df
