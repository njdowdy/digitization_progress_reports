from digitization_progress_reports.functions import cleaning_funcs as cle
from digitization_progress_reports.functions import calculation_funcs as cal
from digitization_progress_reports.functions import plotting_funcs as plt

mypath = "digitization_progress_reports/input/input_template.csv"
# mypath = "digitization_progress_reports/input/TPT Digi Numbers Reported - Year3 AugOct21.csv"
output = "digitization_progress_reports/output/figures/"

if __name__ == "__main__":
    df = cle.import_data(mypath)  # import data [see 'input/input_template.csv']
    df = cle.clean_import_template(df)  # clean data [if following template]
    # df = cle.clean_import_tpt(df)  # clean data [TPT-specific formatting]
    df = cle.make_totals_row(df)  # make totals row
    df = cle.wide_to_long(df)  # convert to long data format
    df = cal.create_percentages(df)  # calculate percentages from reported values
    df = cal.calculate_statistics(df)  # calculate plotting statistics
    plt.create_plots(df, output_path=output)  # plot statistics
