import getpass
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import datetime


def get_json(json_file, api, email_address):
    """
    Pulls fpl draft league data using an api call, and stores the output
    in a json file at the specified location.
    
    To get the FPL Draft api call, I followed advice on [Reddit here](https://www.reddit.com/r/FantasyPL/comments/9rclpj/python_for_fantasy_football_using_the_fpl_api/e8g6ur4?utm_source=share&utm_medium=web2x) which basically said you can derive the API calls by using Chrome's developer window under network you can see the "fetches" that are made, and the example response data. Very cool!
    
    :param file_path: The file path and name of the json file you wish to create
    :param api: The api call for your fpl draft league
    :param email_address: Your email address to authenticate with premierleague.com
    :returns: 
    """
    
    # Post credentials for authentication
    pwd = getpass.getpass('Enter Password: ')
    session = requests.session()
    url = 'https://users.premierleague.com/accounts/login/'
    payload = {
     'password': pwd,
     'login': email_address,
     'redirect_uri': 'https://fantasy.premierleague.com/a/login',
     'app': 'plfpl-web'
    }
    session.post(url, data=payload)
    
    # Call the api and capture the response
    r = session.get(api)
    jsonResponse = r.json()
    with open(json_file, 'w') as outfile:
        json.dump(jsonResponse, outfile)



# Function to convert the json file into 3 respective dataframes
def get_dataframes(json_file):
    """
    Converts a json file of fpl draft league data and converts
    into 3 respective dataframes for league entries, matches and current standings.
    
    :param json_file: The json file which contains the fpl draft league data#
    :returns: league entries dataframe, matches dataframe and current standings dataframe
    """
    
    with open(json_file) as json_data:
        d = json.load(json_data)
        league_entry_df = json_normalize(d['league_entries'])
        matches_df = json_normalize(d['matches'])
        standings_df = json_normalize(d['standings'])
    
    return league_entry_df, matches_df, standings_df



def get_points_over_time(matches_df, league_entry_df):
    # Filter to played matches
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


def get_num_gameweeks():
    
    start_date = datetime.date(2019,8,16)
    
    with open('details.json') as json_data:
        d = json.load(json_data)
        matches_df = json_normalize(d['matches'])
        
    num_gameweeks = matches_df[matches_df['started'] == True]['event'].max()
    
    return num_gameweeks
    