import getpass
import requests
import json
from pandas.io.json import json_normalize
import pandas as pd
from typing import List
import os
import re


def get_json(
        email_address: str,
        league_id: int,
        output_location: List[str],
        datasets: List[str] = ['all']
) -> None:
    """
    Pulls fpl draft league data, for the given league ID, and stores the output
    in a json file at the specified location.

    To get the FPL Draft api call, I followed advice on
    [Reddit here](https://www.reddit.com/r/FantasyPL/comments/9rclpj/python_for_fantasy_football_using_the_fpl_api/e8g6ur4?utm_source=share&utm_medium=web2x)
    which basically said you can derive the API calls by using Chrome's developer window under network you can see the
    "fetches" that are made, and the example response data. Very cool!
    
    :param email_address: Your email address login for premierleague.com
    :param league_id: Your FPL draft league ID
    :param output_location: The location you wish to output the .json file(s)
    :param datasets: The json datasets you want to pull from draft.premierleague.com. This defaults to 'all' which
        will pull all of the supported datasets. Alternatively you can specify a list of the specific dataset(s).
    """
    available_datasets = {
        'transactions': f'https://draft.premierleague.com/api/draft/league/{league_id}/transactions',
        'elements': f'https://draft.premierleague.com/api/bootstrap-static',
        'details': f'https://draft.premierleague.com/api/league/{league_id}/details',
        'element_status': f'https://draft.premierleague.com/api/league/{league_id}/element-status'
    }

    if datasets == ['all']:
        datasets = list(available_datasets.keys())
        print(datasets)

    # Check requested datasets are supported
    if not set(datasets).issubset(available_datasets.keys()):
        invalid_datasets = list(set(datasets) - set(available_datasets.keys()))
        raise ValueError(f"Invalid dataset(s). The following datasets are not supported: \n {invalid_datasets}")

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

    # Loop over the requested datasets, call their related API and capture the response
    for dataset in datasets:
        r = session.get(available_datasets[dataset])
        jsonResponse = r.json()
        with open(f'{output_location}/{dataset}.json', 'w') as outfile:
            json.dump(jsonResponse, outfile)
            print(f"written at {outfile}")

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
    
    
def get_player_data(email_address, elements):
    """
    Function to pull element gameweek data for a specified list of
    elements.
    
    :param email_address: The email address to authenticate with the fpl website.
    :param elements: The list of elements you wish to pull data for.
    
    :return:
    """
    pwd = getpass.getpass('Enter Password: ')
    
    for element in elements:
        
        # Create a separate .json file for an element
        json_files = [f"../data/elements/{str(element)}.json"]
        
        # Write the api call
        apis = [f"https://draft.premierleague.com/api/element-summary/{str(element)}"]

        # Post credentials for authentication
        pwd = pwd
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


def get_player_gameweek_data(elements, gameweek):
    """
    Pull gameweek data for a given list of elements/players
    
    :param elements: The list of elements/players you wish to obtain gameweek data for.
    :param gameweek: The gameweek you want the data limited to
    
    :return: Dataframe of gameweek data for each player
    """
    players_dict = {}
    
    # For each element we want to pull
    for element in elements:
        
        # Load the json data and put into players_df
        with open(f'../data/elements/{element}.json') as json_data:
            d = json.load(json_data)
            players_dict[element] = json_normalize(d['history'])
            players_df = pd.concat(players_dict, ignore_index=True)
            players_df = players_df[players_df['event'] == 28]
            
    return players_df