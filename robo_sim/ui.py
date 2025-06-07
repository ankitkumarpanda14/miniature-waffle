import pygame

def draw_environment(screen, env, robot):
    cell_size = env.cell_size
    for y in range(env.height):
        for x in range(env.width):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

            if (x, y) in env.obstacles:
                pygame.draw.rect(screen, (100, 100, 100), rect)

            if (x, y) == env.dock:
                pygame.draw.rect(screen, (0, 255, 0), rect)

    # Draw robot
    rx, ry = robot.position
    robot_rect = pygame.Rect(rx * cell_size + 5, ry * cell_size + 5, cell_size - 10, cell_size - 10)
    pygame.draw.rect(screen, (0, 0, 255), robot_rect)

def draw_status(screen, robot, y_offset, height):
    font = pygame.font.SysFont(None, 24)
    text = f"Position: {robot.position} | Direction: {robot.direction} | Battery: {robot.battery}%"
    img = font.render(text, True, (0, 0, 0))
    screen.blit(img, (10, y_offset + 10))
