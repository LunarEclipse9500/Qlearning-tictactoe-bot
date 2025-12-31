import random
import json
board=[0, 0, 0, 0, 0, 0, 0, 0, 0]
winning_combinations=[[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
dict_player={1: 'X', -1: 'O'}
current_player=1
AI_PLAYER = -1
Q = {}

def make_move(index):
    global current_player
    if board[index] != 0:
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
            return board[combo[0]]   # 1 or -1

    if 0 not in board:
        return 0   # draw

    return None    # game still going


def print_board():
    symbols = [dict_player.get(cell, ' ') for cell in board]
    print(f"{symbols[0]} | {symbols[1]} | {symbols[2]}")
    print("--+---+--")
    print(f"{symbols[3]} | {symbols[4]} | {symbols[5]}")
    print("--+---+--")
    print(f"{symbols[6]} | {symbols[7]} | {symbols[8]}")

def valid_actions(state):
    return [i for i in range(9) if state[i] == 0]

def get_reward(winner):
    if winner == AI_PLAYER:   # AI wins
        return 1.0
    elif winner == -AI_PLAYER:  # AI loses
        return -1.0
    else:              # draw
        return 0.3

def choose_action(state, epsilon=0.1):
    actions = valid_actions(state)

    if random.random() < epsilon:
        return random.choice(actions)

    q_values = [Q.get((state, a), 0) for a in actions]
    max_q = max(q_values)
    best_actions = [a for a, q in zip(actions, q_values) if q == max_q]
    return random.choice(best_actions)

def update_q(state, action, reward, next_state, alpha=0.1, gamma=0.9):
    old_q = Q.get((state, action), 0)

    future_q = 0
    next_actions = valid_actions(next_state)
    if next_actions:
        future_q = max(Q.get((next_state, a), 0) for a in next_actions)

    Q[(state, action)] = old_q + alpha * (reward + gamma * future_q - old_q)

def train(episodes=100000):
    global current_player
    last_ai_state = None
    last_ai_action = None

    for _ in range(episodes):
        reset()
        state = tuple(board)

        while True:
            if current_player == -1:   # AI move
                action = choose_action(state)
                last_ai_state=state
                last_ai_action=action
                is_ai_turn = True
            else:                      # opponent move (random)
                action = random.choice(valid_actions(state))
                is_ai_turn = False

            make_move(action)
            next_state = tuple(board)
            winner=check_winner(board)

            if winner is not None:
                if winner == AI_PLAYER:
                    # AI won → reward last AI move
                    update_q(last_ai_state, last_ai_action, 1.0, next_state)

                elif winner == -AI_PLAYER:
                    # AI lost → punish last AI move
                    update_q(last_ai_state, last_ai_action, -1.0, next_state)

                else:
                    # Draw → small reward
                    update_q(last_ai_state, last_ai_action, 0.3, next_state)

                break

            else:
                if is_ai_turn:
                    update_q(state, action, 0, next_state)

            state = next_state



def save_policy(filename="ttt_policy.json"):
    policy = {}
    for (state, action), value in Q.items():
        if state not in policy or value > policy[state][1]:
            policy[state] = (action, value)

    # keep only best action
    policy = {str(k): v[0] for k, v in policy.items()}

    with open(filename, "w") as f:
        json.dump(policy, f)

def save_table(filename="ttt_qtable.json"):
    table = {str(k): v for k, v in Q.items()}

    with open(filename, "w") as f:
        json.dump(table, f, indent=2)

train(200_000)
print("Training completed.")
save_policy()
print("Policy saved to ttt_policy.json.")
save_table()
print("Q-table saved to ttt_qtable.json.")