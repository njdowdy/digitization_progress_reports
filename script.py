from functions import cleaning_funcs as cle
from functions import calculation_funcs as cal
from functions import plotting_funcs as plt

mypath = 'input/TPT Digi Numbers Reported - Year3 AugOct21.csv'

if __name__ == "__main__":
    df = cle.import_data(mypath)
    df = cle.clean_import(df)
    df = cle.make_totals_row(df)
    df = cle.wide_to_long(df)
    df = cal.create_percentages(df)
    df = cal.calculate_statistics(df)
    plt.create_plots(df)
