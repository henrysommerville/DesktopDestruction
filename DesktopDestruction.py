from PIL import ImageGrab
import pygame
from pygame.math import Vector2
import os
from typing import Callable
import random
import math
from utils import scale_image, blit_rotate_center
pygame.font.init()

dir_path = os.path.dirname(os.path.realpath(__file__))

TOOL_FONT = pygame.font.SysFont("arialblack", 20)
snapshot = ImageGrab.grab()
save_path = "D:\Coding\DesktopDestruction\snap.png"
snapshot.save(save_path)
SCREENSHOT = pygame.image.load(save_path)
FLAMETHROWER_IMAGE = pygame.image.load(
    "D:/Coding/DesktopDestruction/images/scorch.png")
HAMMER_IMAGE_ONE = scale_image(pygame.image.load(
    "D:/Coding/DesktopDestruction/images/hammer1.png"), 0.25)
HAMMER_IMAGE_TWO = scale_image(pygame.image.load(
    "D:/Coding/DesktopDestruction/images/hammer2.png"), 0.1)

LAWNMOWER_IMAGE = pygame.image.load(
    "D:/Coding/DesktopDestruction/images/green-car.png")

PAINTGUN_IMAGES = [
                    scale_image(pygame.image.load(
                        "D:/Coding/DesktopDestruction/images/paint1.png"), 0.2),
                    scale_image(pygame.image.load(
                       "D:/Coding/DesktopDestruction/images/paint2.png"), 0.2),
                    scale_image(pygame.image.load(
                       "D:/Coding/DesktopDestruction/images/paint3.png"), 0.05),
                    scale_image(pygame.image.load(
                       "D:/Coding/DesktopDestruction/images/paint4.png"), 0.05),
                    scale_image(pygame.image.load(
                       "D:/Coding/DesktopDestruction/images/paint5.png"), 0.15)
                   ]

SCREEN_WIDTH = SCREENSHOT.get_width()
SCREEN_HEIGHT = SCREENSHOT.get_height()


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 colour=(255, 255, 255)) -> None:
        self.width = width
        self.height = height
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.hover_colour = (255, 0, 0)
        self.is_mouse_over = False

    def draw(self, win, outline=None):
        self.is_mouse_over = self.mouse_over()
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y -
                             2, self.width+4, self.height+4), 0)

        if self.is_mouse_over:
            pygame.draw.rect(win, self.hover_colour,
                             (self.x, self.y, self.width, self.height), 0)
        else:
            pygame.draw.rect(win, self.colour,
                             (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('arial', 20)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                     self.y + (self.height/2 - text.get_height()/2)))

    def mouse_over(self):
        pos = pygame.mouse.get_pos()
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class FlameThrowerButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 colour=(255, 255, 255)) -> None:
        super().__init__(x, y, width, height, text, colour)

    def on_click(self):
        print("This is working")


class HammerButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 colour=(255, 255, 255)) -> None:
        super().__init__(x, y, width, height, text, colour)

    def on_click(self):
        print("This is working")


class LawnMowerButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 colour=(255, 255, 255)) -> None:
        super().__init__(x, y, width, height, text, colour)

    def on_click(self):
        print("This is working")


class PaintGunButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 colour=(255, 255, 255)) -> None:
        super().__init__(x, y, width, height, text, colour)

    def on_click(self):
        print("This is working")


class ClearButton(Button):
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 colour=(255, 255, 255)) -> None:
        super().__init__(x, y, width, height, text, colour)

    def on_click(self):
        print("This is working")


class DestructiveImage:
    def __init__(self, x: int, y: int, image: pygame.image, offset_x=0, offset_y=0) -> None:
        self.x_center = x
        self.y_center = y
        self.image = image
        self.x = self.x_center - (self.image.get_width() / 2) + offset_x
        self.y = self.y_center - (self.image.get_height() / 2) + offset_y

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class LawnMower:
    def __init__(self, x, y, max_vel, rotation_vel):
        self.img = LAWNMOWER_IMAGE
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x = x
        self.y = y
        self.acceleration = 0.2

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


"""
Draw the toolbar onto the screen

Parameters:
    win (pygame.display): The game window
    buttons (list): list containing button objects to draw
"""
def draw_toolbar(win, buttons) -> None:
    for button in buttons:
        button.draw(win)
    return None


"""
Draw Screen
Parameters:
    win (pygame.display): the game window
    buttons (list): list containing button objects to draw
"""
def draw(win: pygame.display, buttons: list, \
        destructive_images: list[DestructiveImage], lawnmower_spawned: bool, \
        lawnmower: LawnMower) -> None:
    win.blit(SCREENSHOT, (0, 0))
    for image in destructive_images:
        image.draw(win)
    draw_toolbar(win, buttons)
    if lawnmower_spawned:
        lawnmower.draw(win)
    return None


