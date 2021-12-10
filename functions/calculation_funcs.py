import pandas as pd
import numpy as np


def create_percentages(df: pd.DataFrame):
    df['perc_done'] = 100 * (df['reported'] / df['proposed'])
    df_out = df.replace(np.nan, 0)
    return df_out


def calculate_statistics(df: pd.DataFrame,
                         t_start=0,
                         t_present=28,
                         t_end=36,
                         t_extended=48,
                         checkpoint_completion=60):
    # TODO: capture actual counts in addition to percentages for later plotting
    df_out = pd.DataFrame()
    for idx, row in df.iterrows():
        # define important values
        perc_end = 100
        perc_starting = row.perc_done
        if perc_starting > 100:
            perc_starting = 120  # to avoid plotting graphics errors
        perc_remaining = perc_end - perc_starting
        checkpoint = checkpoint_completion
        if perc_remaining <= 0:
            perc_end = perc_starting
            perc_remaining = 0
            perc_remaining_to_checkpoint = 0
            perc_checkpoint_to_complete = 0
            checkpoint = perc_end
        else:
            perc_remaining_to_checkpoint = checkpoint - row.perc_done
            perc_checkpoint_to_complete = 100 - perc_remaining_to_checkpoint
        current_rate = row.perc_done / (t_present - t_start)
        l2_future_rate = perc_remaining / (t_end - t_present)
        l3_future_rate = perc_remaining / (t_extended - t_present)
        l4a_future_rate = perc_remaining_to_checkpoint / (t_end - t_present)
        l4b_future_rate = perc_checkpoint_to_complete / (t_extended - t_end)
        l5_future_rate = perc_remaining_to_checkpoint / (t_extended - t_present)
        if current_rate != 0:
            l2_fold = l2_future_rate / current_rate
            l3_fold = l3_future_rate / current_rate
            l4a_fold = l4a_future_rate / current_rate
            l4b_fold = l4b_future_rate / current_rate
            l5_fold = l5_future_rate / current_rate
        else:
            l2_fold = 1
            l3_fold = 1
            l4a_fold = 1
            l4b_fold = 1
            l5_fold = 1
        # calculate Line 1 ("L1") segment
        l1 = {'collection_name': row.collection_name,
              'collection_code': row.collection_code,
              'category': row.type,
              'start_x': t_start,
              'end_x': t_present,
              'start_y': 0,
              'end_y': perc_starting,
              'rate': current_rate,
              'fold_increase': 1,
              'plot_group': 'L1'}
        # calculate Line 2 ("L2") segment
        l2 = {'collection_name': row.collection_name,
              'collection_code': row.collection_code,
              'category': row.type,
              'start_x': t_present,
              'end_x': t_end,
              'start_y': perc_starting,
              'end_y': perc_end,
              'rate': l2_future_rate,
              'fold_increase': l2_fold,
              'plot_group': 'L2'}
        # calculate Line 3 ("L3") segment
        l3 = {'collection_name': row.collection_name,
              'collection_code': row.collection_code,
              'category': row.type,
              'start_x': t_present,
              'end_x': t_extended,
              'start_y': perc_starting,
              'end_y': perc_end,
              'rate': l3_future_rate,
              'fold_increase': l3_fold,
              'plot_group': 'L3'}
        # calculate Line 4A ("L4A") segment
        l4a = {'collection_name': row.collection_name,
               'collection_code': row.collection_code,
               'category': row.type,
               'start_x': t_present,
               'end_x': t_end,
               'start_y': perc_starting,
               'end_y': checkpoint,
               'rate': l4a_future_rate,
               'fold_increase': l4a_fold,
               'plot_group': 'L4'}
        # calculate Line 4B ("L4B") segment
        l4b = {'collection_name': row.collection_name,
               'collection_code': row.collection_code,
               'category': row.type,
               'start_x': t_end,
               'end_x': t_extended,
               'start_y': checkpoint,
               'end_y': perc_end,
               'rate': l4b_future_rate,
               'fold_increase': l4b_fold,
               'plot_group': 'L4'}
        # calculate Line 5 ("L5") segment
        l5 = {'collection_name': row.collection_name,
              'collection_code': row.collection_code,
              'category': row.type,
              'start_x': t_present,
              'end_x': t_extended,
              'start_y': perc_starting,
              'end_y': perc_end,
              'rate': l5_future_rate,
              'fold_increase': l5_fold,
              'plot_group': 'L5'}
        df_out = df_out.append(l1, ignore_index=True)
        df_out = df_out.append(l2, ignore_index=True)
        df_out = df_out.append(l3, ignore_index=True)
        df_out = df_out.append(l4a, ignore_index=True)
        df_out = df_out.append(l4b, ignore_index=True)
        df_out = df_out.append(l5, ignore_index=True)
    df_out = df_out.sort_values(['collection_name', 'category', 'plot_group'])
    return df_out
