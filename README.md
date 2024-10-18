# Question 1

## Overview

This is a Tkinter-based text summarization application that uses the Hugging Face BART model for summarization. The app provides two key functionalities:
1. **Summarize Text**: Generates a summary from the input text using the BART model.
2. **Rephrase Summary**: Provides a variation of the summary by using random sampling.

## Features

- **Summarization**: Automatically generates a concise summary for any input text.
- **Rephrasing**: Offers a rephrased version of the summary for variety.
- **Clear Text**: Allows clearing both the input and output fields.
- **Help Menu**: Provides information on how to use the application and displays application details.

## Requirements

Before running the application, make sure you have the following packages installed:

- `tkinter`: For creating the graphical user interface.
- `transformers`: For using the Hugging Face BART model.
- `torch`: Required for model inference with `transformers`.

## Package Installation

To install the required Python packages, use the following commands:

```bash
pip install -r requirements.txt
```

## How to Run the Application

- Clone this repository or copy the code to your local machine.
- Ensure that the necessary packages are installed.
- Run the following command in your terminal or command prompt:

```bash
python question1/summarizer_app.py
```
- The application window will open, allowing you to input text, summarize it, rephrase the summary, and clear the fields.

## Usage Instructions
- Enter the text you want to summarize in the Input Text area.
- Click the Summarize button to get the summarized output.
- Click the Rephrase button to generate a variation of the summary.
- Use the Clear button to reset both the input and output fields.
- Navigate to the Help menu for more details about the application and instructions.

# Question 2
# Side-Scrolling Adventure Game

## Overview

This project is a 2D side-scrolling adventure game built using the Pygame library in Python. The game features various gameplay elements such as a player character, enemies, collectibles, and multiple levels. The player can move, jump, shoot, and interact with the environment, while enemies chase or patrol, and collectibles enhance the player's health or lives. The game is controlled via the keyboard and features a parallax background and smooth camera movement.

## Game Features

- **Player Movement**: The player can run, jump, and shoot projectiles.
- **Enemies**: Different enemy types, including regular enemies and a boss enemy.
- **Collectibles**: Items like health and extra lives can be collected to enhance gameplay.
- **Sound Effects**: Sound is integrated for actions like jumping, shooting, and collecting items.
- **Parallax Scrolling Background**: A layered background creates a parallax effect for a more immersive experience.
- **Multiple Levels**: The game has three levels with progressively harder enemies and challenges.
- **Camera System**: Smooth camera movement follows the player to keep the action centered.
- **Main Menu & Game Over Screens**: A simple menu system for starting and restarting the game.

## Installation

1. **Install Python**: Ensure you have Python 3.7 or later installed.
   
2. **Install Pygame**: You need the Pygame library to run the game. Install it using pip:
   ```bash
   pip install pygame
   ```

3. **Download Assets**: The game requires several assets (images and sounds) to run properly. Ensure that the following files are in the project directory:
   - `jump.mp3`, `shoot.mp3`, `collect.mp3` for sound effects.
   - `player_spritesheet.png` for player animations.
   - `bullet_image.png` for the player's projectile.
   - `enemy_image.png`, `boss_image.png` for enemy sprites.
   - `background_layer4.png` for the parallax background.
   - `health_image.png`, `extra_life_image.png` for collectibles.

4. **Run the Game**: To start the game, run the following command in your terminal:
   ```bash
   python <script_name>.py
   ```

## Controls

- **Arrow Keys (Left/Right)**: Move the player left or right.
- **Spacebar**: Jump.
- **F**: Shoot a projectile.
- **R**: Restart the game after game over.
- **Q**: Quit the game.

## Gameplay

- **Objective**: The goal is to navigate through each level by defeating enemies and collecting items. Survive by managing health and lives. Complete all three levels to win the game.
- **Health and Lives**: Players start with 100 health and 3 lives. Collectibles like health packs and extra lives are scattered throughout levels to help you survive longer.
- **Enemies**: Each level has different enemies. The final level features a boss enemy with higher health and slower movement.

## Game Loop

1. **Main Menu**: The game starts at the main menu. Press `ENTER` to begin.
2. **Levels**: As you progress, enemies become more challenging and collectibles more scarce.
3. **Game Over**: If your lives run out, you'll be taken to the Game Over screen, where you can restart or quit.

## Customization

Feel free to modify the following:

- **Player animations**: Modify `player_spritesheet.png` for custom player animations.
- **Enemy behavior**: Tweak the `Enemy` and `BossEnemy` classes for different enemy patterns or stats.
- **Level Design**: Use the `load_level` function to create new levels by adding more enemies and collectibles.
  
## Dependencies

- **Python 3.7+**
- **Pygame**

## Future Enhancements

- Add more levels with unique mechanics.
- Integrate power-ups or additional weapon types.
- Expand on enemy types with more complex behavior patterns.
- Add background music and more sound effects for a richer experience.

## License

This project is open-source and available under the MIT License.

## Acknowledgments

Thanks to the Pygame community for providing tutorials and resources for game development.

Enjoy the game!
