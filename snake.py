import pygame as pg
import colors
import random


class Tail(pg.Rect):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.direction = ''
        self.turn = ''


class Snake:

    def __init__(self):
        self.FPS = 6
        self.screen = pg.display.set_mode((500, 500))
        self.auto_move = False
        self.game_over_screen = False
        self.ate_food = False
        self.last_move = 0
        self.score_counter = 0
        self.past_head_locations = []
        self.move_speed = (20, 20)
        self.background = colors.GRAY
        self.snake_head = pg.Rect(20, 20, 20, 20)
        self.snake_tail = []
        self.board_spaces = []
        self.used_spaces = []
        self.remaining_spaces = []
        self.food = pg.Rect(20, 20, 20, 20)
        self.game_speed = pg.time.Clock()
        self.running = True
        pg.display.set_caption('SNAKE')
        pg.font.init()
        self.score_font = pg.font.SysFont('Arial', 18)
        self.event_loop()

    def head_movement(self):              
        if self.last_move == pg.K_LEFT:
            self.past_head_locations.insert(0, (self.snake_head.x, self.snake_head.y, 'Left'))
            self.snake_head = self.snake_head.move(-20, 0)
            if self.snake_tail:
                self.tail_movement()
                self.check_tail_collision()
        elif self.last_move == pg.K_RIGHT:
            self.past_head_locations.insert(0, (self.snake_head.x, self.snake_head.y, 'Right'))
            self.snake_head = self.snake_head.move(20, 0)
            if self.snake_tail:
                self.tail_movement()
                self.check_tail_collision()
        elif self.last_move == pg.K_UP:
            self.past_head_locations.insert(0, (self.snake_head.x, self.snake_head.y, 'Up'))
            self.snake_head = self.snake_head.move(0, -20)
            if self.snake_tail:
                self.tail_movement()
                self.check_tail_collision()
        elif self.last_move == pg.K_DOWN:
            self.past_head_locations.insert(0, (self.snake_head.x, self.snake_head.y, 'Down'))
            self.snake_head = self.snake_head.move(0, 20)
            if self.snake_tail:
                self.tail_movement()
                self.check_tail_collision()
        self.check_wall_collision()
        self.check_food_collision()

    def tail_movement(self):
        self.used_spaces = []
        self.used_spaces.append((self.snake_head.x, self.snake_head.y))
        if self.snake_tail:
            for count, tail_segment in enumerate(self.snake_tail):
                tail_segment.x, tail_segment.y, tail_segment.direction = self.past_head_locations[count]
                prev_head_location_tuple = self.past_head_locations[count + 1]
                if tail_segment.direction != prev_head_location_tuple[2]:
                    self.determine_turn_direction(tail_segment, prev_head_location_tuple)
                else:
                    tail_segment.turn = ''
                self.used_spaces.append((tail_segment.x, tail_segment.y))
            self.find_remaining_spaces()

    @staticmethod
    def determine_turn_direction(tail_segment, prev_head_location_tuple):
        if tail_segment.direction == 'Left':
            if prev_head_location_tuple[2] == 'Up':
                tail_segment.turn = 'counterclockwise'
            elif prev_head_location_tuple[2] == 'Down':
                tail_segment.turn = 'clockwise'

        elif tail_segment.direction == 'Down':
            if prev_head_location_tuple[2] == 'Left':
                tail_segment.turn = 'counterclockwise'
            elif prev_head_location_tuple[2] == 'Right':
                tail_segment.turn = 'clockwise'

        elif tail_segment.direction == 'Up':
            if prev_head_location_tuple[2] == 'Left':
                tail_segment.turn = 'clockwise'
            elif prev_head_location_tuple[2] == 'Right':
                tail_segment.turn = 'counterclockwise'

        elif tail_segment.direction == 'Right':
            if prev_head_location_tuple[2] == 'Up':
                tail_segment.turn = 'clockwise'
            elif prev_head_location_tuple[2] == 'Down':
                tail_segment.turn = 'counterclockwise'

    def measure_board(self):
        for x in range(0, 500, 20):
            for y in range(0, 500, 20):
                self.board_spaces.append((x, y))

    def find_remaining_spaces(self):
        self.remaining_spaces = []
        for space in self.board_spaces:
            if space in self.used_spaces:
                pass
            else:
                self.remaining_spaces.append(space)

    def place_objects(self):
        self.snake_head.x = 240
        self.snake_head.y = 240
        self.tail_movement()
        self.find_remaining_spaces()
        self.place_new_food()

    def count_score(self):
        score = self.score_font.render(f'SCORE: {self.score_counter}', False, colors.WHITE)
        self.screen.blit(score, (410, 5))

    def draw_screen(self):
        if not self.ate_food:
            self.screen.fill(self.background)
            self.draw_head_red()
            self.draw_tail_red()
            pg.draw.rect(self.screen, colors.GREEN, self.food, 0)
            self.count_score()
            pg.display.update()
        else:
            self.screen.fill(self.background)
            self.draw_head_white()
            self.draw_tail_white()
            pg.draw.rect(self.screen, colors.GREEN, self.food, 0)
            self.count_score()
            pg.display.update()
            self.ate_food = False

    def draw_head_red(self):
        snake_head_image = pg.image.load('assets/Snake_Head_Red.png')
        if self.last_move == 0:
            self.screen.blit(snake_head_image, self.snake_head)
        elif self.last_move == pg.K_UP:
            self.screen.blit(snake_head_image, self.snake_head)
        elif self.last_move == pg.K_LEFT:
            snake_head_image = pg.transform.rotate(snake_head_image, 90)
            self.screen.blit(snake_head_image, self.snake_head)
        elif self.last_move == pg.K_DOWN:
            snake_head_image = pg.transform.rotate(snake_head_image, 180)
            self.screen.blit(snake_head_image, self.snake_head)
        elif self.last_move == pg.K_RIGHT:
            snake_head_image = pg.transform.rotate(snake_head_image, 270)
            self.screen.blit(snake_head_image, self.snake_head)

    def draw_tail_red(self):
        for count, tail in enumerate(self.snake_tail):
            snake_tail_image = pg.image.load('assets/Snake_Body_Red.png')
            clockwise_turn_image = pg.image.load('assets/Snake_Body_Right_Red.png')
            counterclockwise_turn_image = pg.image.load('assets/Snake_Body_Left_Red.png')
            tail_end_image = pg.image.load('assets/Snake_End_Red.png')

            if count == len(self.snake_tail) - 1:
                if tail.direction == 'Up':
                    tail_end_image = pg.transform.rotate(tail_end_image, 0)
                elif tail.direction == 'Right':
                    tail_end_image = pg.transform.rotate(tail_end_image, 270)
                elif tail.direction == 'Down':
                    tail_end_image = pg.transform.rotate(tail_end_image, 180)
                elif tail.direction == 'Left':
                    tail_end_image = pg.transform.rotate(tail_end_image, 90)
                self.screen.blit(tail_end_image, tail)

            elif tail.direction == 'Up':
                if tail.turn == 'clockwise':
                    clockwise_turn_image = pg.transform.rotate(clockwise_turn_image, 90)
                    self.screen.blit(clockwise_turn_image, tail)
                elif tail.turn == 'counterclockwise':
                    counterclockwise_turn_image = pg.transform.rotate(counterclockwise_turn_image, 270)
                    self.screen.blit(counterclockwise_turn_image, tail)
                elif tail.turn == '':
                    self.screen.blit(snake_tail_image, tail)

            elif tail.direction == 'Left':
                if tail.turn == 'clockwise':
                    clockwise_turn_image = pg.transform.rotate(clockwise_turn_image, 180)
                    self.screen.blit(clockwise_turn_image, tail)
                elif tail.turn == 'counterclockwise':
                    counterclockwise_turn_image = pg.transform.rotate(counterclockwise_turn_image, 0)
                    self.screen.blit(counterclockwise_turn_image, tail)
                elif tail.turn == '':
                    snake_tail_image = pg.transform.rotate(snake_tail_image, 90)
                    self.screen.blit(snake_tail_image, tail)

            elif tail.direction == 'Down':
                if tail.turn == 'clockwise':
                    clockwise_turn_image = pg.transform.rotate(clockwise_turn_image, 270)
                    self.screen.blit(clockwise_turn_image, tail)
                elif tail.turn == 'counterclockwise':
                    counterclockwise_turn_image = pg.transform.rotate(counterclockwise_turn_image, 90)
                    self.screen.blit(counterclockwise_turn_image, tail)
                elif tail.turn == '':

                    snake_tail_image = pg.transform.rotate(snake_tail_image, 180)
                    self.screen.blit(snake_tail_image, tail)

            elif tail.direction == 'Right':
                if tail.turn == 'clockwise':
                    clockwise_turn_image = pg.transform.rotate(clockwise_turn_image, 0)
                    self.screen.blit(clockwise_turn_image, tail)
                elif tail.turn == 'counterclockwise':
                    counterclockwise_turn_image = pg.transform.rotate(counterclockwise_turn_image, 180)
                    self.screen.blit(counterclockwise_turn_image, tail)
                elif tail.turn == '':
                    snake_tail_image = pg.transform.rotate(snake_tail_image, 270)
                    self.screen.blit(snake_tail_image, tail)

    def draw_head_white(self):
        snake_head_image = pg.image.load('assets/Snake_Head_White.png')
        if self.last_move == 0:
            self.screen.blit(snake_head_image, self.snake_head)
        elif self.last_move == pg.K_UP:
            self.screen.blit(snake_head_image, self.snake_head)
        elif self.last_move == pg.K_LEFT:
            snake_head_image = pg.transform.rotate(snake_head_image, 90)
            self.screen.blit(snake_head_image, self.snake_head)
        elif self.last_move == pg.K_DOWN:
            snake_head_image = pg.transform.rotate(snake_head_image, 180)
            self.screen.blit(snake_head_image, self.snake_head)
        elif self.last_move == pg.K_RIGHT:
            snake_head_image = pg.transform.rotate(snake_head_image, 270)
            self.screen.blit(snake_head_image, self.snake_head)

    def draw_tail_white(self):
        for count, tail in enumerate(self.snake_tail):
            snake_tail_image = pg.image.load('assets/Snake_Body_White.png')
            clockwise_turn_image = pg.image.load('assets/Snake_Body_Right_White.png')
            counterclockwise_turn_image = pg.image.load('assets/Snake_Body_Left_White.png')
            tail_end_image = pg.image.load('assets/Snake_End_White.png')

            if count == len(self.snake_tail) - 1:
                if tail.direction == 'Up':
                    tail_end_image = pg.transform.rotate(tail_end_image, 0)
                elif tail.direction == 'Right':
                    tail_end_image = pg.transform.rotate(tail_end_image, 270)
                elif tail.direction == 'Down':
                    tail_end_image = pg.transform.rotate(tail_end_image, 180)
                elif tail.direction == 'Left':
                    tail_end_image = pg.transform.rotate(tail_end_image, 90)
                self.screen.blit(tail_end_image, tail)

            elif tail.direction == 'Up':
                if tail.turn == 'clockwise':
                    clockwise_turn_image = pg.transform.rotate(clockwise_turn_image, 90)
                    self.screen.blit(clockwise_turn_image, tail)
                elif tail.turn == 'counterclockwise':
                    counterclockwise_turn_image = pg.transform.rotate(counterclockwise_turn_image, 270)
                    self.screen.blit(counterclockwise_turn_image, tail)
                elif tail.turn == '':
                    self.screen.blit(snake_tail_image, tail)

            elif tail.direction == 'Left':
                if tail.turn == 'clockwise':
                    clockwise_turn_image = pg.transform.rotate(clockwise_turn_image, 180)
                    self.screen.blit(clockwise_turn_image, tail)
                elif tail.turn == 'counterclockwise':
                    counterclockwise_turn_image = pg.transform.rotate(counterclockwise_turn_image, 0)
                    self.screen.blit(counterclockwise_turn_image, tail)
                elif tail.turn == '':
                    snake_tail_image = pg.transform.rotate(snake_tail_image, 90)
                    self.screen.blit(snake_tail_image, tail)

            elif tail.direction == 'Down':
                if tail.turn == 'clockwise':
                    clockwise_turn_image = pg.transform.rotate(clockwise_turn_image, 270)
                    self.screen.blit(clockwise_turn_image, tail)
                elif tail.turn == 'counterclockwise':
                    counterclockwise_turn_image = pg.transform.rotate(counterclockwise_turn_image, 90)
                    self.screen.blit(counterclockwise_turn_image, tail)
                elif tail.turn == '':

                    snake_tail_image = pg.transform.rotate(snake_tail_image, 180)
                    self.screen.blit(snake_tail_image, tail)

            elif tail.direction == 'Right':
                if tail.turn == 'clockwise':
                    clockwise_turn_image = pg.transform.rotate(clockwise_turn_image, 0)
                    self.screen.blit(clockwise_turn_image, tail)
                elif tail.turn == 'counterclockwise':
                    counterclockwise_turn_image = pg.transform.rotate(counterclockwise_turn_image, 180)
                    self.screen.blit(counterclockwise_turn_image, tail)
                elif tail.turn == '':
                    snake_tail_image = pg.transform.rotate(snake_tail_image, 270)
                    self.screen.blit(snake_tail_image, tail)

    def check_wall_collision(self):
        if self.snake_head.left < 0:
            self.running = False
            self.game_over_screen = True
        elif self.snake_head.right > 500:
            self.running = False
            self.game_over_screen = True
        elif self.snake_head.top < 0:
            self.running = False
            self.game_over_screen = True
        elif self.snake_head.bottom > 500:
            self.running = False
            self.game_over_screen = True
        else:
            pass

    def check_food_collision(self):
        if self.snake_head.left == self.food.left:
            if self.snake_head.right == self.food.right:
                if self.snake_head.top == self.food.top:
                    if self.snake_head.bottom == self.food.bottom:
                        self.eat_food()

    def check_tail_collision(self):
        for tail_segment in self.snake_tail:
            if self.snake_head.top == tail_segment.top:
                if self.snake_head.bottom == tail_segment.bottom:
                    if self.snake_head.left == tail_segment.left:
                        if self.snake_head.right == tail_segment.right:
                            self.running = False
                            self.game_over_screen = True

    def add_tail(self):
        tail = Tail(20, 20, 20, 20)
        self.snake_tail.append(tail)
        self.tail_movement()

    def place_new_food(self):
        food_location = random.choice(self.remaining_spaces)
        self.food.x, self.food.y = food_location

    def eat_food(self):
        self.add_tail()
        self.place_new_food()
        self.ate_food = True
        self.score_counter += 1

    def draw_game_over(self):
        self.screen.fill(self.background)
        end_screen = pg.image.load('assets/placeholder end screen.png')
        game_over_rect = end_screen.get_rect()
        self.screen.blit(end_screen, game_over_rect)
        pg.display.update()

    def event_loop(self):
        pg.init()
        self.measure_board()
        self.place_objects()
        while self.running:
            self.draw_screen()
            self.game_speed.tick(self.FPS)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key in [pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT]:
                    self.auto_move = True
                    self.last_move = event.key
                elif event.type == pg.QUIT:
                    self.running = False
            if self.auto_move:
                self.head_movement()

        while self.game_over_screen:
            self.draw_game_over()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_over_screen = False
        pg.quit()
