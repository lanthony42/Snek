import math

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
TEXT = (5, 5)
FPS = 60

BASE_SIZE = 10
EYE_SIZE = 4
PUPIL_SIZE = EYE_SIZE - 2
BASE_SPEED = 2
MIN_DISTANCE = 1
MAX_DISTANCE = MIN_DISTANCE + 3
SIZE_INC = 15
EYE_INC = SIZE_INC * 4
PUPIL_INC = SIZE_INC * 8
GROWTH_INC = SIZE_INC * 20

BOOST_MIN = 10
BOOST_FACTOR = 2
BOOST_DCR = 5
ENEMIES = 5
AI_RADIUS = 150
BOOST_RADIUS = 100

FOOD_RADIUS = 5
DEAD_FOOD_RADIUS = FOOD_RADIUS + 1
FOOD_INIT = 150
FOOD_DEATH = 4
FOOD_COLOUR = (240, 40, 40)

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
FADED = (60, 60, 160)
GREEN = (30, 180, 30)
RED = (240, 0, 0)
PURPLE = (160, 30, 160)
YELLOW = (215, 215, 70)
TAN = (215, 125, 70)
WHITE = (220, 220, 220)

ENEMY_COLOURS = [RED, GREEN, PURPLE, YELLOW, TAN]
BOOST_OFFSET = 40
PING_PONG = 100


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    @staticmethod
    def t(vector):
        return Vector(vector[0], vector[1])

    def tuple(self):
        return round(self.x), round(self.y)

    def copy(self):
        return Vector(self.x, self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other: float):
        return Vector(self.x * other, self.y * other)

    def __imul__(self, other: float):
        self.x *= other
        self.y *= other
        return self

    def __truediv__(self, other: float):
        return Vector(self.x / other, self.y / other)

    def __itruediv__(self, other: float):
        self.x /= other
        self.y /= other
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

    __repr__ = __str__

    def mag_squared(self):
        return self.x ** 2 + self.y ** 2

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self):
        mag = self.mag()
        if mag > 0:
            return Vector(self.x / mag, self.y / mag)
        else:
            return Vector()

    def normalize(self):
        mag = self.mag()
        if mag > 0:
            self.x /= mag
            self.y /= mag
        else:
            return self

    def perpendicular(self, first=True):
        return Vector(-self.y if first else self.y, self.x if first else -self.x).normalized()

    def lerp(self, target, distance, gap=0):
        direction = target - self
        mag = direction.mag()

        if gap > 0:
            mag -= gap
            direction.normalize()
            direction *= mag

        if mag <= 0:
            return 0, Vector()
        elif mag < distance:
            self.x += direction.x
            self.y += direction.y
            return mag, direction
        else:
            direction *= distance / mag
            self.x += direction.x
            self.y += direction.y
            return distance, direction


class Circle:
    def __init__(self, x=0.0, y=0.0, radius=1, position: Vector = None, colour=FOOD_COLOUR):
        if position is not None:
            self.position = position
        else:
            self.position = Vector(x, y)

        self.radius = radius
        self.colour = colour

    def __str__(self):
        return f'Circle(position={self.position}, radius={self.radius}, colour={self.colour})'

    __repr__ = __str__


START = Vector(BASE_SIZE * 2, SCREEN_HEIGHT // 2)
