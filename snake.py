import pygame as pg
import colors
import random

class Snake:

    def __init__(self):
        self.FPS = 6
        self.screen = pg.display.set_mode((500, 500))
        self.auto_move = False
        self.game_over_screen = False
        self.last_move = 0
        self.score_counter = 0
        self.past_head_locations = []
        self.move_speed = (20, 20)
        self.background = colors.BLACK
        self.snake_color = colors.RED
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
            self.past_head_locations.insert(0, (self.snake_head.x, self.snake_head.y))
            self.snake_head = self.snake_head.move(-20, 0)
            if self.snake_tail:
                self.tail_movement()
                self.check_tail_collision()
        elif self.last_move == pg.K_RIGHT:
            self.past_head_locations.insert(0, (self.snake_head.x, self.snake_head.y))
            self.snake_head = self.snake_head.move(20, 0)
            if self.snake_tail:
                self.tail_movement()
                self.check_tail_collision()
        elif self.last_move == pg.K_UP:
            self.past_head_locations.insert(0, (self.snake_head.x, self.snake_head.y))
            self.snake_head = self.snake_head.move(0, -20)
            if self.snake_tail:
                self.tail_movement()
                self.check_tail_collision()
        elif self.last_move == pg.K_DOWN:
            self.past_head_locations.insert(0, (self.snake_head.x, self.snake_head.y))
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
                tail_segment.x, tail_segment.y = self.past_head_locations[count]
                self.used_spaces.append((tail_segment.x, tail_segment.y))
            self.find_remaining_spaces()


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
        self.screen.fill(self.background)
        pg.draw.rect(self.screen, colors.GREEN, self.food, 0)
        pg.draw.rect(self.screen, self.snake_color, self.snake_head, 0)
        for tail in self.snake_tail:
            pg.draw.rect(self.screen, self.snake_color, tail, 0)
        self.count_score()
        pg.display.update()
        self.snake_color = colors.RED


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
        tail = pg.Rect(20, 20, 20, 20)
        self.snake_tail.append(tail)
        self.tail_movement()


    def place_new_food(self):
        food_location = random.choice(self.remaining_spaces)
        self.food.x, self.food.y = food_location


    def eat_food(self):
        self.add_tail()
        self.place_new_food()
        self.score_counter += 1
        self.snake_color = colors.WHITE


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
            if self.auto_move == True:
                self.head_movement()

        while self.game_over_screen:
            self.draw_game_over()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_over_screen = False
        pg.quit()


if __name__ == '__main__':

    Snake()



