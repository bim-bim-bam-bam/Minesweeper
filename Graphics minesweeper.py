import arcade
from random import randrange

SCREEN_WIDTH = 1250
SCREEN_HEIGHT = 850
TITLE = "Minesweeper"

FIELD_WIDTH = 35
FIELD_HEIGHT = 35
BOMBS_COUNT = 160
SQUARE_SIZE = 20
flags_left = BOMBS_COUNT
game_over = False

BUTTON_SIZE = 40

number_textures = {0: "Sprites/empty square.png",
                   1: "Sprites/one.png",
                   2: "Sprites/two.png",
                   3: "Sprites/three.png",
                   4: "Sprites/four.png",
                   5: "Sprites/five.png",
                   6: "Sprites/six.png",
                   7: "Sprites/seven.png",
                   8: "Sprites/eight.png"}

mode_button_sprites = {True: "Sprites/simple bomb.png",
                       False: "Sprites/flag.png"}


def is_on_field(x, y):
    if (0 <= x < FIELD_WIDTH) and (0 <= y < FIELD_HEIGHT):
        return True
    else:
        return False


class Square:
    def __init__(self, row, col, x, y):
        self.opened = False
        self.flagged = False
        self.bombed = False
        self.number = 0
        self.row = row
        self.col = col
        self.sprite_x = x
        self.sprite_y = y
        self.scale_k = SQUARE_SIZE / 32

    def checking(self, field):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if is_on_field(self.col + dc, self.row + dr) and field[self.row + dr][self.col + dc].get_bombed():
                    self.number += 1

    def get_bombed(self):
        return self.bombed

    def set_bomb(self):
        self.bombed = True

    def get_opened(self):
        return self.opened

    def get_flagged(self):
        return self.flagged

    def print_square(self):
        # print(scale_k)
        if game_over and self.bombed:
            if self.opened:
                sprite = arcade.Sprite("Sprites/activated bomb.png", scale=self.scale_k)
                # print("# ", end="")
            else:
                sprite = arcade.Sprite("Sprites/simple bomb.png", scale=self.scale_k)
                # print("* ", end="")
        elif self.flagged:
            sprite = arcade.Sprite("Sprites/flag.png", scale=self.scale_k)
            # print("! ", end="")
        elif self.opened:
            sprite = arcade.Sprite(number_textures[self.number], scale=self.scale_k)
            # print(self.number, "", end="")
        else:
            sprite = arcade.Sprite("Sprites/closed sell.png", scale=self.scale_k)
            # print("= ", end="")
        sprite.center_x = self.sprite_x
        sprite.center_y = self.sprite_y
        return sprite

    def open_square(self, field):
        # print("Открываем клетку -", self.col, self.row)
        global game_over, flags_left

        if self.bombed:
            print(self.col, self.row)
            self.opened = True
            game_over = True

        elif self.flagged:
            flags_left += 1
            self.flagged = False

        elif self.opened:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if is_on_field(self.col + dc, self.row + dr) and not field[self.row + dr][self.col + dc].get_opened() and not field[self.row + dr][self.col + dc].get_flagged():
                        field[self.row + dr][self.col + dc].open_square(field)

        self.opened = True

        if self.number == 0:
            #print("my coords =", self.row, self.col)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if is_on_field(self.col + dc, self.row + dr) and not field[self.row + dr][self.col + dc].get_opened():
                        field[self.row + dr][self.col + dc].open_square(field)

    def set_flag(self):
        global flags_left
        if not self.opened:
            if self.flagged:
                flags_left += 1
            else:
                flags_left -= 1
            self.flagged = not self.flagged


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.WHITE)

        self.field_screen_width = FIELD_WIDTH * SQUARE_SIZE
        self.field_screen_height = FIELD_HEIGHT * SQUARE_SIZE
        self.field_x = (SCREEN_WIDTH - self.field_screen_width) // 2
        self.field_y = (SCREEN_HEIGHT - self.field_screen_height) // 2
        # print(self.field_start_y)

        self.field = []
        for row in range(FIELD_HEIGHT):
            self.field.append([])
            for col in range(FIELD_WIDTH):
                square = Square(row,
                                col,
                                self.field_x + (col * SQUARE_SIZE) + (SQUARE_SIZE / 2),
                                self.field_y + (row * SQUARE_SIZE) + (SQUARE_SIZE / 2))
                self.field[row].append(square)

        self.first_click = True
        self.mode = True

        self.button_sprite_list = arcade.SpriteList()

        self.mode_button_x = self.field_x + self.field_screen_width - (BUTTON_SIZE / 2)
        print(self.mode_button_x)
        self.mode_button_y = (self.field_y * 1.5) + self.field_screen_height
        print(self.mode_button_y)
        self.restart_button_x = SCREEN_WIDTH / 2
        self.restart_button_y = self.mode_button_y

        self.mode_button_sprite = arcade.Sprite(mode_button_sprites[True], scale=BUTTON_SIZE / 32)
        self.mode_button_sprite.center_x = self.mode_button_x
        self.mode_button_sprite.center_y = self.mode_button_y
        self.button_sprite_list.append(self.mode_button_sprite)

        self.restart_button_sprite = arcade.Sprite("Sprites/restart.png", scale=BUTTON_SIZE / 32)
        self.restart_button_sprite.center_x = self.restart_button_x
        self.restart_button_sprite.center_y = self.restart_button_y
        self.button_sprite_list.append(self.restart_button_sprite)

    def set_bombs(self, click_x, click_y):
        bombs = 0
        while bombs < BOMBS_COUNT:
            x = randrange(FIELD_WIDTH)
            y = randrange(FIELD_HEIGHT)
            if (click_x - 1 <= x <= click_x + 1) and (click_y - 1 <= y <= click_y + 1):
                continue
            elif is_on_field(x, y) and not self.field[y][x].get_bombed():
                self.field[y][x].set_bomb()
                bombs += 1

    def check_bombs(self):
        for row in range(FIELD_HEIGHT):
            for col in range(FIELD_WIDTH):
                self.field[row][col].checking(self.field)

    def on_draw(self):
        self.clear()

        field_sprites = arcade.SpriteList()
        for row in range(FIELD_HEIGHT):
            for col in range(FIELD_WIDTH):
                field_sprites.append(self.field[row][col].print_square())

        field_sprites.draw()
        self.button_sprite_list.draw()

    def is_on_screen_field(self, x, y):
        if (self.field_x <= x <= self.field_x + self.field_screen_width) and (self.field_y <= y <= self.field_y + self.field_screen_height):
            return True
        else:
            return False

    @staticmethod
    def is_in_button(x, y, x1, width, y1, height):
        if (x1 <= x <= x1 + width) and (y1 <= y <= y1 + height):
            return True
        else:
            return False

    def check_win_condition(self):
        win = True
        for row in range(FIELD_HEIGHT):
            for col in range(FIELD_WIDTH):
                if not self.field[row][col].get_bombed() and not self.field[row][col].get_opened():
                    win = False
        return win

    def restart(self):
        global game_over

        self.field = []
        for row in range(FIELD_HEIGHT):
            self.field.append([])
            for col in range(FIELD_WIDTH):
                square = Square(row,
                                col,
                                self.field_x + (col * SQUARE_SIZE) + (SQUARE_SIZE / 2),
                                self.field_y + (row * SQUARE_SIZE) + (SQUARE_SIZE / 2))
                self.field[row].append(square)

        self.first_click = True
        game_over = False
        self.mode = True

        self.mode_button_sprite = arcade.Sprite(mode_button_sprites[True], scale=BUTTON_SIZE / 32)
        self.mode_button_sprite.center_x = self.mode_button_x
        self.mode_button_sprite.center_y = self.mode_button_y
        self.button_sprite_list[0] = self.mode_button_sprite

        self.restart_button_sprite = arcade.Sprite("Sprites/restart.png", scale=BUTTON_SIZE / 32)
        self.restart_button_sprite.center_x = self.restart_button_x
        self.restart_button_sprite.center_y = self.restart_button_y
        self.button_sprite_list[1] = self.restart_button_sprite

    def on_mouse_release(self, x, y, button, modifiers):
        if self.is_on_screen_field(x, y) and not game_over:
            click = [int((x - self.field_x) // SQUARE_SIZE), int((y - self.field_y) // SQUARE_SIZE)]
            if self.first_click and self.mode:
                self.set_bombs(click[0], click[1])
                self.check_bombs()
                self.field[click[1]][click[0]].open_square(self.field)
                self.first_click = False

            elif self.mode:
                self.field[click[1]][click[0]].open_square(self.field)

            else:
                self.field[click[1]][click[0]].set_flag()

        elif self.is_in_button(x, y, self.mode_button_x - (BUTTON_SIZE / 2), BUTTON_SIZE, self.mode_button_y - (BUTTON_SIZE / 2), BUTTON_SIZE):
            self.mode = not self.mode
            self.mode_button_sprite = arcade.Sprite(mode_button_sprites[self.mode], scale=BUTTON_SIZE / 32)
            self.mode_button_sprite.center_x = self.mode_button_x
            self.mode_button_sprite.center_y = self.mode_button_y
            self.button_sprite_list[0] = self.mode_button_sprite
            print(self.mode)

        elif self.is_in_button(x, y, self.restart_button_x - (BUTTON_SIZE / 2), BUTTON_SIZE, self.restart_button_y - (BUTTON_SIZE / 2), BUTTON_SIZE):
            self.restart()

        if flags_left == 0 and self.check_win_condition():
            self.restart_button_sprite = arcade.Sprite("Sprites/win.png", scale=BUTTON_SIZE / 32)
            self.restart_button_sprite.center_x = self.restart_button_x
            self.restart_button_sprite.center_y = self.restart_button_y
            self.button_sprite_list[1] = self.restart_button_sprite


my_game = Game()
arcade.run()
