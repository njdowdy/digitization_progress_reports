import pandas as pd
import numpy as np


def create_percentages(df: pd.DataFrame):
    df["perc_done"] = 100 * (df["reported"] / df["proposed"])
    df_out = df.replace(np.nan, 0)
    return df_out


def calculate_statistics(
    df: pd.DataFrame,
    t_start=0,
    t_present=28,
    t_end=36,
    t_extended=48,
    checkpoint_completion=60,
):
    df_out = pd.DataFrame()
    for idx, row in df.iterrows():
        # define important values
        count_end = row.proposed
        if count_end == 0:  # skip all if count_end == 0
            perc_end = 0
            perc_starting = 0
            perc_remaining = 0
            checkpoint_perc = 0
            perc_remaining_to_checkpoint = 0
            perc_checkpoint_to_complete = 0
            count_starting = 0
            count_remaining = 0
            checkpoint_count = 0
            count_remaining_to_checkpoint = 0
            count_checkpoint_to_complete = 0
        else:
            perc_end = 100
            perc_starting = row.perc_done
            count_starting = row.reported
            # cap starting value at 120% to avoid graphical errors
            if perc_starting > 120:
                cap = 120
                perc_starting = cap
                count_starting = row.proposed * (cap / 100)
            # calculate remaining effort until completion
            perc_remaining = perc_end - perc_starting
            count_remaining = count_end - count_starting
            # calculate remaining effort until checkpoint
            if (
                checkpoint_completion < perc_starting
            ):  # if checkpoint value is less than starting value
                # checkpoint at midpoint to completion (converge on L3)
                checkpoint_perc = (perc_remaining / 2) + perc_starting
                checkpoint_count = count_end * (checkpoint_perc / 100)
            else:  # starting value is equal to or greater than checkpoint value
                # checkpoint at 60% completion
                checkpoint_perc = checkpoint_completion
                checkpoint_count = count_end * (checkpoint_completion / 100)
            # set values for remaining effort if project complete at t_present
            if perc_remaining <= 0:
                perc_end = perc_starting
                count_end = count_starting
                perc_remaining = 0
                count_remaining = 0
                perc_remaining_to_checkpoint = 0
                count_remaining_to_checkpoint = 0
                perc_checkpoint_to_complete = 0
                count_checkpoint_to_complete = 0
                checkpoint_perc = perc_end
                checkpoint_count = count_end
            # set values for remaining effort if project not complete at t_present
            else:
                perc_remaining_to_checkpoint = checkpoint_perc - perc_starting
                count_remaining_to_checkpoint = checkpoint_count - count_starting
                perc_checkpoint_to_complete = 100 - checkpoint_perc
                count_checkpoint_to_complete = count_end - checkpoint_count
        # define date ranges
        t0_t1 = t_present - t_start
        t1_t2 = t_end - t_present
        t1_t3 = t_extended - t_present
        t2_t3 = t_extended - t_end
        # calculate rates (in percentages)
        current_rate = perc_starting / t0_t1
        l2_future_rate = perc_remaining / t1_t2
        l3_future_rate = perc_remaining / t1_t3
        l4a_future_rate = perc_remaining_to_checkpoint / t1_t2
        l4b_future_rate = perc_checkpoint_to_complete / t2_t3
        # calculate rates (in counts)
        current_rate_count = count_starting / t0_t1
        l2_future_rate_count = count_remaining / t1_t2
        l3_future_rate_count = count_remaining / t1_t3
        l4a_future_rate_count = count_remaining_to_checkpoint / t1_t2
        l4b_future_rate_count = count_checkpoint_to_complete / t2_t3
        # calculate fold changes (covers both percentages and counts)
        if current_rate != 0:
            l2_fold = l2_future_rate / current_rate
            l3_fold = l3_future_rate / current_rate
            l4a_fold = l4a_future_rate / current_rate
            l4b_fold = l4b_future_rate / current_rate
        else:  # set fold changes to 1x (otherwise values are infinite)
            l2_fold = 1
            l3_fold = 1
            l4a_fold = 1
            l4b_fold = 1
        # calculate Line 1 ("L1") segment
        # L1: Project Start to Present
        l1 = {
            "collection_name": row.collection_name,
            "collection_code": row.collection_code,
            "category": row.type,
            "start_x": t_start,
            "end_x": t_present,
            "start_y": 0,
            "start_y_count": 0,
            "end_y": perc_starting,
            "end_y_count": count_starting,
            "rate": current_rate,
            "rate_count": current_rate_count,
            "fold_increase": 1,
            "plot_group": "L1",
        }
        # calculate Line 2 ("L2") segment
        # L2: Present to Project End
        l2 = {
            "collection_name": row.collection_name,
            "collection_code": row.collection_code,
            "category": row.type,
            "start_x": t_present,
            "end_x": t_end,
            "start_y": perc_starting,
            "start_y_count": count_starting,
            "end_y": perc_end,
            "end_y_count": count_end,
            "rate": l2_future_rate,
            "rate_count": l2_future_rate_count,
            "fold_increase": l2_fold,
            "plot_group": "L2",
        }
        # calculate Line 3 ("L3") segment
        # L3: Present to Project Extension End
        l3 = {
            "collection_name": row.collection_name,
            "collection_code": row.collection_code,
            "category": row.type,
            "start_x": t_present,
            "end_x": t_extended,
            "start_y": perc_starting,
            "start_y_count": count_starting,
            "end_y": perc_end,
            "end_y_count": count_end,
            "rate": l3_future_rate,
            "rate_count": l3_future_rate_count,
            "fold_increase": l3_fold,
            "plot_group": "L3",
        }
        # calculate Line 4A ("L4A") segment
        # L4a: Present to Checkpoint (Project End)
        l4a = {
            "collection_name": row.collection_name,
            "collection_code": row.collection_code,
            "category": row.type,
            "start_x": t_present,
            "end_x": t_end,
            "start_y": perc_starting,
            "start_y_count": count_starting,
            "end_y": checkpoint_perc,
            "end_y_count": checkpoint_count,
            "rate": l4a_future_rate,
            "rate_count": l4a_future_rate_count,
            "fold_increase": l4a_fold,
            "plot_group": "L4A",
        }
        # calculate Line 4B ("L4B") segment
        # L4a: Checkpoint (Project End) to Project Extension End
        l4b = {
            "collection_name": row.collection_name,
            "collection_code": row.collection_code,
            "category": row.type,
            "start_x": t_end,
            "end_x": t_extended,
            "start_y": checkpoint_perc,
            "start_y_count": checkpoint_count,
            "end_y": perc_end,
            "end_y_count": count_end,
            "rate": l4b_future_rate,
            "rate_count": l4b_future_rate_count,
            "fold_increase": l4b_fold,
            "plot_group": "L4B",
        }
        # write out data
        df_out = df_out.append(l1, ignore_index=True)
        df_out = df_out.append(l2, ignore_index=True)
        df_out = df_out.append(l3, ignore_index=True)
        df_out = df_out.append(l4a, ignore_index=True)
        df_out = df_out.append(l4b, ignore_index=True)
    df_out = df_out.sort_values(
        ["collection_name", "category", "plot_group"]
    )  # sort data for proper plotting
    return df_out
