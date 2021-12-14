from functions import cleaning_funcs as cle
from functions import calculation_funcs as cal
from functions import plotting_funcs as plt

template_path = "input/input_template.csv"
tpt = "input/TPT Digi Numbers Reported - Year3 AugOct21.csv"

if __name__ == "__main__":
    # utilizing the generic template
    df = cle.import_data(template_path)  # import data [see 'input/input_template.csv']
    df = cle.clean_import_template(df)  # clean data [if following template]
    # df = cle.clean_import_tpt(df)  # clean data [TPT-specific formatting]
    df = cle.make_totals_row(
        df, total_label="TOTAL", total_code="TOTAL"
    )  # make totals row
    df = cle.wide_to_long(df)  # convert to long data format
    df = cal.create_percentages(df)  # calculate percentages from reported values
    df = cal.calculate_statistics(df)  # calculate plotting statistics
    plt.create_plots(df)  # plot statistics
