import getpass
import requests
import json
from pandas.io.json import json_normalize
import pandas as pd
import re


def get_json(email_address):
    """
    Pulls fpl draft league data using an api call, and stores the output
    in a json file at the specified location.
    
    To get the FPL Draft api call, I followed advice on [Reddit here](https://www.reddit.com/r/FantasyPL/comments/9rclpj/python_for_fantasy_football_using_the_fpl_api/e8g6ur4?utm_source=share&utm_medium=web2x) which basically said you can derive the API calls by using Chrome's developer window under network you can see the "fetches" that are made, and the example response data. Very cool!
    
    :param file_path: The file path and name of the json file you wish to create
    :param api: The api call for your fpl draft league
    :param email_address: Your email address to authenticate with premierleague.com
    :returns: 
    """
    json_files = ['../data/transactions.json',
         '../data/elements.json',
         '../data/details.json',
         '../data/element_status.json'
                 ]
    
    apis = ['https://draft.premierleague.com/api/draft/league/38996/transactions',
       'https://draft.premierleague.com/api/bootstrap-static',
       'https://draft.premierleague.com/api/league/38996/details',
       'https://draft.premierleague.com/api/league/38996/element-status']
    
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
    
    # Loop over the api(s), call them and capture the response(s)
    for file, i in zip(json_files, apis):
        r = session.get(i)
        jsonResponse = r.json()
        with open(file, 'w') as outfile:
            json.dump(jsonResponse, outfile)
            

def get_data(df_name):
    
    # Dataframes from the details.json
    if df_name == 'league_entries':
        with open('../data/details.json') as json_data:
            d = json.load(json_data)
            league_entry_df = json_normalize(d['league_entries'])
            
        return league_entry_df
    
    elif df_name == 'matches':
        with open('../data/details.json') as json_data:
            d = json.load(json_data)
            matches_df = json_normalize(d['matches'])
            
        return matches_df
    
    elif df_name == 'standings':
        with open('../data/details.json') as json_data:
            d = json.load(json_data)
            standings_df = json_normalize(d['standings'])
            
        return standings_df
    
    # Dataframes from the elements.json
    elif df_name == 'elements':
        with open('../data/elements.json') as json_data:
            d = json.load(json_data)
            elements_df = json_normalize(d['elements'])
            
        return elements_df
    
    elif df_name == 'element_types':
        with open('../data/elements.json') as json_data:
            d = json.load(json_data)
            element_types_df = json_normalize(d['element_types'])
            
        return element_types_df
    
    # Dataframes from the transactions.json
    elif df_name == 'transactions':
        with open('../data/transactions.json') as json_data:
            d = json.load(json_data)
            transactions_df = json_normalize(d['transactions'])
            
        return transactions_df
    
    # Dataframes from the element_status.json
    elif df_name == 'element_status':
        with open('../data/element_status.json') as json_data:
            d = json.load(json_data)
            element_status_df = json_normalize(d['element_status'])
            
        return element_status_df
    
    
def get_team_players_agg_data():
    
    # Pull the required dataframes
    element_status_df = get_data('element_status')
    elements_df = get_data('elements')
    element_types_df = get_data('element_types')
    league_entry_df = get_data('league_entries')
    matches_df = get_data('matches')
    standings_df = get_data('standings')
    
    # Built the initial player -> team dataframe
    players_df = (pd.merge(element_status_df,
                           league_entry_df,
                           left_on='owner',
                           right_on='entry_id'
                        )
              .drop(columns=['in_accepted_trade',
                            'owner',
                            'status',
                            'entry_id',
                            'entry_name',
                            'id',
                            'joined_time',
                            'player_last_name',
                            'short_name',
                            'waiver_pick'])
              .rename(columns={'player_first_name':'team'})
             )
    
    # Get the element details
    players_df = pd.merge(players_df, elements_df, left_on='element', right_on='id')
    players_df = players_df[['team_x',
                             'element',
                             'web_name',
                             'total_points',
                             'goals_scored',
                             'goals_conceded',
                             'clean_sheets',
                             'assists',
                             'bonus',
                             'draft_rank',
                             'element_type',
                             'points_per_game',
                             'red_cards',
                             'yellow_cards'
                            ]]
    
    # Get the player types (GK, FWD etc.)
    players_df = (pd.merge(players_df,
                         element_types_df,
                         how='left',
                         left_on='element_type',
                         right_on='id')
                 .drop(columns=['id',
                                'plural_name_short',
                                'singular_name',
                                'singular_name_short'])
                )

    return players_df


def get_team_players_gw_data():
    
    df = get_team_players_agg_data()
    elements_to_pull = df['element']
    players_dict = {}
    
    for element in elements_to_pull:
        with open(f'../data/elements/{element}.json') as json_data:
            d = json.load(json_data)
            players_dict[element] = json_normalize(d['history'])
            players_df = pd.concat(players_dict, ignore_index=True)
            
    return players_df


def get_num_gameweeks():
    
    matches_df = get_data('matches')       
    num_gameweeks = matches_df[matches_df['finished'] == True]['event'].max()
    
    return num_gameweeks