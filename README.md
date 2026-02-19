# Title: RainWater Simulation #

Introduction:
This project is an interactive rainwater harvesting simulation built with Python and Pygame, designed to visually demonstrate how rainfall can be collected and managed in a simple environment. The simulation allows users to control rain intensity and activate a basic watering system to understand how rainfall contributes to storage (e.g., water tank) over time.

Technical Implementation:
This project specifically avoids high-level drawing libraries for core primitives to showcase fundamental CG algorithms:
- Bresenham's Line Algorithm: Used for drawing the raindrops, water spray.
- Midpoint Ellipse Algorithm: Used in the UI elements inside the control module.
- Linear Interpolation: Used in creating the intensity of the rainfall via slider.
- Collision: Uses in reseting the rainfall after touching the end of screen.
- Transformation and Scaling: Used to transform and scale image. 

🔍 Features:
1) Dynamic rain generation with adjustable intensity
2) Visual representation of environment, gutters, tank, and plant
3) Interactive control panel built with Pygame
4) Real-time simulation of rainwater capture and fall behavior
5) Easy to modify code for experimentation or research

🚀 Installation:

- Clone the repository:
git clone https://github.com/BisheshK/rainwater_simulation.git

- Install dependencies (make sure you have Python 3 and Pygame):
pip install pygame

- Run the simulator:
python main.py

🎮 Controls:
1) Rain Intensity Slider: Adjust how heavy the rain is
2) Water Toggle Button: Switch watering system on/off
3) Use the UI panel to interact during runtime

🛠 Project Structure
main.py — Main simulation loop & UI handlers
rain.py — Raindrop logic and physics
env.py — Scene drawing and environment setup
assets/ — Images for ground, roof, tank, etc.
