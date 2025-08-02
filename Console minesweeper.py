from random import randrange


working = True

FIELD_WIDTH = 10
FIELD_HEIGHT = 10
BOMBS_COUNT = 10


def is_in_field(x, y):
    if (0 <= x < FIELD_WIDTH) and (0 <= y < FIELD_HEIGHT):
        return True
    else:
        return False


class Square:
    def __init__(self, row, col):
        self.opened = False
        self.flagged = False
        self.bombed = False
        self.number = 0
        self.row = row
        self.col = col

    def checking(self, field):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if is_in_field(self.col + dc, self.row + dr) and field[self.row + dr][self.col + dc].get_bombed():
                    self.number += 1

    def get_bombed(self):
        return self.bombed

    def set_bomb(self):
        self.bombed = True

    def get_opened(self):
        return self.opened

    def print_square(self, game_over):
        if game_over and self.bombed:
            if self.opened:
                print("# ", end="")
            else:
                print("* ", end="")
        elif self.flagged:
            print("! ", end="")
        elif self.opened:
            print(self.number, "", end="")
        else:
            print("= ", end="")

    def open_square(self, field):
        if self.flagged:
            self.flagged = False

        self.opened = True

        if self.bombed:
            return False

        elif self.number == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    if is_in_field(self.col + dc, self.row + dr) and not field[self.row + dr][self.col + dc].get_opened():
                        field[self.row + dr][self.col + dc].open_square(field)

        return True

    def set_flag(self, flags_left):
        if not self.opened:
            if self.flagged:
                flags_left += 1
            else:
                flags_left -= 1
            self.flagged = not self.flagged
        return flags_left


class Game:
    def __init__(self):
        self.field = []
        for row in range(FIELD_HEIGHT):
            self.field.append([])
            for col in range(FIELD_WIDTH):
                square = Square(row, col)
                self.field[row].append(square)

        self.game_over = False
        self.first_click = True
        self.flags_left = BOMBS_COUNT
        self.mode = "dig"

    def set_bombs(self, click_x, click_y):
        bombs = 0
        while bombs < BOMBS_COUNT:
            x = randrange(FIELD_WIDTH)
            y = randrange(FIELD_HEIGHT)
            if (click_x - 1 <= x <= click_x + 1) and (click_y - 1 <= y <= click_y + 1):
                continue
            elif is_in_field(x, y) and not self.field[y][x].get_bombed():
                self.field[y][x].set_bomb()
                bombs += 1

    def check_bombs(self):
        for row in range(FIELD_HEIGHT):
            for col in range(FIELD_WIDTH):
                self.field[row][col].checking(self.field)

    def print_field(self, flag=False):
        for row in range(FIELD_HEIGHT):
            for col in range(FIELD_WIDTH):
                self.field[row][col].print_square(flag)
            print()

    def do_click(self, work_flag):
        change_buffer = input("Выберите режим: ")
        self.mode = change_buffer

        click = input().split()
        click[0], click[1] = int(click[0]) - 1, FIELD_HEIGHT - int(click[1])
        if self.first_click and self.mode == "dig":
            self.set_bombs(int(click[0]), int(click[1]))
            self.check_bombs()
            work_flag = self.field[int(click[1])][int(click[0])].open_square(self.field)
            self.first_click = False
        elif self.mode == "dig":
            work_flag = self.field[int(click[1])][int(click[0])].open_square(self.field)
        else:
            self.flags_left = self.field[int(click[1])][int(click[0])].set_flag(self.flags_left)

        return work_flag


my_game = Game()
while working:
    my_game.print_field()
    working = my_game.do_click(working)
    if not working:
        print("GAME OVER")
        my_game.print_field(True)

        command = input("Введите r - для рестарта или q - для выхода: ")
        if command == "r":
            my_game = Game()
            working = True