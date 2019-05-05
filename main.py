import pygame

import resources
from world import World

pygame.init()

display_width = 1280
display_height = 768

nr_tiles_x = 100
nr_tiles_y = 80

tile_size = 64

def load_images():
    for key in resources.tile_dict:
        resources.tile_dict[key]["img"] = pygame.image.load(resources.tile_dict[key]['filename'])

load_images()

world = World(nr_tiles_x, nr_tiles_y)

"""
Set the start for the player
"""
world.add_player("Johan")


gameDisplay = pygame.display.set_mode((display_width, display_height))#, pygame.FULLSCREEN)
pygame.display.set_caption('Civ')
clock = pygame.time.Clock()


def game_loop():

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         pygame.quit()
            #         quit()
            #
            #     if event.key == pygame.K_LEFT:
            #         x_change = -5
            #     if event.key == pygame.K_RIGHT:
            #         x_change = 5
            #
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #         x_change = 0

        # gameDisplay.fill(white)

        world.draw("Johan", gameDisplay, screen_width=display_width, screen_height=display_height,
                   tile_size=tile_size)

        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
quit()


# # FROM TEMPLATE
# def text_objects(text, font):
#     textSurface = font.render(text, True, black)
#     return textSurface, textSurface.get_rect()
# black = (0, 0, 0)
# white = (255, 255, 255)
# red = (255, 0, 0)
#
# # FROM TEMPLATE
# def message_display(text):
#     largeText = pygame.font.Font('freesansbold.ttf', 115)
#     TextSurf, TextRect = text_objects(text, largeText)
#     TextRect.center = ((display_width / 2), (display_height / 2))
#     gameDisplay.blit(TextSurf, TextRect)
#
#     pygame.display.update()
#
#     time.sleep(2)
#
#     game_loop()
