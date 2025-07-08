# TODO: 1) создать игру морской бой используя class для создания борды и первого игрока,
#           а) будет всегда фиксированное кол-во кораблей по стандартным правилам и стандартные доски
#           б) создать отдельный метод для борды чтобы корабли используя рандом модуль расставлялись автоматически
#              после чего у игрока есть выбор или согласиться с такой расстановкой или перерандомить расстановку
#              до той которая ему была бы по вкусу
#       2) В начале игры также будет спрашиваться если игра будет  PvP или PvE, если ПвП используется 2 разных
#          объекта класса Player заранее созданного если же ПвЕ то будет использоваться класс Bot который будет
#          всегда доволен первой раскладкой кораблей, стрелять будет используя модуль рандом.
#        ДОПОЛНИТЕЛЬНО: полностью проштудировать логику игры и последовательность действий в игре для каждого
#                       действия такого как выстрел или проверка на попадание будут созданы методы внутри класса
#                       Board, все статусы будут фиксироваться в классе  Player / Bot  соответственно(пока точно не
#                       знаю какие статусы но что-то в голове есть )
#        + так как отсутствует графический дизайн после каждого выстрела должны прорисовываться:
#           а) в случае игры против бота оба поля свое и вражеское с отметками выстрелов твоих и врага
#           б) в случае игры против другого игрока только вражеское по которому он стреляет и для проверки твоего
#              собственного поля из интереса нужно будет написать специальную команду описанную в отдельном в методе
#              класса  Player
#                               ПОКА ЧТО ВСЕ К ЧЕМУ Я ДОДУМАЛСЯ
#        UPD: 1)    добавить статистику после-матчевую, процент меткости игрока/игроков, самый долго живучий корабль,
#             сколько каждым сделано было выстрелов, макс кол-во ходов подряд без промахов
#             2)    Доработать логику бота в случае попадания, чтобы следующий выстрел был в близ-лежащую точку ( 1 от
#             выстрела предыдущего)
#             3)    Т.к. корабли не могут по правилам стоять рядом друг с другом то соотвественно доработать логику
#             "рандомного" размещения которая должна проверять наличие корабля в радиусе 1 клетки и если он там есть,
#             автоматически сама рерандомить эту часть корабля на другую
#             4)    Также из пункта 3 выходит то что после потопления корабля на полях автоматически должны отмечатся
#             все поля в радиусе 1 клетки от потопленного т.к. по правилам так логически не может быть корабля

import random


BOARD_SIZE: int = 10
SHIPS: dict[str: int] = {
    "4_celled": 1,
    "3_celled": 2,
    "2_celled": 3,
    "1_celled": 4
}
VER_COL_ALIAS: dict[str: int] = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9
}

# Which methods should contain and what exactly implement in logic of a game class Board:
# 1) initialize the board <__init__> (10x10 board, on the start with "~" which says that they're blank)
# 2) String representation <__str__> (By calling it as a string represent visual concept of a current state of board
# 3)


class Ship:

    def __init__(self, coords: list[tuple[int, int]], ship_size: int, orientation: str) -> None:
        self.coords = coords
        self.size = ship_size
        self.orientation = orientation
        self.ship_status: list[bool] = [True] * ship_size

    def is_sunk(self) -> bool:
        return not any(self.ship_status)


