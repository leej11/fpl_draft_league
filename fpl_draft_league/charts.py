import fpl_draft_league.utils as utils
import fpl_draft_league.fpl_draft_league as fpl
import pandas as pd
import matplotlib.pyplot as plt
import os

def chart_league_standings_history():
    
    # Pull required data
    matches_df = utils.get_data('matches')
    matches_df = matches_df[matches_df['finished'] == True]
    league_entry_df = utils.get_data('league_entries')
    
    # Join to get team names
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
                          }))
    
                  
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

    
    plt.savefig(f"{os.environ['HOME']}/Documents/Github/fpl_draft_league/data/standings.png")
    #plt.show()

    
def chart_top_n_players(n=10):
    
    #### Pull in the needed data ####
    # Element status and filter to owned players only
    element_status_df = utils.get_data('element_status')
    element_status_df = element_status_df[element_status_df['status'] == 'o']
    element_status_df = element_status_df[['element', 'owner']]
    
    # League entries
    le_df = utils.get_data('league_entries')
    le_df = le_df[['player_first_name', 'entry_id']]
    
    # Join owner players with league entries (cleaning)
    owner_df = pd.merge(element_status_df, le_df, how='left', left_on='owner', right_on='entry_id')
    owner_df = owner_df.drop(columns=['owner', 'entry_id'])
    
    # Get the actual element data
    elements_df = utils.get_data('elements')
    elements_df = elements_df[['id', 'web_name']]
    
    # Intermediate player ownership df, merging owners with element details
    po_df = pd.merge(owner_df, elements_df, left_on='element', right_on='id')
    po_df = po_df.drop(columns=['id'])
    
    
    # Pull all the teams' players gameweek data
    df = utils.get_team_players_gw_data()
    
    # Limit to just the latest completed gameweek
    df = df[df['event'] == utils.get_num_gameweeks()]
   
    # Build the final players_df in the clean form we want
    players_df = pd.merge(df,
              po_df,
              how='left',
              left_on='element',
              right_on='element')

    players_df = players_df[['web_name', 'player_first_name', 'total_points', 'goals_scored', 'goals_conceded', 'assists', 'bonus']]
    
    # The final df we need :D filtered to specified top 'n'
    players_df = players_df.sort_values(by='total_points', ascending=False).head(n)
    
    # Get list of league entry players
    player_list = list(players_df['player_first_name'])
    
    # Plot!!
    colour_dict = {
        'Thomas': 
            {
                'color':'#04f5ff',
                'hatch':True
            },
        'Huw':
            {
                'color':'#e90052',
                'hatch':True
            },
        'Benji':
            {
                'color':'#00ff85',
                'hatch':True
            },
        'John':
            {
                'color':'#38003c',
                'hatch':True
            },
        'Dave':
            {
                'color':'#EAFF04',
                'hatch':True
            },
        'James':
            {
                'color':'#04f5ff',
                'hatch':False
            },
        'Rebecca':
            {
                'color':'#e90052',
                'hatch':False
            },
        'Cory':
            {
                'color':'#00ff85',
                'hatch':False
            },
        'Liam':
            {
                'color':'#38003c',
                'hatch':False
            },
        'ben':
            {
                'color':'#EAFF04',
                'hatch':False
            }
    }
    
    plt.figure(figsize=[10,5])

    mybar = plt.bar(range(10),
            players_df['total_points'],
            tick_label=players_df['web_name']
            )

    for i, player in zip(range(10), player_list):
        mybar[i].set_color(colour_dict[player]['color'])
        mybar[i].set_label(player)


        if colour_dict[player]['hatch'] == True:
            mybar.patches[i].set_hatch('..')
            mybar.patches[i].set_edgecolor('white')
            mybar.patches[i].set_facecolor(colour_dict[player]['color'])

    ax = plt.gca()
    ax.legend()
    plt.xticks(rotation=80)
    
    plt.savefig(f"{os.environ['HOME']}/Documents/Github/fpl_draft_league/data/topnplayers.png")
    #plt.show()


def chart_current_streaks():
    
    league_entry_df = utils.get_data('league_entries')
    matches_df = utils.get_data('matches')
    stacked_df = fpl.get_matches_stacked(matches_df, league_entry_df)
    streaks_df = fpl.get_streaks(stacked_df)
    
    final_df = streaks_df[streaks_df['match'] == streaks_df.match.max()].sort_values(by='streak', ascending=False)[['team', 'streak']]
    final_df = final_df.sort_values(by='streak', ascending=True)
    
    # Setup the colours to apply
    colors = []

    for team in final_df['team']:
        if final_df[final_df['team'] == team]['streak'].values < 0:
            colors.append('#e90052')

        elif final_df[final_df['team'] == team]['streak'].values > 0:
            colors.append('#00ff85')
    
    # Build the plot
    plt.figure()
    plt.barh(range(10), final_df['streak'], color=colors)
    ax = plt.gca()
    
    ax.set_xlabel('Current Streak Value')
    ax.set_title('Current Team Streaks')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    ax.set_yticks(range(10))
    ax.set_yticklabels(final_df['team'], va='center')
    
    plt.savefig(f"{os.environ['HOME']}/Documents/Github/fpl_draft_league/data/streaks.png")
    #plt.show()