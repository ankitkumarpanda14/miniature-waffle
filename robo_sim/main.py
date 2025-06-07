import pygame
from environment import Environment
from robot import Robot
from ui import draw_environment, draw_status
from llm_interface import convert_command_to_plan
import pygame.freetype


# Initialize Pygame
pygame.init()
pygame.freetype.init()
font = pygame.freetype.SysFont(None, 24)
user_input = ""
input_mode = False
cell_size = 60
grid_width, grid_height = 10, 10
screen = pygame.display.set_mode((grid_width * cell_size, grid_height * cell_size + 40))
pygame.display.set_caption("LLM Robot Simulator")

# Environment and Robot
env = Environment(grid_width, grid_height, cell_size)
robot = Robot(env)

# Add test obstacle and dock
env.add_obstacle(2, 2)
env.set_dock((9, 9))

clock = pygame.time.Clock()
running = True

while running:
    screen.fill((255, 255, 255))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if input_mode:
                if event.key == pygame.K_RETURN:
                    plan = convert_command_to_plan(user_input)
                    robot.set_plan(plan)
                    print("▶️ Executing:", plan)
                    user_input = ""
                    input_mode = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
            elif event.key == pygame.K_RETURN:
                input_mode = True  # Start taking input


    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        robot.move_forward()
    if keys[pygame.K_LEFT]:
        robot.turn_left()
    if keys[pygame.K_RIGHT]:
        robot.turn_right()

    if keys[pygame.K_RETURN]:  # Press Enter to type a command
        user_input = input("Enter command: ")
        plan = convert_command_to_plan(user_input)
        robot.set_plan(plan)

    robot.execute_next_action()

    draw_environment(screen, env, robot)
    draw_status(screen, robot, grid_height * cell_size, 40)
    if input_mode:
        pygame.draw.rect(screen, (220, 220, 220), (10, grid_height * cell_size + 5, 600, 30))
        font.render_to(screen, (15, grid_height * cell_size + 10), f"Command: {user_input}", (0, 0, 0))

    pygame.display.flip()
    clock.tick(5)

pygame.quit()
