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

# Other functions

def calculate_k_d(db, player_id):
    player_data = db[db['player_id'] == player_id]
    
    if player_data.empty:
        return 'Player not found in Database'
    else:

        total_kills = player_data['kills'].sum()
        total_deaths = player_data['deaths'].sum()
        return total_kills/total_deaths

def calculate_wins(db, player_id):
    player_data = db[db['player_id'] == player_id]
    
    if player_data.empty:
        return 'Player not found in Database'
    else:

        total_wins = player_data['win'].sum()
        return total_wins

def calculate_losses(db, player_id):
    player_data = db[db['player_id'] == player_id]
    
    if player_data.empty:
        return 'Player not found in Database'
    else:

        total_loss = player_data['loss'].sum()
        return total_loss

# Add Functions
def add_player(db, username):
    existing_ids = db['ID']
    
    if username in db['name'].values:
        print(f'{username} already exists!')
    
    else:

        if len(existing_ids) == 0:
            new_id = 'p0001'
        else:
            # Extract the numerical part, convert to int, find the max, and increment
            max_id_num = max(int(player_id[1:]) for player_id in existing_ids)
            new_id = f"p{max_id_num + 1:04d}"
        
        # Add the new player
        new_player = pd.Series({'ID': new_id, 'name': username})
        
        # Concatenate the new player row to the existing DataFrame
        players = pd.concat([db, new_player.to_frame().T], ignore_index=True)

        players.to_csv(players_path, index=False)

        print(f'{username} has been added!')

# Delete Functions
def delete_player(db, id, username):
    existing_users = db['name']
    existing_ids = db['ID']

    if username:
        if username not in existing_users.values:
            print(f'{username} does not exist!')
        else:
            # Filter out the player to be deleted
            new_players = db[db['name'] != username]
            
            # Check if the number of rows changed
            if new_players.shape[0] == db.shape[0]:
                print("Player not found, no deletion occurred.")
            else:
                print(f'{username} has been found and deleted.')
                new_players.to_csv(players_path, index=False)
    elif id:
        new_players = db[db['ID'] != id]
        if id not in existing_ids.values:
            print(f'User {id} does not exist!')
        else:
            print(f'User {id} has been found and deleted.')
            new_players.to_csv(players_path, index=False)

# View Functions
def view_player(db, id, username):

    if id == '' and username == '':
        print(db)
    elif id:
        player_info = db[db['ID'] == id]
        if player_info.empty:
            return 'Player could not be found!'
        else:
            return player_info
        
    elif username:
        player_info = db[db['name'] == username]
        
        if player_info.empty:
            return 'Player could not be found!'
        else:
            return player_info

# Main

roles = pd.read_csv(roles_path)
characters = pd.read_csv(characters_path)
players = pd.read_csv(players_path)
maps = pd.read_csv(maps_path)
gamemodes = pd.read_csv(gamemodes_path)
game_detail = pd.read_csv(gameDetail_path)

menu_1 = 0
while menu_1!= 4:
    print('Welcome to Marvels Rivals API\nSelect From Options Below:\n1. Add\n2. Delete\n3. View\n4. Exit')
    menu_1 = int(input('Enter ==> '))
    if menu_1 == 1:
        print('1. Add Player\n2. Add Role\n3. Add Character\n4. Add Map\n5. Add Mode\n6. Add Game Performance Detail')
        add_choice = int(input('Enter ==> '))
        if add_choice == 1:
            username = input('Enter New Player Username ==> ')
            add_player(db=players, username=username)
            pause = getpass.getpass('Hit Enter to Advance to Main Menu...')
        elif add_choice == 2:
            print()
        elif add_choice == 3:
            print()
        elif add_choice == 4:
            print()
        elif add_choice == 5:
            print()
        elif add_choice == 6:
            print()

    elif menu_1 == 2:
        print('1. Delete Player\n2. Delete Role\n3. Delete Character\n4. Delete Map\n5. Delete Mode\n6. Delete Game Performance Detail')
        delete_choice = int(input('Enter ==> '))
        if delete_choice == 1:
            print('1. Delete by Player ID\n2. Delete by Username')
            delete_choice = int(input('Enter == > '))
            if delete_choice == 1:
                id = input('Enter New Player ID ==> ')
                delete_player(db=players, id = id, username='')
            elif delete_choice == 2:
                username = input('Enter New Player Username ==> ')
                delete_player(db=players, id = '', username=username)
            pause = getpass.getpass('Hit Enter to Advance to Main Menu...')
        elif delete_choice == 2:
            print()
        elif delete_choice == 3:
            print()
        elif delete_choice == 4:
            print()
        elif delete_choice == 5:
            print()
        elif delete_choice == 6:
            print()

    elif menu_1 == 3:
        print('1. View Player\n2. View Role\n3. View Character\n4. View Map\n5. View Mode\n6. View Game Performance Detail')
        view_choice = int(input('Enter ==> '))
        if view_choice == 1:
            print('1. See All Players\n2. Lookup by Player ID\n3. Lookup by Username')
            player_view = int(input('Enter == > '))
            if player_view == 1:
                print(view_player(db=players, id='', username=''))
            elif player_view == 2:
                player_id = input('Enter Player ID ==>')
                print(view_player(db=players, id=player_id, username=''))
            elif player_view == 3:
                username = input('Enter Player Username ==>')
                print(view_player(db=players, id='', username=username))
            else:
                print('Invalid Option...\nReturning to Main Menu')
            pause = getpass.getpass('Hit Enter to Advance to Main Menu...')
            
        elif view_choice == 2:
            print()
        elif view_choice == 3:
            print()
        elif view_choice == 4:
            print()
        elif view_choice == 5:
            print()
        elif view_choice == 6:
            print()

    elif menu_1 == 4:
        print('Exiting...\nThank you for using our Marvels Rivals API!')

    roles = pd.read_csv(roles_path)
    characters = pd.read_csv(characters_path)
    players = pd.read_csv(players_path)
    maps = pd.read_csv(maps_path)
    gamemodes = pd.read_csv(gamemodes_path)
    game_detail = pd.read_csv(gameDetail_path)

    



