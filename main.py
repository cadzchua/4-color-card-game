# import json
# import pandas as pd
# from datetime import datetime

# def write_data_to_excel(players_data, win_history):
#     players_df = pd.DataFrame(players_data).transpose()
#     win_history_df = pd.DataFrame(win_history, columns=['Player', 'Amount'])

#     current_date = datetime.now().strftime("%d-%m-%Y")

#     with pd.ExcelWriter(f'四色牌.xlsx') as writer:
#         players_df.to_excel(writer, sheet_name=f'{current_date}_Game Data', index_label='Player')
#         win_history_df.to_excel(writer, sheet_name=f'{current_date}_Game Data', startcol=players_df.shape[1] + 3, index=False)

# def load_data(file_path):
#     try:
#         with open(file_path, 'r') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return {}
#     except json.JSONDecodeError:
#         print("Error decoding JSON. Starting with empty data.")
#         return {}

# def save_data(file_path, data):
#     with open(file_path, 'w') as file:
#         json.dump(data, file, indent=4)

# def clear_data_file(file_path):
#     with open(file_path, 'w') as file:
#         file.write("{}")  # Writing an empty dictionary to clear the file

# def clear_history_file(file_path):
#     with open(file_path, 'w') as file:
#         file.write("[]")  # Writing an empty list to clear the file

# def clear_all_data(data_file, history_file, players_data, win_history):
#     try:
#         write_data_to_excel(players_data, win_history)
#     except Exception as e:
#         print(f"An error occurred while writing data to Excel: {e}")
#         return
#     clear_data_file(data_file)
#     clear_history_file(history_file)
#     print("Data files cleared.")


# def deactivate_player(players_data, player_name):
#     if player_name in players_data:
#         players_data[player_name]['Active'] = False
#         print(f"Player {player_name} has left the game.")
#     else:
#         print(f"Player {player_name} is not in the game.")

# def add_player(players_data, player_name):
#     player_balance = float(input(f"Enter {player_name}'s balance: \n"))
#     players_data[player_name] = {
#         "Starting Balance": player_balance,
#         "Final Balance": player_balance,
#         "Net Balance": 0,
#         "Wins": 0,
#         "Active": True  
#     }
#     print(f"Player {player_name} has joined the game with balance {player_balance}.")

# def update_winner(players_data, player_winner, price, double, win_history):
#     active_players = {player: data for player, data in players_data.items() if data.get('Active', True)}
#     if player_winner in active_players:
#         players_data[player_winner]['Wins'] += 1
#         players_data[player_winner]['Final Balance'] = round(players_data[player_winner]['Final Balance'] + (len(active_players)-1)*(price*double), 2)
#         players_data[player_winner]['Net Balance'] = round(players_data[player_winner]['Final Balance'] - players_data[player_winner]['Starting Balance'], 2)
        
#         for player in active_players:
#             if player != player_winner:
#                 players_data[player]['Final Balance'] = round(players_data[player]['Final Balance'] - (price*double), 2)
#                 players_data[player]['Net Balance'] = round(players_data[player]['Final Balance'] - players_data[player]['Starting Balance'], 2)

#         win_history.append([player_winner, double*price])
#     else:
#         print(f"Player {player_winner} not found in the players data.")
    
# def undo_last_win(players_data, win_history, price):
#     if not win_history:
#         print("No win history to undo.")
#         return

#     last_winner, last_amount = win_history.pop()
#     double_value = last_amount / price
#     active_players = {player: data for player, data in players_data.items() if data.get('Active', True)}

#     players_data[last_winner]['Wins'] -= 1
#     players_data[last_winner]['Final Balance'] = round(players_data[last_winner]['Final Balance'] - (len(active_players) - 1) * price * double_value, 2)
#     players_data[last_winner]['Net Balance'] = round(players_data[last_winner]['Final Balance'] - players_data[last_winner]['Starting Balance'], 2)

#     for player in active_players:
#         if player != last_winner:
#             players_data[player]['Final Balance'] = round(players_data[player]['Final Balance'] + price * double_value, 2)
#             players_data[player]['Net Balance'] = round(players_data[player]['Final Balance'] - players_data[player]['Starting Balance'], 2)

#     print(f"Last win by {last_winner} for amount {last_amount} has been undone.")

# def main():
#     data_file = 'players_data.json'
#     history_file = 'win_history.json'
#     players_data = load_data(data_file)
#     win_history = load_data(history_file)  

#     if not isinstance(win_history, list):
#         win_history = []  

#     try:
#         num_of_players = int(input("Enter the number of players: \n"))  # Checking the number of players in the game
#     except ValueError:
#         print("Please enter a valid integer value.")
#         return

#     PRICE = 0.20  # Base price of 20c per game

#     for i in range(num_of_players):
#         player_name = input(f"Enter the Player {i + 1}'s name: \n")
#         player_balance = input(f"Enter the Player {i + 1}'s balance: \n")
#         while True:
#             try:
#                 player_balance = float(player_balance)
#                 break
#             except ValueError:
#                 print(f"Invalid balance for {player_name}.")
    
#         players_data[player_name] = {
#             "Starting Balance": player_balance,
#             "Final Balance": player_balance,
#             "Net Balance": 0,
#             "Wins": 0,
#             "Active": True
#         }

#     while True:
#         player_winner = input("Enter the name of the winning player ('exit' to finish or 'join'/'leave'): \n")
#         if player_winner.lower() == 'exit':
#             clear_data = input("Do you want to clear existing data files and save it to an excel file? (y/n): \n")
#             if clear_data.lower() == 'y' or clear_data.lower() == 'yes':
#                 clear_all_data(data_file, history_file, players_data, win_history)
#             break
        
#         elif player_winner.lower() == 'leave':
#             player_name = input("Enter the name of the player leaving: \n")
#             deactivate_player(players_data, player_name)
#             continue
#         elif player_winner.lower() == 'join':
#             player_name = input("Enter the name of the new player joining: \n")
#             add_player(players_data, player_name)
#             continue
#         elif player_winner.lower() == 'undo':
#             undo_last_win(players_data, win_history, PRICE)
#             save_data(data_file, players_data)
#             save_data(history_file, win_history)
#             continue

#         while True:
#             double = input("Did the winner get double? (y/n)\n").lower()
            
#             if double.lower() == "y" or double.lower() == "yes":
#                 double_value = 2
#                 break

#             elif double.lower() == "n" or double.lower() == "no":
#                 double_value = 1
#                 break

#         update_winner(players_data, player_winner, PRICE, double_value, win_history)
#         save_data(data_file, players_data)
#         save_data(history_file, win_history)

# if __name__ == "__main__":
#     main()