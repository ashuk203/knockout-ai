# Defining instance of a knockout game
import random

import pygame
from pygame.key import *
from pygame.locals import *
from pygame.color import *

import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

class Knockout(object):
    def _init_space(self):
        self._space = pymunk.Space()
        self._space.damping = 0.5

    def __init__(self, player1, player2, animate=False):
        self._animate = animate
        # self._animate = False

        #self._num_penguins = num_penguins

        self._init_space()
        self._dt = [0.2, 0.05][animate]
        self._image_idx = 0

        self._board_dim = 400
        self._penguins = []
        self.p1 = []
        self.p2 = []
        #self._generate_random_layout()
        self._setUp(player1, player2)
        self._running = True

        # pygame
        if self._animate:
            pygame.init()
            self._screen = pygame.display.set_mode((self._board_dim, self._board_dim))
            self._clock = pygame.time.Clock()

            self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)


    def get_positions(self):
        return list(map(lambda s : list(s.body.position), self._penguins))


    def _setUp(self, player1, player2):
        for p,v in player1.toArray():
            mass = 15
            radius = 15
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            body.position = p
            body.velocity = v
            shape = pymunk.Circle(body, radius, (0, 0))
            shape.elasticity = 0.95
            shape.friction = 1
            self._space.add(body, shape)
            self._penguins.append(shape)
            self.p1.append(body)
        for p, v in player2.toArray():
            mass = 15
            radius = 15
            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)
            body.position = p
            body.velocity = v
            shape = pymunk.Circle(body, radius, (0, 0))
            shape.elasticity = 0.95
            shape.friction = 1
            self._space.add(body, shape)
            self._penguins.append(shape)
            self.p2.append(body)

    def _generate_random_layout(self):
        for i in range(2 * self._num_penguins):
            mass = 15
            radius = 15
            lower_spawn_pos = 0.25 * self._board_dim
            upper_spawn_pos = 0.75 * self._board_dim
            center = 0.5 * self._board_dim
            collision_point = Vec2d(center, center)


            inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
            body = pymunk.Body(mass, inertia)

            y = [lower_spawn_pos, upper_spawn_pos][i % 2]
            # x = lower_spawn_pos + (center / (self._num_penguins - 1)) * (i // 2)
            x = random.randint(lower_spawn_pos, upper_spawn_pos)

            body.position = x, y
            body.velocity = collision_point - body.position

            shape = pymunk.Circle(body, radius, (0, 0))
            shape.elasticity = 0.95
            shape.friction = 1

            self._space.add(body, shape)
            self._penguins.append(shape)

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self._running = False
                elif event.key == K_p:
                    self.save_pic()
                elif event.key == K_r:
                    # self._dt += 0.05
                    self._init_space()
                    self._penguins.clear()
                    self._generate_random_layout()

    def run(self):
        # Main loop
        while self._running:
            self._space.step(self._dt)

            if self._animate:
                self._process_events()
                self._clear_screen()
                self._draw_objects()
                pygame.display.flip()
                pygame.display.set_caption("Press 'r' to restart demo and esc to quit")
            if self._check_stopped():
                self._running = False
        p1 = Player()
        for p in self.p1:
            p1.ps.append(p.position)
            p1.vs.append((0,0))
        self.check_alive(p1)
        p2 = Player()
        for p in self.p2:
            p2.ps.append(p.position)
            p2.vs.append((0, 0))
        self.check_alive(p2)
        return p1,p2

    def save_pic(self):
        pygame.image.save(self._screen, "bouncing_balls " + str(self._image_idx) + ".png")
        self._image_idx += 1

    def _check_stopped(self):
        return all(map(lambda x: x.body.velocity.get_length_sqrd() == 0, self._penguins))

    def _clear_screen(self):
        self._screen.fill(THECOLORS["white"])

    def _draw_objects(self):
        self._space.debug_draw(self._draw_options)

    def check_alive(self, player):
        for p in player.ps:
            if not (0 < p[0] < self._board_dim) or not (0 < p[1] < self._board_dim):
                p[0] = -1000
                p[1] = -1000


class Player():
    def __init__(self):
        self.ps = []
        self.vs = []

    def toArray(self):
        return zip(self.ps, self.vs)

    def copy(self):
        n = Player()
        n.ps = self.ps.copy()
        n.vs = self.vs.copy()
        return n


def step(p1, p2):
    game = Knockout(p1, p2, False)
    return game.run()

if __name__ == '__main__':
    p1 = Player()
    p1.ps.append((50,50))
    p1.vs.append((100,100))
    p2 = Player()
    p2.ps.append((100, 100))
    p2.vs.append((-100, -100))
    p1, p2 = step(p1, p2)
    for p, v in p2.toArray():
        print(p, v)