"""
Initalizes the Button Array

Returns:
    List: List containing button objects
"""
def initialise_buttons() -> list:
    return [FlameThrowerButton(500, 10, 200, 100, "FlameThrower"),
            HammerButton(700, 10, 200, 100, "Hammer"),
            LawnMowerButton(900, 10, 200, 100, "LawnMower"),
            PaintGunButton(1100, 10, 200, 100, "Paint Gun"),
            ClearButton(1300, 10, 200, 100, "Clear")]


def flame_tool(destructive_images):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0] == True:  # evaluate left button
        destructive_images.append(DestructiveImage(
            cur[0], cur[1], FLAMETHROWER_IMAGE))


def paint_tool(destructive_images):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0] == True:  # evaluate left button
        num = random.randint(0, len(PAINTGUN_IMAGES) - 1)
        destructive_images.append(DestructiveImage(
            cur[0], cur[1], PAINTGUN_IMAGES[num]))


def lawnmower_control(lawnmower):
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_a]:
        lawnmower.rotate(left=True)
    if keys[pygame.K_d]:
        lawnmower.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        lawnmower.move_forward()
    if keys[pygame.K_s]:
        moved = True
        lawnmower.move_backward()

    if not moved:
        lawnmower.reduce_speed()


def main():
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Desktop Destruction')
    running = True
    buttons = initialise_buttons()
    destructive_images = []
    flamethrower_tool = False
    hammer_tool = False
    lawnmower_tool = False
    lawnmower_spawned = False
    paintgun_tool = False
    lawnmower = LawnMower(0, 0, 2, 2)

    while running:
        for event in pygame.event.get():
            # keyboard Press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    flamethrower_tool = True
                    hammer_tool = False
                    lawnmower_tool = False
                    paintgun_tool = False
                if event.key == pygame.K_2:
                    flamethrower_tool = False
                    hammer_tool = True
                    lawnmower_tool = False
                    paintgun_tool = False
                if event.key == pygame.K_3:
                    flamethrower_tool = False
                    hammer_tool = False
                    lawnmower_tool = True
                    paintgun_tool = False
                if event.key == pygame.K_4:
                    flamethrower_tool = False
                    hammer_tool = False
                    lawnmower_tool = False
                    paintgun_tool = True
                if event.key == pygame.K_BACKSPACE \
                        or event.key == pygame.K_DELETE or event.key == pygame.K_c:
                    print("clear")
                if event.key == pygame.K_ESCAPE:
                    running = False

            tool_active = True
            # Mouse Press
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        if button.mouse_over():
                            tool_active = False
                            if type(button) == FlameThrowerButton:
                                flamethrower_tool = True
                                hammer_tool = False
                                lawnmower_tool = False
                                paintgun_tool = False
                                button.on_click()
                            if type(button) == PaintGunButton:
                                flamethrower_tool = False
                                hammer_tool = False
                                lawnmower_tool = False
                                paintgun_tool = True
                                button.on_click()
                            if type(button) == LawnMowerButton:
                                flamethrower_tool = False
                                hammer_tool = False
                                lawnmower_tool = True
                                paintgun_tool = False
                                button.on_click()
                            if type(button) == HammerButton:
                                flamethrower_tool = False
                                hammer_tool = True
                                lawnmower_tool = False
                                paintgun_tool = False
                                button.on_click()
                            if type(button) == ClearButton:
                                flamethrower_tool = False
                                hammer_tool = False
                                lawnmower_tool = False
                                lawnmower_spawned = False
                                paintgun_tool = False

                                destructive_images.clear()
                            break
                        else:
                            tool_active = True

                    x, y = pygame.mouse.get_pos()
                    if tool_active:
                        if hammer_tool:
                            num = random.randint(0, 1)
                            if num == 0:
                                image = HAMMER_IMAGE_ONE
                                destructive_images.append(
                                    DestructiveImage(x, y, image, -20, 5))
                            elif num == 1:
                                image = HAMMER_IMAGE_TWO
                                destructive_images.append(
                                    DestructiveImage(x, y, image, -25, 10))
                        if not lawnmower_spawned and lawnmower_tool:
                            lawnmower_spawned = True
                            lawnmower.x = x - (LAWNMOWER_IMAGE.get_width() / 2)
                            lawnmower.y = y - \
                                (LAWNMOWER_IMAGE.get_height() / 2)

            # Quit pygame
            if event.type == pygame.QUIT:
                running = False

        if tool_active:
            if flamethrower_tool:
                flame_tool(destructive_images)
            if paintgun_tool:
                paint_tool(destructive_images)
            if lawnmower_spawned and lawnmower_tool:
                lawnmower_control(lawnmower)
        # Draw Screen
        draw(win, buttons, destructive_images, lawnmower_spawned, lawnmower)

        if len(destructive_images) > 250:
            destructive_images = destructive_images[1:]

        pygame.display.update()

    # remove screenshot and quit
    os.remove(save_path)
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
