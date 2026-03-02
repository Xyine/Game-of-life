import pygame
from PIL import Image
from gui.gui import GameGUI

game = GameGUI()
screen = game.screen


frames = []

# Suppose que `screen` est ta surface pygame
for _ in range(100):  # 100 frames
    game.update()      # une boucle update de ton jeu
    pygame.display.flip()
    frame = pygame.surfarray.array3d(screen)
    frame = frame.transpose([1, 0, 2])  # swap axes
    frames.append(Image.fromarray(frame))

frames[0].save('gameplay.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)