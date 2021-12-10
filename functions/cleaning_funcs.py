import pandas as pd


def import_data(path: str):
    df = pd.read_csv(path)
    return df


def clean_import(df: pd.DataFrame):
    df_out = df.drop(df.index[0:3])
    df_out = df_out.drop(df_out.columns[[2, 3, 4, 5, 8, 11, 14, 17, 18, 19, 20, 21]], axis=1)
    df_out = df_out.set_axis(['collection_name',
                              'collection_code',
                              'proposed_transcriptions',
                              'reported_transcriptions',
                              'proposed_scanned_vials',
                              'reported_scanned_vials',
                              'proposed_scanned_slides',
                              'reported_scanned_slides',
                              'proposed_hires_images',
                              'reported_hires_images'], axis=1)
    df_out = df_out.replace(['X', '?', 'NA'], '0')
    df_out = df_out.apply(lambda x: pd.to_numeric(x.str.replace(',', '')) if x.name in list(df_out.columns[2:]) else x)
    df_out.columns = df_out.columns.str.strip()
    return df_out


def make_totals_row(df: pd.DataFrame):
    df_out = df.append(df.sum(numeric_only=True), ignore_index=True)
    df_out.at[len(df_out) - 1, 'collection_name'] = 'TPT_TOTAL'
    df_out.at[len(df_out) - 1, 'collection_code'] = 'TPT'
    return df_out


def wide_to_long(df: pd.DataFrame):
    df_long = df.melt(id_vars=['collection_name', 'collection_code'])
    df_long[['class', 'type']] = df_long['variable'].str.split('_', 1, expand=True)
    df_long = df_long.drop('variable', axis=1)
    df_long = df_long[['collection_name',
                       'collection_code',
                       'class',
                       'type',
                       'value']]
    df_long = df_long.pivot_table(values='value',
                                  index=['collection_name', 'collection_code', 'type'],
                                  columns=['class'])
    df_long.reset_index(inplace=True)
    return df_long
