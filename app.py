from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load your data
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

def formattingPlayerStats():
    player_stats_view = player_stats.copy()
    id_to_name = dict(zip(players['ID'], players['name']))
    id_to_role = dict(zip(roles['ID'], roles['name']))
    player_stats_view['username'] = player_stats_view['player_id'].map(id_to_name)
    player_stats_view['role'] = player_stats_view['role_id'].map(id_to_role)
    
    player_stats_view['win/loss_pct'] = round(player_stats_view['wins'] / player_stats_view['matches_played'], 2)
    player_stats_view['kills_per_game'] = round(player_stats_view['kills'] / player_stats_view['matches_played'], 1)
    player_stats_view['solo_kills_per_game'] = round(player_stats_view['solo_kills'] / player_stats_view['matches_played'], 1)
    player_stats_view['damage_per_game'] = round(player_stats_view['damage'] / player_stats_view['matches_played'], 1)
    player_stats_view['damage_blocked_per_game'] = round(player_stats_view['damage_blocked'] / player_stats_view['matches_played'], 1)
    player_stats_view['healing_per_game'] = round(player_stats_view['healing'] / player_stats_view['matches_played'], 1)

    player_stats_view = player_stats_view[['username', 'role', 'kills', 'solo_kills', 
                                           'assists', 'matches_played', 'kills_per_game',
                                           'solo_kills_per_game', 'wins', 'win/loss_pct', 'damage', 
                                           'damage_per_game', 'damage_blocked', 'damage_blocked_per_game', 
                                           'healing', 'healing_per_game']]

    numerical_columns = player_stats_view.columns[3:]
    for col in numerical_columns:
        player_stats_view[col] = player_stats_view[col].apply(lambda x: f"{x:,}")

    return player_stats_view

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view_stats_menu')
def view_stats_menu():
    return render_template('view_stats_menu.html')

@app.route('/view_stats', methods=['GET', 'POST'])
def view_stats():
    player_stats_view = formattingPlayerStats()
    if request.method == 'POST':
        lookup_type = request.form.get('lookup_type')
        if lookup_type == 'id':
            player_id = request.form.get('player_id')
            if player_id in players['ID'].values:
                username = players[players['ID'] == player_id]['name'].values[0]
                results = player_stats_view[player_stats_view['username'] == username]
                if results.empty:
                    return render_template('view_stats_menu.html', message="No Stats Found", player_stats=None)
                return render_template('view_stats_menu.html', player_stats=results)
            else:
                return render_template('view_stats_menu.html', message="Player ID not found", player_stats=None)

        elif lookup_type == 'username':
            username = request.form.get('username').strip().lower()
            clean_usernames = players['name'].str.strip().str.lower()
            if username in clean_usernames.values:
                results = player_stats_view[player_stats_view['username'].str.strip().str.lower() == username]
                if results.empty:
                    return render_template('view_stats_menu.html', message="No Stats Found", player_stats=None)
                return render_template('view_stats_menu.html', player_stats=results)
            else:
                return render_template('view_stats_menu.html', message="Player Username not found", player_stats=None)

        elif lookup_type == 'all':
            if player_stats_view.empty:
                return render_template('view_stats_menu.html', message="No stats available", player_stats=None)
            return render_template('view_stats_menu.html', player_stats=player_stats_view)
    
    return render_template('view_stats_menu.html', player_stats=None)

if __name__ == '__main__':
    app.run(debug=True)