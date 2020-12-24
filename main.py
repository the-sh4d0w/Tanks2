import enum
import json
import os
import typing

import pygame


class Game:
    """The game class."""

    def __init__(self) -> None:
        """Initializes the game.

        Returns:
            Nothing.
        """
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 400
        self.window = pygame.display.set_mode(size=(
            self.WIDTH, self.HEIGHT), flags=pygame.SCALED | pygame.RESIZABLE)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
        self.clock = pygame.time.Clock()
        self.player_one = None
        self.player_two = None
        self.bullets = []
        self.walls = []
        self.entities = []
        self.level_number = 6
        self.debug = False
        self.invulnerable = False
        self.debug = False
        self.color_one = Color.blue
        self.color_two = Color.yellow
        self.volume = 1.0
        with open("config.json", "r") as f:
            self.config = json.load(f)
        pygame.display.set_caption("Tanks2")
        pygame.display.set_icon(pygame.image.load(
            f"images{os.sep}icon.png").convert_alpha())

    def load_level(self) -> None:
        """Loads levels.

        Returns:
            Nothing.
        """
        with open(f"levels{os.sep}level_{self.level_number}.json", "r") as f:
            level = json.load(f)
        self.player_one = Player(level["spawn_one"][0], level["spawn_one"][1], self.config["speed"],
                                 self.config["firerate"], self.color_one, ord("a"), ord("d"), ord("w"), ord("s"), ord("f"))
        self.player_two = Player(level["spawn_two"][0], level["spawn_two"][1], self.config["speed"], self.config["firerate"],
                                 self.color_two, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, ord("l"))
        self.entities = []
        self.walls = []
        self.bullets = []
        self.entities.append(self.player_one)
        self.entities.append(self.player_two)
        for wall in level["walls"]:
            wall_ = Wall(wall["position"][0],
                         wall["position"][1], wall["type"])
            self.walls.append(wall_)

    def game_loop(self) -> None:
        """The main loop of the game.

        Returns:
            Nothing.
        """
        if not os.path.isfile(f"levels{os.sep}level_{self.level_number}.json"):
            self.level_number = 1
            return
        self.load_level()
        dead = False
        pygame.mixer.music.load(f"sound{os.sep}background_song.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)
        while not dead:
            self.window.fill((190, 190, 190))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_F3:
                        self.debug = not self.debug
                    elif event.key == pygame.K_F2:
                        dead = 2
                    elif event.key == pygame.K_F1:
                        dead = 1
            self.entities = [self.player_one, self.player_two] + self.walls
            self.player_one.move(self.entities, self.HEIGHT, self.WIDTH)
            self.player_one.attack(self.bullets)
            self.player_one.update(self.window)
            self.player_two.move(self.entities, self.HEIGHT, self.WIDTH)
            self.player_two.attack(self.bullets)
            self.player_two.update(self.window)
            for bullet in self.bullets:
                dead = bullet.move(self.bullets, self.walls, self.player_one,
                                   self.player_two, self.HEIGHT, self.WIDTH, self.window)
                bullet.update(self.window)
            for wall in self.walls:
                wall.update(self.window)
            if self.debug:
                self.window.blit(pygame.font.SysFont(
                    "Arial, Helvetica, sans-serif", 20).render("Debug", False, (255, 255, 255)), (10, 10))
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
                    f"FPS: {round(self.clock.get_fps())}", False, (255, 255, 255)), (10, 30))
                pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(
                    self.player_one.rect.x, self.player_one.rect.y, self.player_one.rect.width, self.player_one.rect.height), 1)
                pygame.draw.rect(self.window, (0, 255, 0), pygame.Rect(
                    self.player_two.rect.x, self.player_two.rect.y, self.player_two.rect.width, self.player_two.rect.height), 1)
                for wall in self.walls:
                    pygame.draw.rect(self.window, (255, 0, 0), pygame.Rect(
                        wall.rect.x, wall.rect.y, wall.rect.width, wall.rect.height), 1)
                for bullet in self.bullets:
                    pygame.draw.rect(self.window, (0, 0, 255), pygame.Rect(
                        bullet.rect.x, bullet.rect.y, bullet.rect.width, bullet.rect.height), 1)
            pygame.display.update()
            self.clock.tick(self.config["fps"])
        self.result_screen(dead)
        self.game_loop()

    def menu_screen(self) -> None:
        """The menu screen. Allows either starting the game or quitting it.

        Returns:
            Nothing.
        """
        selected = Menu.Start
        pygame.mixer.music.load(f"sound{os.sep}menu_song.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)
        while True:
            self.window.fill((190, 190, 190))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = selected.previous()
                    elif event.key == pygame.K_DOWN:
                        selected = selected.next()
                    elif event.key == pygame.K_RETURN:
                        if selected == Menu.Start:
                            self.game_loop()
                            pygame.mixer.music.load(
                                f"sound{os.sep}menu_song.wav")
                            pygame.mixer.music.play(-1)
                        elif selected == Menu.Farbwahl:
                            self.color_choosing_screen()
                        elif selected == Menu.Optionen:
                            self.options_screen()
                        elif selected == Menu.Credits:
                            self.credit_screen()
                        elif selected == Menu.Beenden:
                            pygame.quit()
                            quit()
            self.window.blit(pygame.font.SysFont(
                "Arial, Helvetica, sans-serif", 80).render("Tanks 2", False, (0, 0, 255)), (300, 10))
            x = 380
            y = 120
            for menu_item in Menu:
                if menu_item == selected:
                    color = (0, 0, 255)
                else:
                    color = (0, 0, 0)
                self.window.blit(pygame.font.SysFont(
                    "Arial, Helvetica, sans-serif", 20).render(str(menu_item), False, color), (x, y))
                y += 50
            pygame.display.update()
            self.clock.tick(60)

    def color_choosing_screen(self) -> None:
        """The color choosing screen. Lets players choose their color.

        Returns:
            Nothing.
        """
        options = True
        while options:
            self.window.fill((190, 190, 190))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        options = False
                    if event.key == pygame.K_a:
                        self.color_one = self.color_one.previous()
                        if self.color_one == self.color_two:
                            self.color_one = self.color_one.previous()
                    elif event.key == pygame.K_d:
                        self.color_one = self.color_one.next()
                        if self.color_one == self.color_two:
                            self.color_one = self.color_one.next()
                    if event.key == pygame.K_LEFT:
                        self.color_two = self.color_two.previous()
                        if self.color_two == self.color_one:
                            self.color_two = self.color_two.previous()
                    elif event.key == pygame.K_RIGHT:
                        self.color_two = self.color_two.next()
                        if self.color_two == self.color_one:
                            self.color_two = self.color_two.next()
            self.window.blit(pygame.image.load(
                f"images{os.sep}player_{str(self.color_one)}{os.sep}player_{str(self.color_one)}_up.png").convert_alpha(), (200, 200))
            self.window.blit(pygame.image.load(
                f"images{os.sep}player_{str(self.color_two)}{os.sep}player_{str(self.color_two)}_up.png").convert_alpha(), (600, 200))
            self.window.blit(pygame.font.SysFont(
                "Arial, Helvetica, sans-serif", 40).render("Farbwahl", False, (0, 0, 255)), (320, 70))
            self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                 20).render(str(self.color_one), False, (0, 0, 0)), (200, 230))
            self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                 20).render(str(self.color_two), False, (0, 0, 0)), (600, 230))
            pygame.display.update()
            self.clock.tick(60)

    def options_screen(self) -> None:
        """The options screen. For configuring sound.

        Returns:
            Nothing.
        """
        options = True
        while options:
            self.window.fill((190, 190, 190))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        options = False
                    if event.key == pygame.K_UP:
                        self.volume += 0.01
                        if self.volume > 1.0:
                            self.volume = 1.0
                        pygame.mixer.music.set_volume(self.volume)
                    elif event.key == pygame.K_DOWN:
                        if self.volume < 0.0:
                            self.volume = 0.0
                        self.volume -= 0.01
                        pygame.mixer.music.set_volume(self.volume)
            self.window.blit(pygame.font.SysFont(
                "Arial, Helvetica, sans-serif", 80).render("Optionen", False, (0, 0, 255)), (300, 10))
            self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
                f"Lautstärke: {int(self.volume * 100)}%", False, (0, 0, 255)), (380, 120))
            pygame.display.update()
            self.clock.tick(60)

    def result_screen(self, player: int) -> None:
        """The result screen. Shows who has won.

        Arguments:
            player: the number of the player.

        Returns:
            Nothing.
        """
        self.level_number += 1
        winner = True
        ok = True
        pygame.mixer.music.load(f"sound{os.sep}winner_song.wav")
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)
        while winner:
            self.window.fill((190, 190, 190))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        ok = not ok
                    elif event.key == pygame.K_LEFT:
                        ok = not ok
                    elif event.key == pygame.K_RETURN:
                        if ok:
                            winner = False
                        else:
                            pygame.quit()
                            quit()
            self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 50).render(
                f"Spieler {player} hat gewonnen!", False, (0, 150, 0)), (180, 120))
            if ok:
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Weiter", False, (0, 0, 150)), (290, 200))
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Beenden", False, (0, 0, 0)), (430, 200))
            else:
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Weiter", False, (0, 0, 0)), (290, 200))
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Beenden", False, (0, 0, 150)), (430, 200))
            pygame.display.update()
            self.clock.tick(60)
        pygame.mixer.music.stop()

    def splash_screen(self) -> None:
        """The splash screen. Shows the game studio logo.

        Returns:
            Nothing.
        """
        self.window.blit(pygame.transform.smoothscale(pygame.image.load(
            f"images{os.sep}Evil Panda Studios Logo.png").convert(), (self.WIDTH, self.HEIGHT)), (0, 0))
        pygame.display.update()
        pygame.time.wait(3000)

    def credit_screen(self) -> None:
        """The credit screen. Shows who worked on the game.

        Returns:
            Nothing.
        """
        self.window.fill((0, 0, 0))
        self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                             20).render("Credits", False, (255, 255, 255)), (360, 50))
        self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
            "Spieledesigner         Niklas", False, (255, 255, 255)), (100, 100))
        self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
            "Programmierer        Benjamin", False, (255, 255, 255)), (100, 150))
        self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
            "Grafiker                  Benjamin", False, (255, 255, 255)), (100, 200))
        self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
            "Komponist              Benjamin", False, (255, 255, 255)), (100, 250))
        self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
            "Leveldesigner          Niklas", False, (255, 255, 255)), (100, 300))
        self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
            "Tester 1                 Niklas", False, (255, 255, 255)), (500, 100))
        self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
            "Tester 2                 Benjamin", False, (255, 255, 255)), (500, 150))
        self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
            "Sounddesigner       Benjamin", False, (255, 255, 255)), (500, 200))
        self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
            "Produzent 1            Benjamin", False, (255, 255, 255)), (500, 250))
        self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif", 20).render(
            "Produzent 2            Niklas", False, (255, 255, 255)), (500, 300))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return


