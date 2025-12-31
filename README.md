# Tic-Tac-Toe Bot using Q-Learning (From Scratch)
## What this is
A Tic-Tac-Toe AI that learns through self play without any hardcoded strategies
## Why I built this
I built this project to learn the fundamentals of Reinforcement Learning 
## How it works (high level)
- The game board is represented as a state
- Each possible move is treated as an action
- The agent plays thousands of games against an opponent which makes random moves
- The AI is rewarded for each win, loss and draw accordingly
- Over time, the AI learns the optimal strategy
## Reward system
- Win: +1
- Loss: -1
- Draw: +0.3
## Result
We get an AI which can block immediate threats, snatch at opportunities while still making human-like errors
## How to run
1. Clone the repository
2. Run `ttt train.py` to train the agent
3. Paste the newly generated `ttt_policy.json` in the same folder as `ttt play.py`
4. Run `ttt play.py` to play against the AI
## Requirements
No libraries required
## Limitation
- The AI will always play the same move for a specific board state
