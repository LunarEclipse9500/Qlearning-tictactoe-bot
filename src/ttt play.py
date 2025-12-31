import json
board=[0, 0, 0, 0, 0, 0, 0, 0, 0]
winning_combinations=[[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
dict_player={1: 'X', -1: 'O'}
current_player=1

#getting the policy for ai in a dictionary
with open('ttt_policy.json', 'r') as f:
    policy=json.load(f)

def choose_symbol():
    global human_player, ai_player
    symbol = input("Choose your symbol (X/O): ").strip().upper()
    if symbol == 'X':
        human_player = 1
        ai_player = -1
    elif symbol == 'O':
        human_player = -1
        ai_player = 1
    else:
        print("Invalid symbol. Defaulting to X.")
        human_player = 1
        ai_player = -1 

def make_move(index):
    global current_player
    if board[index] != 0:
        print("Invalid move. Try again.")
        return board
    board[index]=current_player
    current_player*=-1
    return board

def reset():
    global board, current_player
    board=[0, 0, 0, 0, 0, 0, 0, 0, 0]
    current_player=1
    
def check_winner(board):
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
            if board[combo[0]] == human_player:
                print("Congratulations! You win!")
            elif board[combo[0]] == ai_player:
                print("My AI is better, You lose!")
            return board[combo[0]]   # 1 or -1

    if 0 not in board:
        print("It's a draw!")
        return 0   # draw

    return None    # game still going


def print_board():
    symbols = [dict_player.get(cell, ' ') for cell in board]
    print(f"{symbols[0]} | {symbols[1]} | {symbols[2]}")
    print("--+---+--")
    print(f"{symbols[3]} | {symbols[4]} | {symbols[5]}")
    print("--+---+--")
    print(f"{symbols[6]} | {symbols[7]} | {symbols[8]}")

def game():
    choose_symbol()
    reset()
    while True:
        if current_player == human_player:
            move = int(input("Enter your move (0-8): "))
            make_move(move)
        else:
            state_key = str(tuple(board))
            if state_key in policy:
                move = int(policy[state_key])
            # else:
            #     move = random.choice([i for i in range(9) if board[i] == 0])
            print(f"AI chooses move: {move}")
            make_move(move)

        print_board()
        if check_winner(board)!=None:
            game()
            break

game()