import application as d

# import os
# os.chdir('./digitization_progress_reports')

mypath = "application/input/input_template.csv"
#!TPT!# mypath = "application/input/TPT_YR3_NOV-JAN1.csv"
myoutput = "application/output/figures/"


def entrypoint(path: str, output: str) -> None:
    df = d.clean.import_data(path)  # import data [see 'input/input_template.csv']
    df = d.clean.clean_import_template(df)  # clean data [if following template]
    #!TPT!# df = d.clean.clean_import_tpt(df)  # clean data [TPT-specific formatting]
    df = d.clean.make_totals_row(df)  # make totals row
    df = d.clean.wide_to_long(df)  # convert to long data format
    df = d.calc.create_percentages(df)  # calculate percentages from reported values
    df = d.calc.calculate_statistics(df)  # calculate plotting statistics
    d.plot.create_plots(df, output_path=output)  # plot statistics


if __name__ == "__main__":
    entrypoint(mypath, myoutput)
