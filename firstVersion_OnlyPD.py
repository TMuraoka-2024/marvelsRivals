import pandas as pd
import numpy as np
import seaborn as sns
import getpass as getpass

roles_path = 'C:/Users/Trey Muraoka/Documents/Coding Projects/Marvels Rivals/Git/roles.csv'
characters_path = 'C:/Users/Trey Muraoka/Documents/Coding Projects/Marvels Rivals/Git/characters.csv'
players_path = 'C:/Users/Trey Muraoka/Documents/Coding Projects/Marvels Rivals/Git/players.csv'
maps_path = 'C:/Users/Trey Muraoka/Documents/Coding Projects/Marvels Rivals/Git/maps.csv'
gamemodes_path = 'C:/Users/Trey Muraoka/Documents/Coding Projects/Marvels Rivals/Git/gamemodes.csv'
gameDetail_path = 'C:/Users/Trey Muraoka/Documents/Coding Projects/Marvels Rivals/Git/gameDetails.csv'
playerstats_path = 'C:/Users/Trey Muraoka/Documents/Coding Projects/Marvels Rivals/Git/playerStats.csv'

roles = pd.read_csv(roles_path)
characters = pd.read_csv(characters_path)
players = pd.read_csv(players_path)
maps = pd.read_csv(maps_path)
gamemodes = pd.read_csv(gamemodes_path)
game_detail = pd.read_csv(gameDetail_path)
player_stats = pd.read_csv(playerstats_path)

def formattingPlayerStats(player_stats=player_stats, roles=roles, players=players):
    player_stats_view = player_stats
    id_to_name = dict(zip(players['ID'], players['name']))
    id_to_role = dict(zip(roles['ID'], roles['name']))
    player_stats_view['username'] = player_stats_view['player_id'].map(id_to_name)
    player_stats_view['role'] = player_stats_view['role_id'].map(id_to_role)
    
    player_stats_view['win/loss_pct'] = round(player_stats_view['wins']/player_stats_view['matches_played'], 2)
    player_stats_view['kills_per_game'] = round(player_stats_view['kills']/player_stats_view['matches_played'], 1)
    player_stats_view['solo_kills_per_game'] = round(player_stats_view['solo_kills']/player_stats_view['matches_played'], 1)
    player_stats_view['damage_per_game'] = round(player_stats_view['damage']/player_stats_view['matches_played'], 1)
    player_stats_view['damage_blocked_per_game'] = round(player_stats_view['damage_blocked']/player_stats_view['matches_played'], 1)
    player_stats_view['healing_per_game'] = round(player_stats_view['healing']/player_stats_view['matches_played'], 1)


    player_stats_view = player_stats_view[['username', 'role', 'kills', 'solo_kills', 
                                'assists', 'matches_played', 'kills_per_game',
                                'solo_kills_per_game','wins', 'win/loss_pct', 'damage', 'damage_per_game', 'damage_blocked', 
                                'damage_blocked_per_game', 'healing', 'healing_per_game']]
    
    numerical_columns = player_stats_view.columns[3:]
    
    for col in numerical_columns:
        player_stats_view[col] = player_stats_view[col].apply(lambda x: f"{x:,}")

    return player_stats_view

# Main

menu_1 = 0
while menu_1!= 2:
    print('Welcome to the Marvel Rivals API! Please select from the following options:\
          \n1. View Player Stats\n2. Exit')
    menu_1 = int(input('Enter ==> '))

    if menu_1 == 1:
        player_stats_view = formattingPlayerStats()
        print('Player Stats\nPlease select from the following options:\
          \n1. All Player Stats\n2. Lookup by Player ID\n3. Lookup by Player Username')
        
        menu_2 = int(input('Enter ==> '))
        if menu_2 == 1:
            print(player_stats_view)

        elif menu_2 == 2:
            ID = input('Enter Player ID ==> ')

            if ID in players['ID'].values:
                username = players[players['ID'] == ID]['name'].values[0]
                results = player_stats_view[player_stats_view['username'] == username]
                if results.empty:
                    print('No Stats')
                else:
                    print(results)

            else:
                print(f'Player ID {ID} not found')

        elif menu_2 == 3:
            username = input('Enter Player Username ==> ').strip().lower()

            clean_usernames = players['name'].str.strip().str.lower()

            if username in clean_usernames.values:
                results = player_stats_view[player_stats_view['username'].str.strip().str.lower() == username]
                if results.empty:
                    print('No Stats')
                else:
                    print(results)

            else:
                print(f'Player Username {username} not found')

        else:
            print('Invalid selection. Returning to Main Menu')

    elif menu_1 == 2:
        print('Thank you for using the Marvel Rivals API')

    pass