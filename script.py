import digitization_progress_reports as d

mypath = "digitization_progress_reports/input/input_template.csv"
# mypath = "digitization_progress_reports/input/TPT Digi Numbers Reported - Year3 AugOct21.csv"
output = "digitization_progress_reports/output/figures/"

if __name__ == "__main__":
    df = d.clean.import_data(mypath)  # import data [see 'input/input_template.csv']
    df = d.clean.clean_import_template(df)  # clean data [if following template]
    # df = d.clean.clean_import_tpt(df)  # clean data [TPT-specific formatting]
    df = d.clean.make_totals_row(df)  # make totals row
    df = d.clean.wide_to_long(df)  # convert to long data format
    df = d.calc.create_percentages(df)  # calculate percentages from reported values
    df = d.calc.calculate_statistics(df)  # calculate plotting statistics
    d.plot.create_plots(df, output_path=output)  # plot statistics
