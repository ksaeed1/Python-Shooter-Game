# 2D Shooter Game Prototype
<img width="984" height="793" alt="Screenshot 2025-04-18 163204" src="https://github.com/user-attachments/assets/2b371721-181d-4498-b5b6-3b7e8f43530a" />

## Folder Structure

- `main_game.py` – Main file to run the game.
- `setup_leaderboard_db.py` – Script to create and initialise the leaderboard database.
- `leaderboard.db` – SQLite database file used to save player's score.
- `ar.json` – Contains Arabic translations.
- `translations.json` – Folder for both EN and AR translations.
- `img` – Game images and icons.
- `audio` – Sound effects and music files.
- `level1_data.csv` – Stores the tile map for the level's background.
- `Amiri-Regular.ttf` – Arabic font used for rendering Arabic text correctly.


## Required Installations

Before running the game, ensure you have Python 3.13.1 installed. Then install the following libraries by running these commands in your terminal:

pip install pygame
pip install arabic_reshaper
pip install python-bidi
pip install babel


## Running the Game

If you are using Sublime Text (preferred) or another IDE:

1. Open your terminal.
2. Navigate to the project folder: cd path/to/Prototype_KhadeejahSaeed_19220863
3. Run the game: python main_game.py (Or press Ctrl + B in Sublime Text)


## Note on Language

Due to technical constraints, the game opens with the default language set to English. This is to ensure that non-Arabic speaking users can understand the "Enter your name" input prompt.

However, if you would like to view the correct Arabic text rendering achieved in the prototype for the "Enter your name" prompt, you can manually change the default language by changing the following line of code (Line 165 in the code) to: current_language = "ar"



