# 2D Shooter Game Prototype
<p align="center">
  <img src="https://github.com/user-attachments/assets/2b371721-181d-4498-b5b6-3b7e8f43530a" alt="Game Screenshot" width="600"/>
</p>

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

## Game Screenshots

## English Localised Menu Screen
<p align="center">
  <img width="550" height="350" alt="Screenshot 2025-03-13 212100" src="https://github.com/user-attachments/assets/14e9660a-3047-44b8-ac3e-619df30d2630" />
</p>

## Arabic Localised Menu Screen
<p align="center">
  <img width="550" height="350" alt="Screenshot 2025-04-18 163148" src="https://github.com/user-attachments/assets/702f3c1d-50c5-41c8-81dc-7623526038c2" />
</p>

## Leaderboard Screen
<p align="center">
  <img width="597" height="341" alt="Screenshot 2025-04-08 195012" src="https://github.com/user-attachments/assets/f21bf5de-90de-4899-9a93-2ab795debad2" />
  </p>
<p align="center">
  <img width="597" height="341" alt="Screenshot 2025-04-12 185036" src="https://github.com/user-attachments/assets/3d798546-e8d5-49b6-9687-27cb22af81d2" />
</p>

