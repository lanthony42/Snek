import pygame
import random
from constants import *


class Snake:
    def __init__(self, start: Vector = START, colour=BLUE, target: Vector = START):
        self.body = [start.copy()]
        self.speed_factor = 1.0
        self.colour = colour

        self.direction = Vector()
        self.target = target
        self.state = 'main'

    @property
    def speed(self):
        return BASE_SPEED * self.speed_factor

    @property
    def radius(self):
        return BASE_SIZE + len(self.body) // SIZE_INC

    @property
    def position(self):
        return self.body[0]

    def gradient(self, i):
        boost = BOOST_OFFSET if self.speed_factor == BOOST_FACTOR else 0
        if i // PING_PONG % 2 == 1:
            i = PING_PONG - i % PING_PONG
        else:
            i %= PING_PONG
        r = min(max(self.colour[0] + i + boost, 0), 255)
        g = min(max(self.colour[1] + i + boost, 0), 255)
        b = min(max(self.colour[2] + i + boost, 0), 255)

        return r, g, b

    def __str__(self):
        return f'Snake(position={self.position}, length={len(self.body)}, state={self.state})'

    __repr__ = __str__

    def render(self, screen):
        if self.state == 'dead':
            return
        for i, vector in list(enumerate(self.body))[::-1]:
            pygame.draw.circle(screen, self.gradient(i), (round(vector.x), round(vector.y)), self.radius)

        direct = self.position - (self.body[1] if len(self.body) > 1 else self.target)
        for b in (True, False):
            offset = direct.perpendicular(b) * (self.radius // 2)
            pygame.draw.circle(screen, WHITE, (self.position + offset).tuple(), EYE_SIZE + len(self.body) // EYE_INC)
            pygame.draw.circle(screen, BLACK, (self.position + offset).tuple(), PUPIL_SIZE + len(self.body)
                               // PUPIL_INC)

    def move(self):
        if self.state == 'boost':
            if pygame.time.get_ticks() % BOOST_DCR == 0:
                self.body.pop()
            self.speed_factor = BOOST_FACTOR
        else:
            self.speed_factor = 1

        moved, self.direction = self.body[0].lerp(self.target, self.speed)

        for i in range(1, len(self.body)):
            _, self.direction = self.body[i].lerp(self.body[i-1], moved, MAX_DISTANCE)

        self.state = 'main'

    def grow(self):
        if self.state == 'dead':
            return
        for _ in range(len(self.body) // GROWTH_INC + 1):
            self.body.append(self.body[len(self.body) - 1] - self.direction.normalized() * MIN_DISTANCE)

    def boost(self):
        if self.state == 'dead':
            return
        if len(self.body) > BOOST_MIN:
            self.state = 'boost'

    def collide_snake(self, other, head=False):
        for piece in other.body[0 if head else 1:]:
            min_length = self.radius + other.radius
            difference = (self.position - piece).mag_squared()
            if min_length ** 2 >= difference:
                return True
        return False

    def collide_circle(self, other: Circle):
        min_length = self.radius + other.radius
        difference = (self.position - other.position).mag_squared()
        return min_length ** 2 >= difference

    def die(self, foods):
        for i, piece in list(enumerate(self.body))[::-FOOD_DEATH]:
            foods.append(Circle(round(piece.x) + random.randint(0, self.radius),
                                round(piece.y) + random.randint(0, self.radius),
                                DEAD_FOOD_RADIUS, colour=self.gradient(i)))
        self.state = 'dead'
