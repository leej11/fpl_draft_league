import getpass
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import datetime
import numpy as np



def get_points_over_time(matches_df, league_entry_df):
    # Filter to played matches
    utils
    
    matches_df = matches_df[matches_df['finished'] == True]

    # Join to get team names and player names of entry 1 (home team)
    matches_df = pd.merge(matches_df,
                          league_entry_df[['id', 'player_first_name']],
                          how='left',
                          left_on='league_entry_1',
                          right_on='id')

    # Join to get team names and player names of entry 2 (away team)
    matches_df = pd.merge(matches_df,
                          league_entry_df[['id', 'player_first_name']],
                          how='left',
                          left_on='league_entry_2',
                          right_on='id')

    # Drop unused columns, rename for clearer columns
    matches_df = (matches_df
                 .drop(['finished', 'started', 'id_x', 'id_y', 'league_entry_1', 'league_entry_2'], axis=1)
                .rename(columns={'event':'match',
                           'player_first_name_x': 'home_player',
                           'league_entry_1_points': 'home_score',
                           'player_first_name_y': 'away_player',
                           'league_entry_2_points': 'away_score',
                          })
                )
    
    def calc_points(df):
        if df['home_score'] == df['away_score']:
            df['home_points'] = 1
            df['away_points'] = 1
        elif df['home_score'] > df['away_score']:
            df['home_points'] = 3
            df['away_points'] = 0
        else:
            df['home_points'] = 0
            df['away_points'] = 3
        return df

    matches_df = matches_df.apply(calc_points, axis=1)
    
    home_df = matches_df[['match', 'home_player', 'home_score', 'home_points']]
    home_df = home_df.rename(columns={'home_player':'team', 'home_score':'score', 'home_points':'points'})

    away_df = matches_df[['match', 'away_player', 'away_score', 'away_points']]
    away_df = away_df.rename(columns={'away_player':'team', 'away_score':'score', 'away_points':'points'})

    matches_df_stacked = home_df.append(away_df)
    matches_df_stacked = matches_df_stacked.sort_values(by='match').reset_index().drop(['index'], axis=1)

    pivot_df = matches_df_stacked.pivot(index='match', columns='team', values=['points'])

    output_df = pivot_df.cumsum()
    
    # Plot the data
    
    plt.figure(figsize=[15,6])


    # for col in liam_df['points']:
    #     plt.plot(liam_df['points'][col], label=col)

    plt.plot(output_df['points']['Benji'], label='Benji', marker='o')
    plt.plot(output_df['points']['Cory'], label='Cory', marker='o')
    plt.plot(output_df['points']['Dave'], label='Dave', marker='o')
    plt.plot(output_df['points']['Huw'], label='Huw', marker='o')
    plt.plot(output_df['points']['James'], label='James', marker='o')

    plt.plot(output_df['points']['John'], label='John', marker='o')
    plt.plot(output_df['points']['Liam'], label='Liam', marker='o')
    plt.plot(output_df['points']['Rebecca'], label='Rebecca', marker='o')
    plt.plot(output_df['points']['Thomas'], label='Thomas', marker='o')
    plt.plot(output_df['points']['ben'], label='ben', marker='o')

    ax = plt.gca()

    ax.set_xticks(range(1, len(output_df) + 1, 1))
    ax.set_xticklabels(range(1, len(output_df) + 1, 1))
    ax.set_xlabel('Gameweek #')
    ax.set_ylabel('Points total')
    ax.set_title('FPL Draft League - Points over time')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.legend(loc=0)

    plt.show()
    
    return output_df, matches_df_stacked, pivot_df


