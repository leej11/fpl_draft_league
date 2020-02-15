import fpl_draft_league.utils as utils
import pandas as pd
import matplotlib.pyplot as plt

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

    plt.show()
    
    
def 