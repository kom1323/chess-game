# Chess Game

This repository contains a chess app. The app includes move history, animations, and a chess bot.

# Example Videos

Here’s a demo of the game in action:

[Watch the demo video](https://github.com/user-attachments/assets/ebccc886-a33f-4e48-a42b-57a551fde8b3)

# Controls

- **Mouse clicks** – Move a piece  
- **`z`** – Undo the last move  
- **`r`** – Reset the board

# Try It Yourself

1. Clone this repository to your local machine.
2. Set up a Python virtual environment with all the Python dependencies from the [requirements.txt](requirements.txt).
3. Choose whether a bot is playing or not in lines 45 and 46:

    ```python
    player_one = False
    player_two = False
    ```

    `player_one` is white, `player_two` is black. `False` means a bot is playing.

4. Run **chess_main.py**.

# Techniques

- pygame  
- Negamax algorithm with Alpha-beta pruning