def get_matches_stacked(matches_df, league_entry_df):
    
    # Limit to finished games only
    matches_df = matches_df[matches_df['finished'] == True]

    # Join to get team names and player names of entry 1 (home team)
    matches_df = pd.merge(matches_df,
                          league_entry_df[['id', 'player_first_name']],
                          how='left',
                          left_on='league_entry_1',
                          right_on='id')

    # Join to get team names and player names of entry 2 (away team)
    matches_df = pd.merge(matches_df,
                          league_entry_df[['id', 'player_first_name']],
                          how='left',
                          left_on='league_entry_2',
                          right_on='id')

    # Drop unused columns, rename for clearer columns
    matches_df = (matches_df
                 .drop(['finished', 'started', 'id_x', 'id_y', 'league_entry_1', 'league_entry_2'], axis=1)
                .rename(columns={'event':'match',
                           'player_first_name_x': 'home_player',
                           'league_entry_1_points': 'home_score',
                           'player_first_name_y': 'away_player',
                           'league_entry_2_points': 'away_score',
                          })
                )
    
    def calc_points(df):
        if df['home_score'] == df['away_score']:
            df['home_points'] = 1
            df['away_points'] = 1
        elif df['home_score'] > df['away_score']:
            df['home_points'] = 3
            df['away_points'] = 0
        else:
            df['home_points'] = 0
            df['away_points'] = 3
            
        df['home_margin'] = df['home_score'] - df['away_score']
        df['away_margin'] = df['away_score'] - df['home_score']
        
        return df

    matches_df = matches_df.apply(calc_points, axis=1)
    
    home_df = matches_df[['match', 'home_player', 'home_score', 'home_points', 'home_margin']]
    home_df = home_df.rename(columns={'home_player':'team', 'home_score':'score', 'home_points':'points', 'home_margin':'margin'})

    away_df = matches_df[['match', 'away_player', 'away_score', 'away_points', 'away_margin']]
    away_df = away_df.rename(columns={'away_player':'team', 'away_score':'score', 'away_points':'points', 'away_margin':'margin'})

    matches_df_stacked = home_df.append(away_df)
    matches_df_stacked = matches_df_stacked.sort_values(by='match').reset_index().drop(['index'], axis=1)
    
    return matches_df_stacked


def chart_margins_single(df, player):
    
    df = df[df['team'] == player]
    my_colour = np.where(df['margin']>0, '#00ff85', '#e90052')
    plt.figure(figsize=(10,6))

    plt.bar(df['match'], df['margin'], color=my_colour)

    ax = plt.gca()
    ax.set_xticks(range(1, len(df) + 1, 1))
    ax.set_yticks(range(-50,50,10))
    ax.set_xticklabels(range(1, len(df) + 1, 1))
    ax.set_xlabel('Gameweek #')
    ax.set_ylabel('Points margin')
    ax.set_title('Gameweek Points Margins')
    ax.grid(True, color='778899', alpha=0.1, axis='y')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

def chart_margins_multi(df, name_dict):
    
    fig1, ax = plt.subplots(3,3, figsize=(50,20), sharex='col', sharey='row')

    fig1.suptitle("Gameweek Margins by player", fontsize=30)

    counter = 0
    for i in range(3):
        for j in range(3):
            my_colour = np.where(df[df['team'] == name_dict[counter]]['margin']>0, '#00ff85', '#e90052')
            ax[i, j].bar(df[df['team'] == name_dict[counter]]['match'],
                         df[df['team'] == name_dict[counter]]['margin'],
                         color=my_colour
                        )
            ax[i,j].set_title(f"{name_dict[counter]}", fontsize=20)
            ax[i,j].set_xticks(range(1, len(df[df['team'] == name_dict[counter]]) + 1, 1))
            ax[i,j].set_yticks(range(-60,60,10))
            ax[i,j].set_xticklabels(range(1, len(df[df['team'] == name_dict[counter]]) + 1, 1),fontsize=10)
            ax[i,j].set_xlabel('Gameweek #',fontsize=15)
            ax[i,j].set_ylabel('Points margin',fontsize=15)
            ax[i,j].grid(True, color='778899', alpha=0.1, axis='y')
            ax[i,j].spines['right'].set_visible(False)
            ax[i,j].spines['top'].set_visible(False)

            counter += 1


def get_streaks(matches_df_stacked):
    
    df = matches_df_stacked
    
    def win_lose_bin(df):
        if df['points'] == 3:
            df['binary'] = 1
        elif df['points'] == 1:
            df['binary'] = 0
        elif df['points']==0:
            df['binary'] = -1
            
        return df
    
    df = (df.apply(win_lose_bin, axis=1)
          .sort_values(by=['team', 'match'])
         )
    
    teams_grpd = df.groupby('team')
    
    def get_team_streaks(group):
    
        grouper = (group.binary != group.binary.shift()).cumsum()
        group['streak'] = group['binary'].groupby(grouper).cumsum()
    
        return group
    
    df = teams_grpd.apply(get_team_streaks)
    
    return df



    