class Board:

    # Initializing the board which will contain 10x10
    def __init__(self) -> None:
        self.board: list[list[str]] = [["~" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.ships: list[Ship] = []
        self.ships_placed: bool = False
        self.ship_sizes: list[int] = [1, 1, 2, 3, 4]

    def __str__(self) -> str:
        vertical_coord: str = "     A   B   C   D   E   F   G   H   I   J   "
        top_line: str = f"   ┌{"───┬" * (BOARD_SIZE-1)}───┐"
        bottom_line: str = f"   └{"───┴" * (BOARD_SIZE-1)}───┘"
        lines: list[str] = [vertical_coord, top_line]
        for y in range(BOARD_SIZE):
            row: str = f"{y+1:>2} │"
            for x in range(BOARD_SIZE):
                row += f" {self.board[y][x]} │"
            lines.append(row)
            if y < BOARD_SIZE - 1:
                lines.append(f"   ├{"───┼" * (BOARD_SIZE - 1)}───┤")
            else:
                lines.append(bottom_line)
        return "\n".join(lines)

    @staticmethod
    def get_surrounding_cells(coords: list[tuple[int, int]]) -> list[tuple[int, int]]:
        cells_around: list[tuple[int, int]] = []
        for x, y in coords:
            for i in range(x-1, x+2):
                if 0 <= i < BOARD_SIZE:
                    for z in range(y-1, y+2):
                        if 0 <= z < BOARD_SIZE:
                            if (i == x) and (z == y):
                                continue
                            cells_around.append((i, z))
        return list(set(cells_around))

    def can_be_placed(self, coords: list[tuple[int, int]]) -> bool:
        if any(self.board[x][y] == "■" for x, y in coords):
            return False
        cells_around = self.get_surrounding_cells(coords)
        return all(self.board[x][y] == "~" for x, y in cells_around)

    def place_the_ship(self, ship_size: int) -> None:
        while True:
            if (orientation := random.choice(["V", "H"])) == "V":
                x = random.randint(0, 10 - ship_size)
                y = random.randint(0,9)
                coords: list[tuple[int, int]] = [(x + i, y) for i in range(ship_size)]
            else:    # orientation == "H":
                x = random.randint(0, 9)
                y = random.randint(0, 10 - ship_size)
                coords: list[tuple[int, int]] = [(x, y + i) for i in range(ship_size)]

            if self.can_be_placed(coords):
                for x, y in coords:
                    self.board[x][y] = "■"
                self.ships.append(Ship(coords, ship_size, orientation))
                break

    def place_all_ships(self, ships_sizes: list[int]):
        for ship_size in ships_sizes:
            self.place_the_ship(ship_size)
        self.ships_placed = True

    # TODO: clear_the_board method should be able to reset the field to completely blank one
    #  and better (if it's possible now or later) add the logic that it can be called only before
    #  game start or after it's end(somebody won) not during the game to avoid bugs.
    #  This method will be used as a part of rearranging_ships method as a helping one

    def clear_the_board(self) -> None:
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                self.board[x][y] = "~"
        self.ships.clear()

    def rearrange_ships(self) -> None:
        if self.ships_placed:
            self.clear_the_board()
            self.place_all_ships(self.ship_sizes)
        else:
            print("There is nothing to rearrange, since ships was not place at least once!")


class Player:

    # TODO: 1) Init method just in case, still don't know for what :D (whose turn is it, ) +
    #               attribute to keep your own field and see enemy field
    #           2) method shoot, if hit(turn again) if sunk(turn again + reveal all near cells)
    #           2a) after each shoot the enemy_board should be returned
    #           3) method is hit() which will probably will affect Ship and Board logic
    #           4) method to show my state of my board
    #           5) method to show off statistic

    def __init__(self, mode: str) -> None:
        self.turn: bool = False
        self.my_board: Board = Board()
        self.opponent: Player | Bot = Player() if mode == "PvP" else Bot()
        self.opponent_board = self.opponent.my_board


        self.opponent: Player | Bot = Player() if mode == "PvP" else Bot()
        self.opponent_board = self.opponent.my_board


class Bot:

    def __init__(self) -> None:
        pass
# ship_x = Ship(3)
# ship_e = Ship(3)
# ship_q = Ship(2)
# ship_w = Ship(1)


test_list = [1, 1, 2, 3, 4]

x = Board()
x.place_all_ships(test_list)
print(x)
x.rearrange_ships()
print(x)
x.clear_the_board()
print(x)
# lst = [ship_x, ship_e, ship_w, ship_q]
# for elem in lst:
#     x.place_the_ship(elem)