class Player(pygame.sprite.Sprite):
    """The player class."""

    def __init__(self, x: int, y: int, speed: int, firerate: int, color: str, left: int, right: int, up: int, down: int, fire: int) -> None:
        """Initializes the player.

        Arguments:
            x: the x coordinate.
            y: the y coordinate.
            speed: the speed of the player.
            firerate: the firerate of the player.
            color: the color of the player.
            left: the key for left.
            right: the key for right.
            up: the key for up.
            down: the key for down.
            fire: the key for firing.

        Returns:
            Nothing.
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f"images{os.sep}player_{str(color)}{os.sep}player_{str(color)}_up.png").convert_alpha(), pygame.image.load(f"images{os.sep}player_{str(color)}{os.sep}player_{str(color)}_left.png").convert_alpha(
        ), pygame.image.load(f"images{os.sep}player_{str(color)}{os.sep}player_{str(color)}_down.png").convert_alpha(), pygame.image.load(f"images{os.sep}player_{str(color)}{os.sep}player_{str(color)}_right.png").convert_alpha()]
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = 0
        self.firerate = firerate
        self.fire = 0
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.fire_key = fire

    def move(self, entities: list, HEIGHT: int, WIDTH: int,) -> None:
        """Moves the player based on user input.

        Arguments:
            entities: the other entitites in the game.
            HEIGHT: the height of the game window.
            WIDTH: the width of the game window.
            left: the id of the key for left movement.
            right: the id of the key for right movement.
            up: the id of the key for up movement.
            down: the id of the key for down movement.

        Returns:
            Nothing.
        """
        keys = pygame.key.get_pressed()
        if keys[self.up]:
            self.direction = 0
            self.rect.y -= self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.y <= 0:
                self.rect.y += self.speed
        elif keys[self.left]:
            self.direction = 1
            self.rect.x -= self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.x <= 0:
                self.rect.x += self.speed
        elif keys[self.down]:
            self.direction = 2
            self.rect.y += self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.y >= (HEIGHT - 32):
                self.rect.y -= self.speed
        elif keys[self.right]:
            self.direction = 3
            self.rect.x += self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.x >= (WIDTH - 32):
                self.rect.x -= self.speed

    def attack(self, bullets: list) -> None:
        """Shoots bullets based on user input.

        Arguments:
            bullets: all bullets in the game.

        Returns:
            Nothing.
        """
        keys = pygame.key.get_pressed()
        if keys[self.fire_key]:
            if self.fire == 0:
                self.fire = self.firerate
                bullets.append(
                    Bullet(self.rect.x, self.rect.y, 4, self.direction))
            else:
                self.fire -= 1
        else:
            self.fire = 0

    def update(self, window: pygame.Surface) -> None:
        """Draws the player on the screen.

        Arguments:
            window: the game window.

        Returns:
            Nothing.
        """
        window.blit(self.images[self.direction], (self.rect.x, self.rect.y))


class Bullet(pygame.sprite.Sprite):
    """Class for the bullet."""

    def __init__(self, x: int, y: int, speed: int, direction: int) -> None:
        """Initializes the bullet.

        Arguments:
            x: the x coordinate.
            y: the y coordinate.
            speed: the speed of the bullet.
            direction: the direction the bullet is facing.

        Returns:
            Nothing.
        """
        pygame.sprite.Sprite.__init__(self)
        images = {
            0: pygame.image.load(f"images{os.sep}bullet{os.sep}bullet_y.png").convert(),
            1: pygame.image.load(f"images{os.sep}bullet{os.sep}bullet_x.png").convert(),
            2: pygame.image.load(f"images{os.sep}bullet{os.sep}bullet_y.png").convert(),
            3: pygame.image.load(f"images{os.sep}bullet{os.sep}bullet_x.png").convert()
        }
        x_ = {
            0: x + 16,
            1: x,
            2: x + 16,
            3: x + 32
        }
        y_ = {
            0: y,
            1: y + 16,
            2: y + 32,
            3: y + 16
        }
        self.image = images[direction]
        self.rect = self.image.get_rect()
        self.rect.x = x_[direction]
        self.rect.y = y_[direction]
        self.speed = speed
        self.direction = direction
        pygame.mixer.Sound(f"sound{os.sep}shot_sound.wav").play()

    def move(self, bullets: list, walls: list, player_one: Player, player_two: Player, HEIGHT: int, WIDTH: int, window: pygame.Surface) -> typing.Union[None, int]:
        """Moves the bullet.

        Arguments:
            bullets: all bullets in the game.
            walls: all the walls in the game.
            player_one: the first player.
            player_two: the second player.
            HEIGHT: the height of the game window.
            WIDTH: the width of the game window.
            window: the game window.

        Returns:
            Nothing or the number of the player that was hit.
        """
        if self.direction == 0:
            self.rect.y -= self.speed
        elif self.direction == 1:
            self.rect.x -= self.speed
        elif self.direction == 2:
            self.rect.y += self.speed
        elif self.direction == 3:
            self.rect.x += self.speed
        if self.rect.x <= 0 or self.rect.x >= WIDTH or self.rect.y <= 0 or self.rect.y >= HEIGHT:
            bullets.remove(self)
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                bullets.remove(self)
        if self.rect.colliderect(player_one.rect):
            pygame.mixer.Sound(f"sound{os.sep}explosion_sound.wav").play()
            window.blit(pygame.image.load(
                f"images{os.sep}explosion.png").convert_alpha(), (self.rect.x, self.rect.y))
            return 2
        if self.rect.colliderect(player_two.rect):
            pygame.mixer.Sound(f"sound{os.sep}explosion_sound.wav").play()
            window.blit(pygame.image.load(
                f"images{os.sep}explosion.png").convert_alpha(), (self.rect.x, self.rect.y))
            return 1

    def update(self, window: pygame.Surface) -> None:
        """Draws the bullet on the screen.

        Arguments:
            window: the game window.

        Returns:
            Nothing or the number of the player that was hit.
        """
        window.blit(self.image, (self.rect.x, self.rect.y))


class Wall(pygame.sprite.Sprite):
    """Class for the wall."""

    def __init__(self, x: int, y: int, type_: str) -> None:
        """Initializes the wall.

        Arguments:
            x: the x coordinate.
            x: the y coordinate.
            type_: the type of wall.

        Returns:
            Nothing.
        """
        pygame.sprite.Sprite.__init__(self)
        images = {
            "I_x": pygame.image.load(f"images{os.sep}wall{os.sep}wall_I_x.png").convert(),
            "I_y": pygame.image.load(f"images{os.sep}wall{os.sep}wall_I_y.png").convert()
        }
        self.image = images[type_]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, window: pygame.Surface) -> None:
        """Draws the wall on the screen.

        Arguments:
            window: the game window.

        Returns:
            Nothing.
        """
        window.blit(self.image, (self.rect.x, self.rect.y))


class Color(enum.IntEnum):
    """The class for the colors."""
    blue = enum.auto()
    yellow = enum.auto()
    green = enum.auto()
    red = enum.auto()

    def __str__(self) -> str:
        """Returns string representation.

        Returns:
            The name of the color.
        """
        return self.name

    def next(self) -> enum.IntEnum:
        """Go to next color.

        Returns:
            The next color.
        """
        x = self.value + 1
        if x > len(Color):
            x = 1
        return Color(x)

    def previous(self) -> enum.IntEnum:
        """Go to previous color.

        Returns:
            The previous color.
        """
        x = self.value - 1
        if x < 1:
            x = len(Color)
        return Color(x)


class Menu(enum.IntEnum):
    """The class for the menu."""
    Start = enum.auto()
    Farbwahl = enum.auto()
    Optionen = enum.auto()
    Credits = enum.auto()
    Beenden = enum.auto()

    def __str__(self) -> str:
        """Returns string representation.

        Returns:
            The name of the menu item.
        """
        return self.name

    def next(self) -> enum.IntEnum:
        """Go to next menu item.

        Returns:
            The next menu item.
        """
        x = self.value + 1
        if x > len(Menu):
            x = 1
        return Menu(x)

    def previous(self) -> enum.IntEnum:
        """Go to previous menu item.

        Returns:
            The previous menu item.
        """
        x = self.value - 1
        if x < 1:
            x = len(Menu)
        return Menu(x)


Game().splash_screen()
Game().menu_screen()
