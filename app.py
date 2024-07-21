from flask import Flask, send_from_directory, request, jsonify, render_template
import json
import pandas as pd
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins="*")

data_file = 'players_data.json'
history_file = 'win_history.json'
PRICE = 0.20

def write_data_to_excel(players_data, win_history):
    players_df = pd.DataFrame(players_data).transpose()
    win_history_df = pd.DataFrame(win_history, columns=['Player', 'Amount'])

    current_date = datetime.now().strftime("%d-%m-%Y")
    try: 
        with pd.ExcelWriter('四色牌.xlsx', mode="a", engine="openpyxl", if_sheet_exists='overlay') as writer:
            players_df.to_excel(writer, sheet_name=f'{current_date}_Game Data', index_label='Player')
            win_history_df.to_excel(writer, sheet_name=f'{current_date}_Game Data', startcol=players_df.shape[1] + 3, index=False)
    except FileNotFoundError:
        with pd.ExcelWriter('四色牌.xlsx', mode="w", engine="openpyxl") as writer:
            players_df.to_excel(writer, sheet_name=f'{current_date}_Game Data', index_label='Player')
            win_history_df.to_excel(writer, sheet_name=f'{current_date}_Game Data', startcol=players_df.shape[1] + 3, index=False)

def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON. Starting with empty data.")
        return {}

def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def clear_data_file(file_path):
    with open(file_path, 'w') as file:
        file.write("{}")  # Writing an empty dictionary to clear the file

def clear_history_file(file_path):
    with open(file_path, 'w') as file:
        file.write("[]")  # Writing an empty list to clear the file

def clear_all_data(data_file, history_file, players_data, win_history):
    try:
        write_data_to_excel(players_data, win_history)
    except Exception as e:
        print(f"An error occurred while writing data to Excel: {e}")
        return
    clear_data_file(data_file)
    clear_history_file(history_file)
    print("Data files cleared.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_players', methods=['GET'])
def get_players():
    players_data = load_data(data_file)
    return jsonify(players_data)

@app.route('/get_history', methods=['GET'])
def get_history():
    win_history = load_data(history_file)
    return jsonify(win_history)

@app.route('/add_player', methods=['POST'])
def add_player():
    data = request.json
    player_name = data.get('name')
    player_balance = data.get('balance')
    players_data = load_data(data_file)
    if player_name and player_balance is not None:
        players_data[player_name] = {
            "Starting Balance": player_balance,
            "Final Balance": player_balance,
            "Net Balance": 0,
            "Single Wins": 0,
            "Double Wins": 0,
            "Total Wins": 0,
            "Active": True
        }
        save_data(data_file, players_data)
        return jsonify({"status": "Player added"}), 201
    return jsonify({"error": "Invalid input"}), 400

@app.route('/update_winner', methods=['POST'])
def update_winner():
    data = request.json
    player_winner = data.get('winner')
    double_value = data.get('double')
    players_data = load_data(data_file)
    win_history = load_data(history_file)
    if not isinstance(win_history, list):
        win_history = []
    active_players = {player: data for player, data in players_data.items() if data.get('Active', True)}
    if player_winner in active_players:
        if double_value == 2:
            players_data[player_winner]['Double Wins'] += 1
        else: 
            players_data[player_winner]['Single Wins'] += 1
        players_data[player_winner]['Total Wins'] += 1
        players_data[player_winner]['Final Balance'] = round(players_data[player_winner]['Final Balance'] + (len(active_players) - 1) * (PRICE * double_value), 2)
        players_data[player_winner]['Net Balance'] = round(players_data[player_winner]['Final Balance'] - players_data[player_winner]['Starting Balance'], 2)
        for player in active_players:
            if player != player_winner:
                players_data[player]['Final Balance'] = round(players_data[player]['Final Balance'] - (PRICE * double_value), 2)
                players_data[player]['Net Balance'] = round(players_data[player]['Final Balance'] - players_data[player]['Starting Balance'], 2)
        win_history.append([player_winner, double_value * PRICE])
        save_data(data_file, players_data)
        save_data(history_file, win_history)
        return jsonify({"status": "Winner updated"}), 200
    else:
        return jsonify({"error": "Player not found or is inactive."}), 404

@app.route('/clear_data', methods=['POST'])
def clear_data():
    players_data = load_data(data_file)
    win_history = load_data(history_file)
    clear_all_data(data_file, history_file, players_data, win_history)
    return jsonify({"status": "Data cleared and saved to Excel"}), 200

@app.route('/deactivate_player', methods=['POST'])
def deactivate_player():
    data = request.json
    player_name = data.get('name')
    players_data = load_data(data_file)
    if player_name in players_data:
        players_data[player_name]['Active'] = False
        save_data(data_file, players_data)
        return jsonify({"status": f"Player {player_name} has left the game."}), 200
    return jsonify({"error": f"Player {player_name} is not in the game."}), 404

@app.route('/activate_player', methods=['POST'])
def activate_player():
    data = request.json
    player_name = data.get('name')
    players_data = load_data(data_file)
    if player_name in players_data:
        players_data[player_name]['Active'] = True
        save_data(data_file, players_data)
        return jsonify({"status": f"Player {player_name} has joined the game."}), 200
    return jsonify({"error": f"Player {player_name} is not in the game."}), 404

@app.route('/undo_last_win', methods=['POST'])
def undo_last_win():
    players_data = load_data(data_file)
    win_history = load_data(history_file)
    if not win_history:
        return jsonify({"error": "No win history to undo."}), 400

    last_winner, last_amount = win_history.pop()
    double_value = last_amount / PRICE
    active_players = {player: data for player, data in players_data.items() if data.get('Active', True)}

    players_data[last_winner]['Total Wins'] -= 1
    if double_value == 2:
        players_data[last_winner]['Double Wins'] -= 1
    else:
        players_data[last_winner]['Single Wins'] -= 1
    players_data[last_winner]['Final Balance'] = round(players_data[last_winner]['Final Balance'] - (len(active_players) - 1) * PRICE * double_value, 2)
    players_data[last_winner]['Net Balance'] = round(players_data[last_winner]['Final Balance'] - players_data[last_winner]['Starting Balance'], 2)

    for player in active_players:
        if player != last_winner:
            players_data[player]['Final Balance'] = round(players_data[player]['Final Balance'] + PRICE * double_value, 2)
            players_data[player]['Net Balance'] = round(players_data[player]['Final Balance'] - players_data[player]['Starting Balance'], 2)

    save_data(data_file, players_data)
    save_data(history_file, win_history)
    return jsonify({"status": f"Last win by {last_winner} for amount {last_amount} has been undone."}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
