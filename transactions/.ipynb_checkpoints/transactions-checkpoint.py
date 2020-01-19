import sys
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append("../") # Enables importing from parent directory
import fpl_draft_league as fpl

def get_transactions_df(entries_df, elements_df, transactions_df, accepted=True):
    """
    This takes in 3 separate dataframes and produces a cleaned transactions dataframe for consumption.
    
    :param entries_df: The dataframe containing all the league entries
    :param elements_df: The dataframe containing details of every premier league player
    :param accepted: Limit only to transfers that were accepted (as opposed to failed)
    :returns: dataframe with list of every transaction
    """
    
    entries_df = entries_df[['entry_id', 'player_first_name']]
    elements_df = elements_df[['id', 'first_name', 'second_name']]
    transactions_df = transactions_df
    
    # Left join to get league player name
    df = pd.merge(transactions_df,
              entries_df,
              how='left',
              left_on='entry',
              right_on='entry_id')
    
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
    df['player_in'] = df['first_name_x'] + ' ' + df['second_name_x']
    df['player_out'] = df['first_name_y'] + ' ' + df['second_name_y']
    
    df = df.drop(['first_name_x',
         'first_name_y',
         'second_name_x',
         'second_name_y',
         'id', 'id_y',
         'entry_id',
         'entry',
         'element_in',
         'element_out',
         'id_x',], axis=1)
    
    df['added'] = df['added'].str[:10]
    
    if accepted == True:
        df = df[df['result'] == 'a']
        
    return df


def get_trxn_rankings(df, accepted=True):
    """
    This takes in 3 separate dataframes and produces a cleaned transactions dataframe for consumption.
    
    :param df: The dataframe of transactions you wish to aggregate
    :returns: Dataframe listing players and count of transactions made, ordered descending
    """
    
    if accepted == True:
        df = df[df['result'] == 'a']
    
    df = (df['player_first_name'].reset_index()
    .groupby('player_first_name')
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