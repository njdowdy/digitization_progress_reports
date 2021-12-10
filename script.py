from functions import cleaning_funcs as cf

mypath = 'input/TPT Digi Numbers Reported - Year3 AugOct21.csv'

if __name__ == "__main__":
    df = cf.import_data(mypath)
    df = cf.clean_import(df)
    df = cf.make_totals_row(df)
    df = cf.wide_to_long(df)

