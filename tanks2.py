import json
import os
import typing

import pygame


class Game:
    """The game class."""

    def __init__(self) -> None:
        """Initializes the game."""
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
        self.level_number = 1
        self.debug = False
        self.invulnerable = False
        with open("config.json", "r") as f:
            self.config = json.load(f)
        pygame.display.set_caption("Tanks2")
        pygame.display.set_icon(pygame.image.load(
            f"images{os.sep}icon.png").convert_alpha())

    def load_level(self) -> None:
        """Loads levels."""
        if not os.path.isfile(f"levels{os.sep}level_{self.level_number}.json"):
            self.level_number = 1
            self.credit_screen()
        with open(f"levels{os.sep}level_{self.level_number}.json", "r") as f:
            level = json.load(f)
        self.player_one = Player_Blue(
            level["spawn_one"][0], level["spawn_one"][1], self.config["speed"], self.config["firerate"])
        self.player_two = Player_Yellow(
            level["spawn_two"][0], level["spawn_two"][1], self.config["speed"], self.config["firerate"])
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
        """The main loop of the game."""
        self.load_level()
        dead = False
        pygame.mixer.music.load(f"sound{os.sep}background_song.wav")
        pygame.mixer.music.play(-1)
        while True:
            self.window.fill((190, 190, 190))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
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
                if dead:
                    self.result_screen(dead)
            for wall in self.walls:
                wall.update(self.window)
            pygame.display.update()
            self.clock.tick(self.config["fps"])

    def menu_screen(self) -> None:
        """The menu screen. Allows either starting the game or quitting it."""
        menu = True
        start = True
        pygame.mixer.music.load(f"sound{os.sep}menu_song.wav")
        pygame.mixer.music.play(-1)
        while menu:
            self.window.fill((190, 190, 190))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        start = not start
                    elif event.key == pygame.K_DOWN:
                        start = not start
                    elif event.key == pygame.K_RETURN:
                        if start:
                            menu = False
                        else:
                            pygame.quit()
                            quit()
            self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                 40).render("Tanks 2", False, (0, 0, 255)), (360, 70))
            if start:
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Starten", False, (0, 0, 150)), (380, 150))
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Beenden", False, (0, 0, 0)), (380, 200))
            else:
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Starten", False, (0, 0, 0)), (380, 150))
                self.window.blit(pygame.font.SysFont("Arial, Helvetica, sans-serif",
                                                     20).render("Beenden", False, (0, 0, 150)), (380, 200))
            pygame.display.update()
            self.clock.tick(60)
        pygame.mixer.music.stop()
        self.game_loop()

    def result_screen(self, player: int) -> None:
        """The result screen. Shows who has won."""
        self.level_number += 1
        winner = True
        ok = True
        pygame.mixer.music.load(f"sound{os.sep}winner_song.wav")
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
        self.game_loop()

    def splash_screen(self) -> None:
        """The splash screen. Shows the game studio logo."""
        self.window.blit(pygame.transform.smoothscale(pygame.image.load(
            f"images{os.sep}Evil Panda Studios Logo.png").convert(), (self.WIDTH, self.HEIGHT)), (0, 0))
        pygame.display.update()
        pygame.time.wait(3000)
        self.menu_screen()

    def credit_screen(self) -> None:
        """The credit screen. Shows who worked on the game."""
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
            "Produzent              Benjamin", False, (255, 255, 255)), (500, 250))
        pygame.display.update()
        pygame.time.wait(7000)
        self.menu_screen()


