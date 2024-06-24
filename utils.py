import pygame

def scale_image(image, factor):
    size = (round(image.get_width() * factor),
            round(image.get_height() * factor))
    return pygame.transform.scale(image, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)

def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)

def blit_text(win, font, text, position, color=(255, 255, 255)):
    render = font.render(text, 1, color)
    win.blit(render, position)
    