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

    def __init__(self, num_penguins, animate=False):
        self._animate = animate
        # self._animate = False

        self._num_penguins = num_penguins

        self._init_space()
        self._dt = [0.2, 0.05][animate]
        self._image_idx = 0

        self._board_dim = 400
        self._penguins = []
        self._generate_random_layout()

        self._running = True

        # pygame
        if self._animate:
            pygame.init()
            self._screen = pygame.display.set_mode((self._board_dim, self._board_dim))
            self._clock = pygame.time.Clock()

            self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)


    def get_positions(self):
        return list(map(lambda s : list(s.body.position), self._penguins))

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
            elif self._check_stopped():
                self._running = False

    def save_pic(self):
        pygame.image.save(self._screen, "bouncing_balls " + str(self._image_idx) + ".png")
        self._image_idx += 1

    def _check_stopped(self):
        return all(map(lambda x: x.body.velocity.get_length_sqrd() == 0, self._penguins))

    def _clear_screen(self):
        self._screen.fill(THECOLORS["white"])

    def _draw_objects(self):
        self._space.debug_draw(self._draw_options)


if __name__ == '__main__':
    game = Knockout(4, True)
    game.run()
