import pygame
from pygame.locals import *
from constants import *
from snake import Snake
import random
import sys

pygame.init()


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Slither.jar')
        self.font = pygame.font.SysFont('arial', 24)

        self.snakes = []
        self.food = [new_food()]
        self.state = 'start'
        self.score = 0

        for _ in range(FOOD_INIT):
            self.food.append(new_food())
        for _ in range(ENEMIES):
            self.snakes.append(self.new_enemy())

    @property
    def snake(self):
        return None if self.state == 'start' else self.snakes[0]

    def run(self):
        while True:
            self.handle_input()

            self.update()
            self.render()

            pygame.display.update()
            self.clock.tick(FPS)

    def update(self):
        for snake in self.snakes:
            if snake and snake.state != 'dead':
                self.ai(snake)
                snake.move()

                for enemy in self.snakes:
                    if snake is not self.snake and enemy is self.snake:
                        if BOOST_RADIUS ** 2 > (enemy.position - snake.position).mag_squared():
                            snake.boost()
                    if snake is not enemy and enemy.state != 'dead' and snake.collide_snake(enemy, snake is self.snake):
                        snake.die(self.food)
                        if snake is self.snake:
                            self.state = 'end'
                        else:
                            self.snakes.append(self.new_enemy())
                        break
                if snake.state == 'dead':
                    continue

                for food in self.food:
                    if snake.collide_circle(food):
                        snake.grow()
                        self.food.remove(food)

                        if snake is self.snake:
                            self.score += 1
                        if food.radius == FOOD_RADIUS:
                            self.food.append(new_food())
                        break

        self.snakes = [snake for snake in self.snakes if snake.state != 'dead' or snake is self.snake]

    def render(self):
        self.screen.fill(BLACK)
        for food in self.food:
            pygame.draw.circle(self.screen, food.colour, (food.position.x, food.position.y), food.radius)
        for snake in self.snakes[::-1]:
            snake.render(self.screen)

        if self.state == 'play':
            self.screen.blit(self.font.render(f'Score: {self.score}', 1, GREEN), TEXT)
        elif self.state == 'start':
            pygame.draw.circle(self.screen, FADED, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), BASE_SIZE)
            self.screen.blit(self.font.render('Press Any Key to Start...', 1, GREEN), TEXT)
        elif self.state == 'end':
            self.screen.blit(self.font.render('You Failed lol...', 1, WHITE), TEXT)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == MOUSEBUTTONUP:
                if self.state == 'start':
                    self.snakes.insert(0, Snake(Vector.t(pygame.mouse.get_pos())))
                    self.state = 'play'
                elif self.state == 'end':
                    self.state = 'start'
            elif event.type == QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        if self.snake:
            if pygame.mouse.get_pressed()[0]:
                self.snake.boost()
            self.snake.target = Vector.t(pygame.mouse.get_pos())

    def ai(self, snake):
        if snake is not self.snake and snake.position == snake.target:
            snake.target = self.next_food(snake.position)

    def new_enemy(self):
        position = Vector(random.randint(0, SCREEN_WIDTH-1), random.randint(0, SCREEN_HEIGHT-1))
        return Snake(position, random.choice(ENEMY_COLOURS), self.next_food(position))

    def next_food(self, position):
        for food in self.food:
            if AI_RADIUS ** 2 > (food.position - position).mag_squared():
                return food.position
        return random.choice(self.food).position


def new_food():
    return Circle(random.randint(0, SCREEN_WIDTH-1), random.randint(0, SCREEN_HEIGHT-1), FOOD_RADIUS)


game = Game()
game.run()
