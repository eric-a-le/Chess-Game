---
layout: page
title: "How to Set Up"
permalink: /setup/
---
# Main Setup:
Step 1. Clone this repo to your computer
- Open Command Prompt on your computer. Use the cd command to move into the directory you want to clone this project into.
- Once inside the directory, run this command: ```git clone https://github.com/olincollege/Chess-Game.git```
- You should now see a folder called "Chess-Game"

Step 2. Run main.exe 
- main.exe is inside of the Chess-Game folder
- We want to clone the project first because your browser might block you from downloading the .exe file directly from GitHub

You're all set! Once you run main.exe should see the pygame window appear on your screen :)

# Alternative Setup:
The program can run on Python 3.14, 3.13, or earlier versions. It is recommended to use pygame-ce, but pygame has also worked.

Step 1. Clone this repo
```
git clone https://github.com/olincollege/Chess-game.git
```
Step 2. Install requirements
```
pip install -r requirements.txt
```
This will install the latest version of pygame-ce.
You can also install pygame-ce with
```
pip install pygame-ce
```
Alternatively, you can install pygame if using Python 3.13 or earlier:
```
pip install pygame
```
If using a Windows system, you may need to use the following prefix:
```
py -m pip install -r requirements.txt
```
Step 3. Use the following commands to run Chess-Game:
```
cd Chess-Game
python main.py
```
## Stockfish Implementation
If you want to play against the computer, you will also need to download Stockfish. Currently, our code implementation for accessing Stockfish only works for Windows and WSL.

Step 1. Download Stockfish for Windows at [https://stockfishchess.org/download/](https://stockfishchess.org/download/)

Step 2. Move the resulting Stockfish folder into the Chess-Game folder. If using VSCode for Windows, the Chess-Game folder may be inside the documents folder accesed throught the following path: This PC > OS(C:) > User

Troubleshooting:

If sprites or Stockfish isn't loading, make sure to have the Chess-Game folder open before running.