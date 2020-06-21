import sys
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append("../") # Enables importing from parent directory
import fpl_draft_league as fpl
from fpl_draft_league import utils

def get_transactions_df(gameweek, accepted=True):
    """
    This takes in 3 separate dataframes and produces a cleaned transactions dataframe for consumption.
    
    :param entries_df: The dataframe containing all the league entries
    :param elements_df: The dataframe containing details of every premier league player
    :param accepted: Limit only to transfers that were accepted (as opposed to failed)
    :returns: dataframe with list of every transaction
    """
    
    entries_df = utils.get_data('league_entries')
    elements_df = utils.get_data('elements')
    transactions_df = utils.get_data('transactions')

    entries_df = entries_df[['entry_id', 'player_first_name']]
    elements_df = elements_df[['web_name', 'id']]
    transactions_df = transactions_df[['element_in', 'element_out', 'event', 'entry', 'result', 'kind']]
    transactions_df = transactions_df[transactions_df['event'] == gameweek]
    
    # Left join to get league player name
    df = (pd.merge(transactions_df,
              entries_df,
              how='left',
              left_on='entry',
              right_on='entry_id')
          .drop(columns=['entry', 'entry_id']))
    
    # Left join to get transfer in name 
    df = pd.merge(df,
              elements_df,
              how='left',
              left_on='element_in',
              right_on='id')
     
    # Left join to get transfer out name 
    df = pd.merge(df,
             elements_df,
             how='left',
             left_on='element_out',
             right_on='id')
    
    # Cleaning data
    df = (
        # Rename columns
        df.rename(
            columns={
                'player_first_name':'team',
                'web_name_x' : 'player_in',
                'web_name_y' : 'player_out',
                'id_x' : 'player_in_id',
                'id_y' : 'player_out_id',
            }
        )
        # Reorder columns
        [[
            'team',
            'event',
            'kind',
            'player_in',
            'player_in_id',
            'player_out',
            'player_out_id',
            'result'
        ]]
    )
    
    if accepted == True:
        df = df[df['result'] == 'a']
        
    return df




def get_trxn_rankings(df, accepted=True, event=None):
    """
    This takes in 3 separate dataframes and produces a cleaned transactions dataframe for consumption.
    
    :param df: The dataframe of transactions you wish to aggregate
    :returns: Dataframe listing players and count of transactions made, ordered descending
    """
    
    if accepted == True:
        df = df[df['result'] == 'a']
        
    if event:
        df = df[df['event'] == event]
    
    df = (df['team'].reset_index()
    .groupby('team')
    .count()
    .sort_values(by='index', ascending=False)
    .rename(columns={'index':'count'})
    )
    
    return df


def chart_trxn_vol(df):
    
    df = (df[['event', 'player_in']]
          .groupby('event')
          .count()
          .reset_index()
         )
    
    plt.figure()

    plt.bar(df['event'], df['player_in'])

    ax = plt.gca()

    ax.set_xticks(range(1, fpl.get_num_gameweeks()+1))
    ax.set_xticklabels(range(1, fpl.get_num_gameweeks()+1))
    ax.set_title('FPL Draft League - Transfer volume by gameweek')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.show()
    
    return df