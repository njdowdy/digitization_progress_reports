import os
import pandas as pd
from matplotlib import pyplot as plt


def create_plots(df: pd.DataFrame,
                 t_start=0,
                 t_present=28,
                 t_end=36,
                 t_extended=48,
                 checkpoint_completion=60,
                 output_path='output/figures/'
                 ):
    # TODO: Annotate records/month on line segments to show rate needed
    # TODO: Add 2nd y-axis with counts instead of percentages only
    # TODO: Add meaningful axes labels
    # TODO: add x-axis labels at the vertical key date points
    # TODO: color each line group (L1-L5) differently and provide legend explaining each scenario (by deadline, by ext.)
    for idx, row in df.iterrows():
        if row.plot_group == 'L1':
            plt.rcParams["figure.figsize"] = [7.50, 3.50]
            plt.rcParams["figure.autolayout"] = True
            plt.title(f"{row.collection_code.replace(' | ', '-')}_{row.category}")
            plt.hlines(100, 0, 50, color='green', linestyle="--")  # target completeness
            plt.hlines(checkpoint_completion, 0, 50, color='green', linestyle="--", alpha=0.5)  # target checkpoint
            plt.vlines(t_start, 0, 100, color='gray', linestyle="--", alpha=0.5)  # starting date
            plt.vlines(t_present, 0, 100, color='gray', linestyle="--", alpha=0.5)  # present date
            plt.vlines(t_end, 0, 100, color='gray', linestyle="--", alpha=0.5)  # end date
            plt.vlines(t_extended, 0, 100, color='gray', linestyle="--", alpha=0.5)  # extension date
            plt_color = 'green'
            plt_line = '-'
        else:
            plt_color = 'grey'
            plt_line = '--'
        line_segment_data = [[row.start_x, row.start_y], [row.end_x, row.end_y]]  # [[start_x, start_y], [end_x, end_y]]
        plt.plot([line_segment_data[0][0],
                  line_segment_data[1][0]],
                 [line_segment_data[0][1],
                  line_segment_data[1][1]], color=plt_color, linestyle=plt_line)
        if row.plot_group == 'L5':
            output_directory = f"{output_path}{row.collection_code.replace(' | ', '-')}/"
            os.makedirs(output_directory, exist_ok=True)
            plt.savefig(f"{output_directory}{row.category}.png")
            plt.clf()
    return
