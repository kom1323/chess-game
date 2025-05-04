# Chess Game
This repository contains a chess app. The app also include move history, animations and a chess bot. 

# Example Videos

https://github.com/user-attachments/assets/ebccc886-a33f-4e48-a42b-57a551fde8b3





# Controlls

- Mouse clicks – move
- `z` – undo
- `r` – reset board

# Try It Yourself

1. Clone this repo
2. Setup a Python virtual environment with all the Python dependencies based on [requirements.txt](requirements.txt).
3. Choose whether a bot is playing or not in lines 45,46.
   
    ```python
    player_one = False
    player_two = False 
   ```
   `player_one` is white, `player_two` is black.
   `False` means a bot is playing.
5. Run **chess_main.py**.

# Techniques 
pygame

Negamax algorithm with Alpha-beta pruning

