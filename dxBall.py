from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys
from math import sin, cos

# =====================
# Window Configuration
# =====================
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# =====================
# Game Variables
# =====================
score = 0
lives = 3
level = 1
game_over = False

# =====================
# Paddle
# =====================
paddle_width = 120
paddle_height = 15
paddle_x = WINDOW_WIDTH // 2
paddle_y = 40
paddle_speed = 8   # smooth speed

# Paddle key states
key_left = False
key_right = False

# =====================
# Ball
# =====================
ball_radius = 8
ball_x = WINDOW_WIDTH // 2
ball_y = paddle_y + 20
ball_dx = 3
ball_dy = 3

# =====================
# Bricks
# =====================
brick_rows = 5
brick_cols = 10
brick_width = 70
brick_height = 20
bricks = []

# =====================
# Utility Functions
# =====================
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = WINDOW_WIDTH // 2
    ball_y = paddle_y + 20
    ball_dx = random.choice([-3, 3])
    ball_dy = 3


def reset_game():
    global score, lives, level, game_over
    score = 0
    lives = 3
    level = 1
    game_over = False
    create_bricks()
    reset_ball()

# =====================
# Brick System
# =====================
def create_bricks():
    global bricks
    bricks = []
    offset_x = (WINDOW_WIDTH - (brick_cols * brick_width)) // 2
    offset_y = WINDOW_HEIGHT - 100

    for row in range(brick_rows):
        for col in range(brick_cols):
            x = offset_x + col * brick_width
            y = offset_y - row * brick_height
            bricks.append([x, y, True])

# =====================
# Drawing Functions
# =====================
def draw_rect(x, y, w, h):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()


def draw_circle(x, y, r):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(0, 361, 5):
        angle = i * 3.1416 / 180
        glVertex2f(x + r * cos(angle), y + r * sin(angle))
    glEnd()


def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

# =====================
# Collision Detection
# =====================
def check_collisions():
    global ball_dx, ball_dy, score, level

    # Wall collision
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WINDOW_WIDTH:
        ball_dx *= -1

    if ball_y + ball_radius >= WINDOW_HEIGHT:
        ball_dy *= -1

    # Paddle collision
    if (paddle_x - paddle_width // 2 <= ball_x <= paddle_x + paddle_width // 2 and
            paddle_y <= ball_y - ball_radius <= paddle_y + paddle_height):
        ball_dy = abs(ball_dy)

    # Brick collision
    for brick in bricks:
        if not brick[2]:
            continue
        bx, by = brick[0], brick[1]
        if (bx <= ball_x <= bx + brick_width and
                by <= ball_y <= by + brick_height):
            brick[2] = False
            ball_dy *= -1
            score += 10

    # Level complete
    if all(not brick[2] for brick in bricks):
        level += 1
        create_bricks()
        ball_dy += 0.5   # difficulty increase
        reset_ball()

# =====================
# Game Update 
# =====================
def update():
    global ball_x, ball_y, lives, game_over, paddle_x

    if game_over:
        return

    # Smooth paddle movement
    if key_left:
        paddle_x -= paddle_speed
    if key_right:
        paddle_x += paddle_speed

    paddle_x = max(paddle_width // 2,
                   min(WINDOW_WIDTH - paddle_width // 2, paddle_x))

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball lost
    if ball_y < 0:
        lives -= 1
        if lives == 0:
            game_over = True
        reset_ball()

    check_collisions()
    glutPostRedisplay()

# =====================
# timer
# =====================
def timer(value):
    update()
    glutTimerFunc(16, timer, 0)

# =====================
# Keyboard Input
# =====================
def keyboard(key, x, y):
    if key == b'r' and game_over:
        reset_game()
    elif key == b'\x1b':
        sys.exit()

    # Optional WASD
    if key == b'a':
        global paddle_x
        paddle_x -= paddle_speed
    elif key == b'd':
        paddle_x += paddle_speed


def special_key_down(key, x, y):
    global key_left, key_right
    if key == GLUT_KEY_LEFT:
        key_left = True
    elif key == GLUT_KEY_RIGHT:
        key_right = True


def special_key_up(key, x, y):
    global key_left, key_right
    if key == GLUT_KEY_LEFT:
        key_left = False
    elif key == GLUT_KEY_RIGHT:
        key_right = False

# =====================
# Rendering
# =====================
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Paddle
    glColor3f(0.2, 0.8, 0.9)
    draw_rect(paddle_x - paddle_width // 2, paddle_y,
              paddle_width, paddle_height)

    # Ball
    glColor3f(1, 1, 1)
    draw_circle(ball_x, ball_y, ball_radius)

    # Bricks
    glColor3f(1, 0.3, 0.3)
    for brick in bricks:
        if brick[2]:
            draw_rect(brick[0], brick[1],
                      brick_width, brick_height)

    # HUD
    glColor3f(1, 1, 1)
    draw_text(10, 570, f"Score: {score}")
    draw_text(200, 570, f"Lives: {lives}")
    draw_text(350, 570, f"Level: {level}")

    if game_over:
        draw_text(300, 300, "GAME OVER")
        draw_text(260, 260, "Press R to Restart")

    glutSwapBuffers()

# =====================
# OpenGL Setup
# =====================
def init():
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

# =====================
# Main
# =====================
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"DX Ball - PyOpenGL")

    init()
    create_bricks()

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_key_down)
    glutSpecialUpFunc(special_key_up)
    glutTimerFunc(0, timer, 0)

    glutMainLoop()


if __name__ == "__main__":
    main()
