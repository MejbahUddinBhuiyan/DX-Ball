#  DX Ball Game (PyOpenGL)

A classic **DX Ball / Brick Breaker** style game built using **Python** and **PyOpenGL**.  
The game features smooth paddle movement, ball physics, brick collision, scoring, lives, and progressive difficulty through levels.

This project is designed for **learning OpenGL fundamentals**, **game loops**, and **collision detection** using Python.

---

##  Game Features

-  Smooth paddle movement (Arrow keys / WASD)
-  Real-time ball physics
-  Brick collision & destruction
-  Life system (3 lives)
-  Level progression with increasing difficulty
-  Score tracking
-  Restart option after Game Over
-  Fixed-timestep game loop using GLUT timer

---

##  Technologies Used

- **Python 3**
- **PyOpenGL**
- **GLUT**
- **OpenGL (2D Orthographic Projection)**

---

## ▶ How to Run

### 1️⃣ Install Dependencies
```bash
pip install PyOpenGL PyOpenGL_accelerate
python dxBall.py
```
## Controls
| Key     | Action                         |
| ------- | ------------------------------ |
| ⬅️ / ➡️ | Move paddle left / right       |
| A / D   | Move paddle (optional)         |
| R       | Restart game (after Game Over) |
| ESC     | Exit game                      |


## Game Logic Overview
- Bricks are generated dynamically using rows & columns.

- Ball collisions are handled with:

   - Walls

   - Paddle

   - Bricks

- Each destroyed brick increases the score.

- Completing a level increases ball speed for higher difficulty.

- Losing all lives triggers Game Over.

## Tested Environment

- Python 3.9+

- Windows / Linux

- OpenGL 2.0+

##  Project Structure

dx-ball/  
│  
├── dxBall.py          
└── README.md       

## Author

### Mejbah Uddin Bhuiyan  
BSc in Computer Science & Engineering  
BRAC University  

## License

This project is intended for educational and academic use.  
You are free to modify, extend, and experiment with the code.  
