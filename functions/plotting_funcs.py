import os
import math
import pandas as pd
from matplotlib import pyplot as plt


def create_plots(
    df: pd.DataFrame,
    t_start=0,
    t_present=28,
    t_end=36,
    t_extended=48,
    output_path="output/figures/",
    annotations=True,
):
    annotate_line = annotations
    base_font_size = 24
    cap = 120
    fig, ax = plt.subplots()  # blank assignment (overwritten)
    ax2 = ax.twinx()  # blank assignment (overwritten)
    for idx, row in df.iterrows():
        if row.plot_group == "L1":
            plt.rcParams["figure.figsize"] = [19.20, 10.80]  # in 1/100 pixels
            plt.rcParams["figure.autolayout"] = True
            plt.rc("font", size=base_font_size)
            fig, ax = plt.subplots()
            ax.set_xlim([t_start, t_extended + 1])
            ax.set_ylim([0, cap + 1])
            ax2 = ax.twinx()
            ax.hlines(100, 0, 50, color="green", linestyle="--")  # target completeness
            ax.vlines(
                t_start, 0, 100, color="gray", linestyle="--", alpha=0.3
            )  # starting date
            ax.vlines(
                t_present, 0, 100, color="gray", linestyle="--", alpha=0.3
            )  # present date
            ax.vlines(
                t_end, 0, 100, color="gray", linestyle="--", alpha=0.3
            )  # end date
            ax.vlines(
                t_extended, 0, 100, color="gray", linestyle="--", alpha=0.3
            )  # extension date
            plt_color = "green"
            plt_line = "-"
            legend_lab = "Project Start - Present"
            if row.end_y == 0:  # turn off annotations of empty plots
                annotate_line = False
            else:
                annotate_line = annotations
        elif row.plot_group == "L2":
            if row.end_y == 0:  # turn off annotations of empty plots
                annotate_line = False
            else:
                annotate_line = annotations
            plt_color = "red"
            plt_line = "--"
            legend_lab = "Present - Project End"
        elif row.plot_group == "L3":
            plt_color = "yellow"
            plt_line = "--"
            legend_lab = "Present - Project Extension"
        elif row.plot_group == "L4A":
            plt_color = "orange"
            plt_line = "--"
            legend_lab = (
                f"Present - Project Extension with {round(row.end_y, 2)}% Checkpoint"
            )
            ax.hlines(
                row.end_y, 0, 50, color="green", linestyle="--", alpha=0.3
            )  # target checkpoint
        elif row.plot_group == "L4B":
            plt_color = "orange"
            plt_line = "--"
            legend_lab = None  # remove legend for 2nd line segment of L4
        else:
            plt_color = "grey"
            plt_line = "--"
            legend_lab = "Unknown"
        if (
            row.plot_group in ["L2", "L3"] and row.start_y >= 100
        ):  # force projections above 100% to be green
            plt_color = "green"
            plt_line = "--"
            annotate_line = False
            legend_lab = None
        elif row.plot_group in ["L4A", "L4B"] and row.start_y >= 100:
            plt_color = "green"
            plt_line = ""
            annotate_line = False
            legend_lab = None
        line_segment_data = [
            [row.start_x, row.start_y],
            [row.end_x, row.end_y],
        ]  # [[start_x, start_y], [end_x, end_y]]
        ax.plot(
            [line_segment_data[0][0], line_segment_data[1][0]],
            [line_segment_data[0][1], line_segment_data[1][1]],
            color=plt_color,
            linestyle=plt_line,
            label=legend_lab,
        )
        if annotate_line:
            if row.plot_group in ["L4A", "L4B"]:
                x_offset = 0.5
                y_offset = -1
                xytextbox = (25, -50)
                xytextarrow = (15, -15)
                v_align = "bottom"
            else:
                x_offset = -0.5
                y_offset = 1
                xytextbox = (-25, 50)
                xytextarrow = (-15, 15)
                v_align = "top"
            ax2.annotate(
                f"Rate (per mo.):\n{round(row.rate_count, 2)}",
                xy=(
                    x_offset + (row.end_x - row.start_x) / 2 + row.start_x,
                    y_offset
                    + (row.end_y_count - row.start_y_count) / 2
                    + row.start_y_count,
                ),
                xycoords="data",
                xytext=xytextbox,
                textcoords="offset points",
                horizontalalignment="center",
                verticalalignment=v_align,
                annotation_clip=True,
                fontsize=base_font_size * 0.5,
                bbox=dict(facecolor="white", edgecolor="black", boxstyle="square"),
            )
            ax2.annotate(
                f"",
                xy=(
                    x_offset + (row.end_x - row.start_x) / 2 + row.start_x,
                    y_offset
                    + (row.end_y_count - row.start_y_count) / 2
                    + row.start_y_count,
                ),
                xycoords="data",
                xytext=xytextarrow,
                textcoords="offset points",
                arrowprops=dict(facecolor=plt_color, headwidth=8, headlength=5),
                horizontalalignment="center",
                verticalalignment=v_align,
                annotation_clip=True,
            )
        if row.plot_group == "L4B":
            ax.legend(
                loc="upper left",
                fontsize=base_font_size * 0.5,
                bbox_to_anchor=(0.01, 0.80),
            )
            if row.end_y != 0:
                ax2.set_ylim(
                    [
                        0,
                        math.floor(
                            round((row.end_y_count / row.end_y) * 100)
                            * ((cap + 1) / 100)
                        ),
                    ]
                )
            ax.set_title(
                f"{row.collection_code.replace(' | ', '-')}: {row.category.capitalize()}\n",
                color="black",
                fontsize=base_font_size * 1.25,
            )
            ax.set_xlabel(
                "\n\n\nTime Since Project Start (months)", fontsize=base_font_size
            )
            ax.set_ylabel(
                "Percentage Proposed\nCompleted (%)\n", fontsize=base_font_size
            )
            ax2.set_ylabel("\nCount Completed (unit)", fontsize=base_font_size)
            ax.annotate(
                "Project Start:\n Aug. 31, 2019",
                xy=(t_start, -8),
                xycoords="data",
                xytext=(0, -15),
                textcoords="offset points",
                arrowprops=dict(facecolor="grey", headwidth=8, headlength=5),
                horizontalalignment="center",
                verticalalignment="top",
                annotation_clip=False,
                fontsize=base_font_size * 0.66,
            )
            ax.annotate(
                "Present:\n Dec. 31, 2021",
                xy=(t_present + 0.1, -8),
                xycoords="data",
                xytext=(0, -15),
                textcoords="offset points",
                arrowprops=dict(facecolor="grey", headwidth=8, headlength=5),
                horizontalalignment="center",
                verticalalignment="top",
                annotation_clip=False,
                fontsize=base_font_size * 0.66,
            )
            ax.annotate(
                "Project End:\n Dec. 31, 2022",
                xy=(t_end + 0.1, -8),
                xycoords="data",
                xytext=(0, -15),
                textcoords="offset points",
                arrowprops=dict(facecolor="grey", headwidth=8, headlength=5),
                horizontalalignment="center",
                verticalalignment="top",
                annotation_clip=False,
                fontsize=base_font_size * 0.66,
            )
            ax.annotate(
                "Project Extension End:\n Dec. 31, 2023",
                xy=(t_extended + 0.1, -8),
                xycoords="data",
                xytext=(0, -15),
                textcoords="offset points",
                arrowprops=dict(facecolor="grey", headwidth=8, headlength=5),
                horizontalalignment="center",
                verticalalignment="top",
                annotation_clip=False,
                fontsize=base_font_size * 0.66,
            )
            output_directory = (
                f"{output_path}{row.collection_code.replace(' | ', '-')}/"
            )
            os.makedirs(output_directory, exist_ok=True)
            fig.savefig(f"{output_directory}{row.category}.png")
            fig.clf()
            plt.clf()
            plt.close()
    return