class Player(pygame.sprite.Sprite):
    """The player base class."""

    def __init__(self, x: int, y: int, speed: int, firerate: int, images: list) -> None:
        """Initializes the player."""
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.rect = self.images[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = 0
        self.firerate = firerate
        self.fire = 0

    def move(self, entities: list, HEIGHT: int, WIDTH: int, left: int, right: int, up: int, down: int) -> None:
        """Moves the player based on user input."""
        keys = pygame.key.get_pressed()
        if keys[up]:
            self.direction = 0
            self.rect.y -= self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.y <= 0:
                self.rect.y += self.speed
        elif keys[left]:
            self.direction = 1
            self.rect.x -= self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.x <= 0:
                self.rect.x += self.speed
        elif keys[down]:
            self.direction = 2
            self.rect.y += self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.y >= (HEIGHT - 32):
                self.rect.y -= self.speed
        elif keys[right]:
            self.direction = 3
            self.rect.x += self.speed
            if any(self.rect.colliderect(entity.rect) for entity in entities if entity != self) or self.rect.x >= (WIDTH - 32):
                self.rect.x -= self.speed

    def attack(self, bullets: list, fire: int) -> None:
        """Shoots bullets based on user input."""
        keys = pygame.key.get_pressed()
        if keys[fire]:
            if self.fire == 0:
                self.fire = self.firerate
                bullets.append(
                    Bullet(self.rect.x, self.rect.y, 4, self.direction))
            else:
                self.fire -= 1
        else:
            self.fire = 0

    def update(self, window: pygame.Surface) -> None:
        """Draws the player on the screen."""
        window.blit(self.images[self.direction], (self.rect.x, self.rect.y))


class Player_Blue(Player):
    """Class for the blue player. Inherits from the player class."""

    def __init__(self, x: int, y: int, speed: int, firerate: int) -> None:
        """Initializes the blue player. Calls the inherited function."""
        super().__init__(x, y, speed, firerate, [pygame.image.load(f"images{os.sep}player_blue{os.sep}player_blue_up.png").convert_alpha(), pygame.image.load(f"images{os.sep}player_blue{os.sep}player_blue_left.png").convert_alpha(
        ), pygame.image.load(f"images{os.sep}player_blue{os.sep}player_blue_down.png").convert_alpha(), pygame.image.load(f"images{os.sep}player_blue{os.sep}player_blue_right.png").convert_alpha()])

    def move(self, entities: list, HEIGHT: int, WIDTH: int) -> None:
        """Moves the blue player based on user input. Calls the inherited function."""
        super().move(entities, HEIGHT, WIDTH, ord("a"), ord("d"), ord("w"), ord("s"))

    def attack(self, bullets: list) -> None:
        """Shoots bullets based on user input. Calls the inherited function."""
        return super().attack(bullets, ord("f"))


class Player_Yellow(Player):
    """Class for the yellow player. Inherits from the player class."""

    def __init__(self, x: int, y: int, speed: int, firerate: int) -> None:
        """Initializes the yellow player. Calls the inherited function."""
        super().__init__(x, y, speed, firerate, [pygame.image.load(f"images{os.sep}player_yellow{os.sep}player_yellow_up.png").convert_alpha(), pygame.image.load(f"images{os.sep}player_yellow{os.sep}player_yellow_left.png").convert_alpha(
        ), pygame.image.load(f"images{os.sep}player_yellow{os.sep}player_yellow_down.png").convert_alpha(), pygame.image.load(f"images{os.sep}player_yellow{os.sep}player_yellow_right.png").convert_alpha()])

    def move(self, entities: list, HEIGHT: int, WIDTH: int) -> None:
        """Moves the yellow player based on user input. Calls the inherited function."""
        super().move(entities, HEIGHT, WIDTH, pygame.K_LEFT,
                     pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

    def attack(self, bullets: list) -> None:
        """Shoots bullets based on user input. Calls the inherited function."""
        return super().attack(bullets, ord("l"))


class Bullet(pygame.sprite.Sprite):
    """Class for the bullet."""

    def __init__(self, x: int, y: int, speed: int, direction: int) -> None:
        """Initializes the bullet."""
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

    def move(self, bullets: list, walls: list, player_one: Player_Blue, player_two: Player_Yellow, HEIGHT: int, WIDTH: int, window: pygame.Surface) -> typing.Union[None, int]:
        """Moves the bullet."""
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
        """Draws the bullet on the screen."""
        window.blit(self.image, (self.rect.x, self.rect.y))


class Wall(pygame.sprite.Sprite):
    """Class for the wall."""

    def __init__(self, x: int, y: int, type_: str) -> None:
        """Initializes the wall."""
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
        """Draws the wall on the screen."""
        window.blit(self.image, (self.rect.x, self.rect.y))


Game().splash_screen()
