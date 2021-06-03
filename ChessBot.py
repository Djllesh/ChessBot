import telebot
from telebot import types
# "♔♕♗♘♙♖♚♛♝♞♟♜"
bot = telebot.TeleBot('1573096092:AAECVPMuLSFayxe79pjErfWTZ-1bNuw41jk')
games = {}

#----------Elijah devlog-----------------
#1. Renamed murkup_maker() to markup_maker()
#2. Replaced a lot of repeated lines in markup_maker() with a small for-loop
#3. Renamed the key "move" to "turn" and made it explicit to say, which turn is it now: whites' or blacks'
#4. Automized a creation of figures in new_board() function by creating set_figure() method
#5. 

class Figure:
    def __init__(self, fig):
        self.fig = fig
        self.is_moved = False


class Pawn(Figure):
    def __init__(self, fig):
        super().__init__(fig=fig)
        self.is_two_steps = False
        self.is_two_steps_r = False


class King(Figure):
    def __init__(self, fig):
        super().__init__(fig)
        self.is_attacked = False

    def set_is_attacked(self):
        if self.is_attacked:
            self.is_attacked = False
        else:
            self.is_attacked = True


class Bishop(Figure):
    def __init__(self, fig):
        super().__init__(fig=fig)
        self.possible_p_p = True
        self.possible_p_m = True
        self.possible_m_p = True
        self.possible_m_m = True


class Queen(Figure):
    def __init__(self, fig):
        super().__init__(fig=fig)
        self.possible_p_p = True
        self.possible_p_m = True
        self.possible_m_p = True
        self.possible_m_m = True
        self.possible_p_p1 = True
        self.possible_p_m1 = True
        self.possible_m_p1 = True
        self.possible_m_m1 = True

def set_figure(figure):
    #создает фигуру в зависимости от ее внешнего вида
    #возвращает объект Figure 
    if figure == "♔" or figure == "♚":
        return King(figure)
    elif figure == "♕" or figure == "♛":
        return Queen(figure)
    elif figure == "♗" or figure == "♝":
        return Bishop(figure)
    elif figure == "♖" or figure == "♜":
        return Bishop(figure)
    elif figure == "♘" or figure == "♞":
        return Figure(figure)


def new_board():
    #заполняет структуру games
    #создает новую доску
     
    desk = {
        "turn": "white",
        "touch": False,
        "moved": True,
        "touched": {"fig": None,
                    "pos": None},
        "board": {"extra": Figure(" ")},
        "pawn": False,
        "is_check": False
    }
    for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
        for p in ['1', '2', '3', '4', '5', '6', '7', '8']:
            if p == '2':
                desk["board"][i + p] = Pawn("♙")
            elif p == '7':
                desk["board"][i + p] = Pawn("♟")
            else:
                desk["board"][i+p] = Figure(" ")

    letter_array = ["a", "b", "c" ,"d", "e", "f", "g", "h"]
    iterator = 0
    for figure in "♖♘♗♕♔♗♘♖":
        desk["board"][letter_array[iterator] + str(1)] = set_figure(figure)
        iterator += 1

    iterator = 8
    for figure in "♜♞♝♛♚♝♞♜":
        desk["board"][letter_array[len(letter_array) - iterator] + str(8)] = set_figure(figure)
        iterator -= 1

    return desk


def markup_maker(message, pawn):
    #отрисовывает поле на каждый ход
    markup = types.InlineKeyboardMarkup(row_width=8)
    board = []
    for row in range(1, 9):
        board.append([])
        for cell in ["a" + str(row), "b" + str(row), "c" + str(row), "d" + str(row), "e" + str(row), "f" + str(row), "g" + str(row), "h" + str(row)]:
            board[row - 1].append(types.InlineKeyboardButton(games[message.chat.id]["board"][cell].fig, callback_data = cell))
        markup.row(board[row - 1][0], board[row - 1][1], board[row - 1][2], board[row - 1][3], board[row - 1][4], board[row - 1][5], board[row - 1][6], board[row - 1][7])
    if pawn:
        addr = []
        for button in "QKRB":
            addr.append(types.InlineKeyboardButton(button, callback_data=button))
        markup.row(addr[0], addr[1], addr[2],addr[3])  
        
    return markup


def move(pos: str, num, let):
    #проверяет, может ли фигура сдвинуться на какую-то клетку
    number = int(pos[1]) + num
    letter = chr(ord(pos[0]) + let)
    if 1 > int(number) or int(number) > 8 or 97 > ord(letter) or ord(letter) > 104:
        return "extra"
    return letter + str(number)


def possible_move(id, pos):
    #добавляет на поле кружочки, на которые можно походить
    if games[id]["board"][pos].fig == " " and pos != "extra":
        games[id]["board"][pos].fig = "○"
        games[id]["moved"] = True


def is_attacked(message, pos):
    return True


def take(message, pos, fig):
    #переставляет фигуры на поле в соответствии с ходом 
    positions = []
    return_set = []
    if fig.fig == "♙":
        positions = [move(pos, 1, 1), move(pos, 1, -1)]
    elif fig.fig == "♟":
        positions = [move(pos, -1, 1), move(pos, -1, -1)]
    elif fig.fig == "♝" or fig.fig == "♗":
        for i in range(1, 8):
            if fig.possible_m_p:
                if games[message.chat.id]["board"][move(pos, -i, i)].fig != "○":
                    fig.possible_m_p = False
                    positions.append(move(pos, -i, i))
            if fig.possible_p_p:
                if games[message.chat.id]["board"][move(pos, i, i)].fig != "○":
                    fig.possible_p_p = False
                    positions.append(move(pos, i, i))
            if fig.possible_m_m:
                if games[message.chat.id]["board"][move(pos, -i, -i)].fig != "○":
                    fig.possible_m_m = False
                    positions.append(move(pos, -i, -i))
            if fig.possible_p_m:
                if games[message.chat.id]["board"][move(pos, i, -i)].fig != "○":
                    fig.possible_p_m = False
                    positions.append(move(pos, i, -i))
        fig.possible_p_m = True
        fig.possible_p_p = True
        fig.possible_m_m = True
        fig.possible_m_p = True
    elif fig.fig == "♖" or fig.fig == "♜" :
        for i in range(1, 8):
            if fig.possible_m_p:
                if games[message.chat.id]["board"][move(pos, 0, i)].fig != "○":
                    fig.possible_m_p = False
                    positions.append(move(pos, 0, i))
            if fig.possible_p_p:
                if games[message.chat.id]["board"][move(pos, 0, -i)].fig != "○":
                    fig.possible_p_p = False
                    positions.append(move(pos, 0, -i))
            if fig.possible_m_m:
                if games[message.chat.id]["board"][move(pos, i, 0)].fig != "○":
                    fig.possible_m_m = False
                    positions.append(move(pos, i, 0))
            if fig.possible_p_m:
                if games[message.chat.id]["board"][move(pos, -i, 0)].fig != "○":
                    fig.possible_p_m = False
                    positions.append(move(pos, -i, 0))
        fig.possible_p_m = True
        fig.possible_p_p = True
        fig.possible_m_m = True
        fig.possible_m_p = True
    elif fig.fig == "♘" or fig.fig == "♞":
            positions.append(move(pos, 2, -1))
            positions.append(move(pos, 2, 1))
            positions.append(move(pos, -2, -1))
            positions.append(move(pos, -2, 1))
            positions.append(move(pos, 1, -2))
            positions.append(move(pos, 1, 2))
            positions.append(move(pos, -1, -2))
            positions.append(move(pos, -1, 2))
    elif fig.fig == "♕" or fig.fig == "♛":
        for i in range(1, 8):
            if fig.possible_m_p:
                if games[message.chat.id]["board"][move(pos, 0, i)].fig != "○":
                    fig.possible_m_p = False
                    positions.append(move(pos, 0, i))
            if fig.possible_p_p:
                if games[message.chat.id]["board"][move(pos, 0, -i)].fig != "○":
                    fig.possible_p_p = False
                    positions.append(move(pos, 0, -i))
            if fig.possible_m_m:
                if games[message.chat.id]["board"][move(pos, i, 0)].fig != "○":
                    fig.possible_m_m = False
                    positions.append(move(pos, i, 0))
            if fig.possible_p_m:
                if games[message.chat.id]["board"][move(pos, -i, 0)].fig != "○":
                    fig.possible_p_m = False
                    positions.append(move(pos, -i, 0))

            if fig.possible_m_p1:
                if games[message.chat.id]["board"][move(pos, -i, i)].fig != "○":
                    fig.possible_m_p1 = False
                    positions.append(move(pos, -i, i))
            if fig.possible_p_p1:
                if games[message.chat.id]["board"][move(pos, i, i)].fig != "○":
                    fig.possible_p_p1 = False
                    positions.append(move(pos, i, i))
            if fig.possible_m_m1:
                if games[message.chat.id]["board"][move(pos, -i, -i)].fig != "○":
                    fig.possible_m_m1 = False
                    positions.append(move(pos, -i, -i))
            if fig.possible_p_m1:
                if games[message.chat.id]["board"][move(pos, i, -i)].fig != "○":
                    fig.possible_p_m1 = False
                    positions.append(move(pos, i, -i))
        fig.possible_p_m = True
        fig.possible_p_p = True
        fig.possible_m_m = True
        fig.possible_m_m = True
        fig.possible_p_m1 = True
        fig.possible_p_p1 = True
        fig.possible_m_m1 = True
        fig.possible_m_p1 = True
    if fig.fig == "♚" or fig.fig == "♔":
        positions.append(move(pos, -1, 1))
        positions.append(move(pos, -1, -1))
        positions.append(move(pos, 1, -1))
        positions.append(move(pos, 1, 1))
        positions.append(move(pos, 0, 1))
        positions.append(move(pos, 0, -1))
        positions.append(move(pos, 1, 0))
        positions.append(move(pos, -1, 0))


    for i in positions:
        if games[message.chat.id]["turn"] == "white":
            if games[message.chat.id]["board"][i].fig in "♚♛♝♞♟♜":
                return_set.append(i)
        else:
            if games[message.chat.id]["board"][i].fig in "♔♕♗♘♙♖":
                return_set.append(i)
    return return_set


def touch(message, pos):
    #заполняет поля кружочками
    if games[message.chat.id]["pawn"]:
        # "♔♕♗♘♙♖♚♛♝♞♟♜"
        if pos == "Q" and games[message.chat.id]["turn"] == "white":
            games[message.chat.id]["board"][games[message.chat.id]["touched"]["pos"]] = set_figure("♛")
            games[message.chat.id]["pawn"] = False
            return True
        elif pos == "K" and  games[message.chat.id]["turn"] == "white":
            games[message.chat.id]["board"][games[message.chat.id]["touched"]["pos"]] = set_figure("♞")
            games[message.chat.id]["pawn"] = False
            return True
        elif pos == "B" and  games[message.chat.id]["turn"] == "white":
            games[message.chat.id]["board"][games[message.chat.id]["touched"]["pos"]] = set_figure("♝")
            games[message.chat.id]["pawn"] = False
            return True
        elif pos == "R" and  games[message.chat.id]["turn"] == "white":
            games[message.chat.id]["board"][games[message.chat.id]["touched"]["pos"]] = set_figure("♜")
            games[message.chat.id]["pawn"] = False
            return True
        if pos == "Q" and games[message.chat.id]["turn"] == "black":
            games[message.chat.id]["board"][games[message.chat.id]["touched"]["pos"]] = set_figure("♕")
            games[message.chat.id]["pawn"] = False
            return True
        elif pos == "K" and games[message.chat.id]["turn"] == "black":
            games[message.chat.id]["board"][games[message.chat.id]["touched"]["pos"]] = set_figure("♘")
            games[message.chat.id]["pawn"] = False
            return True
        elif pos == "B" and games[message.chat.id]["turn"] == "black":
            games[message.chat.id]["board"][games[message.chat.id]["touched"]["pos"]] = set_figure("♗")
            games[message.chat.id]["pawn"] = False
            return True
        elif pos == "R" and games[message.chat.id]["turn"] == "black":
            games[message.chat.id]["board"][games[message.chat.id]["touched"]["pos"]] = set_figure("♖")
            games[message.chat.id]["pawn"] = False
            return True
        else:
            return False

    fig = games[message.chat.id]["board"][pos]
    if games[message.chat.id]["touched"]["fig"] is not None:

        if games[message.chat.id]["touched"]["fig"].fig == "♙" and \
                not games[message.chat.id]["touched"]["fig"].is_moved and pos[1] == "4":
            if games[message.chat.id]["board"][move(pos, 0, 1)].fig == "♟":
                games[message.chat.id]["board"][move(pos, 0, 1)].is_two_steps = True
                games[message.chat.id]["board"][move(pos, 0, 1)].is_two_steps_r = True
            if games[message.chat.id]["board"][move(pos, 0, -1)].fig == "♟":
                games[message.chat.id]["board"][move(pos, 0, -1)].is_two_steps = True

        if games[message.chat.id]["touched"]["fig"].fig == "♟" and \
                not games[message.chat.id]["touched"]["fig"].is_moved and pos[1] == '5':
            if games[message.chat.id]["board"][move(pos, 0, 1)].fig == "♙":
                games[message.chat.id]["board"][move(pos, 0, 1)].is_two_steps = True
                games[message.chat.id]["board"][move(pos, 0, 1)].is_two_steps_r = True
            if games[message.chat.id]["board"][move(pos, 0, -1)].fig == "♙":
                games[message.chat.id]["board"][move(pos, 0, -1)].is_two_steps = True

        if fig.fig == "○":
            if games[message.chat.id]["touched"]["fig"].fig == "♙" and\
                    games[message.chat.id]["touched"]["pos"][0] != pos[0]:
                games[message.chat.id]["board"][move(pos, -1, 0)] = Figure(" ")
                games[message.chat.id]["touched"]["fig"].is_two_steps = False

            if games[message.chat.id]["touched"]["fig"].fig == "♟" and\
                    games[message.chat.id]["touched"]["pos"][0] != pos[0]:
                games[message.chat.id]["board"][move(pos, 1, 0)] = Figure(" ")
                games[message.chat.id]["touched"]["fig"].is_two_steps = False

            if games[message.chat.id]["touched"]["fig"].fig == "♔":
                if pos == "c1":
                    games[message.chat.id]["board"]["d1"] = games[message.chat.id]["board"]["a1"]
                    games[message.chat.id]["board"]["a1"] = Figure(" ")
                if pos == "g1":
                    games[message.chat.id]["board"]["f1"] = games[message.chat.id]["board"]["h1"]
                    games[message.chat.id]["board"]["h1"] = Figure(" ")

            if games[message.chat.id]["touched"]["fig"].fig == "♚":
                if pos == "c8":
                    games[message.chat.id]["board"]["d8"] = games[message.chat.id]["board"]["a8"]
                    games[message.chat.id]["board"]["a8"] = Figure(" ")
                if pos == "g8":
                    games[message.chat.id]["board"]["f8"] = games[message.chat.id]["board"]["h8"]
                    games[message.chat.id]["board"]["h8"] = Figure(" ")
            previous_turn = games[message.chat.id]["turn"]
            games[message.chat.id]["turn"] = ("black", "white")[previous_turn == "black"]
            games[message.chat.id]["board"][pos] = games[message.chat.id]["touched"]["fig"]
            games[message.chat.id]["board"][games[message.chat.id]["touched"]["pos"]] = Figure(" ")
            games[message.chat.id]["board"][pos].is_moved = True
        elif fig.fig == " ":
            pass

        elif pos == games[message.chat.id]["touched"]["pos"]:
            pass

        elif pos in take(message, games[message.chat.id]["touched"]["pos"], games[message.chat.id]["touched"]["fig"]):
            games[message.chat.id]["board"][games[message.chat.id]["touched"]["pos"]] = Figure(" ")
            games[message.chat.id]["board"][pos] = games[message.chat.id]["touched"]["fig"]
            previous_turn = games[message.chat.id]["turn"]
            games[message.chat.id]["turn"] = ("black", "white")[previous_turn == "black"]
            games[message.chat.id]["moved"] = True

        for i in games[message.chat.id]["board"]:#------------to redo loop----------
            if games[message.chat.id]["board"][i].fig == "○":
                games[message.chat.id]["board"][i].fig = " "
        games[message.chat.id]["touched"]["fig"] = None

        return True

    else:
        games[message.chat.id]["moved"] = False
        if fig.fig == "♙":
            if games[message.chat.id]["turn"] == "white":
                games[message.chat.id]["touched"]["pos"] = pos
                games[message.chat.id]["touched"]["fig"] = fig
                games[message.chat.id]["touch"] = True
                possible_move(message.chat.id, move(pos, 1, 0))
                if not fig.is_moved:
                    possible_move(message.chat.id, move(pos, 2, 0))
                if fig.is_two_steps:
                    if not fig.is_two_steps_r:
                        possible_move(message.chat.id, move(pos, 1, 1))
                    else:
                        possible_move(message.chat.id, move(pos, 1, -1))
                return True

        if fig.fig == "♟":
            if games[message.chat.id]["turn"] == "black":
                games[message.chat.id]["touched"]["pos"] = pos
                games[message.chat.id]["touched"]["fig"] = fig
                games[message.chat.id]["touch"] = True
                possible_move(message.chat.id, move(pos, -1, 0))
                if not fig.is_moved:
                    possible_move(message.chat.id, move(pos, -2, 0))
                if fig.is_two_steps:
                    if not fig.is_two_steps_r:
                        possible_move(message.chat.id, move(pos, -1, 1))
                    else:
                        possible_move(message.chat.id, move(pos, -1, -1))

                return True
        if fig.fig == "♔" and games[message.chat.id]["turn"] == "white":
            if not fig.is_moved:
                if (not games[message.chat.id]["board"]["a1"].is_moved) and\
                        games[message.chat.id]["board"]["b1"].fig == " " and\
                        games[message.chat.id]["board"]["c1"].fig == " " and\
                        games[message.chat.id]["board"]["d1"].fig == " " and\
                        is_attacked(message, "b1") and is_attacked(message, "a1") and\
                        is_attacked(message, "c1") and is_attacked(message, "d1") and is_attacked(message, "e1"):
                    possible_move(message.chat.id, move(pos, 0, -2))
                if (not games[message.chat.id]["board"]["h1"].is_moved) and\
                        games[message.chat.id]["board"]["g1"].fig == " " and\
                        games[message.chat.id]["board"]["f1"].fig == " " and\
                        is_attacked(message, "h1") and is_attacked(message, "g1") and\
                        is_attacked(message, "f1") and is_attacked(message, "e1"):
                    possible_move(message.chat.id, move(pos, 0, 2))
            games[message.chat.id]["touched"]["pos"] = pos
            games[message.chat.id]["touched"]["fig"] = fig
            games[message.chat.id]["touch"] = True
            possible_move(message.chat.id, move(pos, 1, -1))
            possible_move(message.chat.id, move(pos, 1, 1))
            possible_move(message.chat.id, move(pos, -1, -1))
            possible_move(message.chat.id, move(pos, -1, 1))
            possible_move(message.chat.id, move(pos, 0, -1))
            possible_move(message.chat.id, move(pos, 0, 1))
            possible_move(message.chat.id, move(pos, 1, 0))
            possible_move(message.chat.id, move(pos, -1, 0))
            return True

        if fig.fig == "♚" and games[message.chat.id]["turn"] == "black":
            if not fig.is_moved:
                if (not games[message.chat.id]["board"]["a8"].is_moved) and \
                        games[message.chat.id]["board"]["b8"].fig == " " and \
                        games[message.chat.id]["board"]["c8"].fig == " " and \
                        games[message.chat.id]["board"]["d8"].fig == " " and \
                        is_attacked(message, "b8") and is_attacked(message, "a8") and \
                        is_attacked(message, "c8") and is_attacked(message, "d8") and is_attacked(message, "e8"):
                    possible_move(message.chat.id, move(pos, 0, -2))
                if (not games[message.chat.id]["board"]["h8"].is_moved) and\
                        games[message.chat.id]["board"]["g8"].fig == " " and\
                        games[message.chat.id]["board"]["f8"].fig == " " and\
                        is_attacked(message, "h8") and is_attacked(message, "g8") and\
                        is_attacked(message, "f8") and is_attacked(message, "e8"):
                    possible_move(message.chat.id, move(pos, 0, 2))
            games[message.chat.id]["touched"]["pos"] = pos
            games[message.chat.id]["touched"]["fig"] = fig
            games[message.chat.id]["touch"] = True
            possible_move(message.chat.id, move(pos, 1, -1))
            possible_move(message.chat.id, move(pos, 1, 1))
            possible_move(message.chat.id, move(pos, -1, -1))
            possible_move(message.chat.id, move(pos, -1, 1))
            possible_move(message.chat.id, move(pos, 0, -1))
            possible_move(message.chat.id, move(pos, 0, 1))
            possible_move(message.chat.id, move(pos, 1, 0))
            possible_move(message.chat.id, move(pos, -1, 0))
            return True

        if (fig.fig == "♗" and games[message.chat.id]["turn"] == "white") or\
                (fig.fig == "♝"and games[message.chat.id]["turn"] == "black"):
            games[message.chat.id]["touched"]["pos"] = pos
            games[message.chat.id]["touched"]["fig"] = fig
            games[message.chat.id]["touch"] = True
            for i in range(1, 8):
                if fig.possible_m_p:
                    if games[message.chat.id]["board"][move(pos, -i, i)].fig != " ":
                        fig.possible_m_p = False
                    possible_move(message.chat.id, move(pos, -i, i))
                if fig.possible_p_p:
                    if games[message.chat.id]["board"][move(pos, i, i)].fig != " ":
                        fig.possible_p_p = False
                    possible_move(message.chat.id, move(pos, i, i))
                if fig.possible_m_m:
                    if games[message.chat.id]["board"][move(pos, -i, -i)].fig != " ":
                        fig.possible_m_m = False
                    possible_move(message.chat.id, move(pos, -i, -i))
                if fig.possible_p_m:
                    if games[message.chat.id]["board"][move(pos, i, -i)].fig != " ":
                        fig.possible_p_m = False
                    possible_move(message.chat.id, move(pos, i, -i))
            fig.possible_p_m = True
            fig.possible_p_p = True
            fig.possible_m_m = True
            fig.possible_m_p = True
            return True
        if (fig.fig == "♘" and games[message.chat.id]["turn"] == "white") or \
                (fig.fig == "♞" and games[message.chat.id]["turn"] == "black"):
            games[message.chat.id]["touched"]["pos"] = pos
            games[message.chat.id]["touched"]["fig"] = fig
            games[message.chat.id]["touch"] = True
            possible_move(message.chat.id, move(pos, 2, -1))
            possible_move(message.chat.id, move(pos, 2, 1))
            possible_move(message.chat.id, move(pos, -2, -1))
            possible_move(message.chat.id, move(pos, -2, 1))
            possible_move(message.chat.id, move(pos, 1, -2))
            possible_move(message.chat.id, move(pos, 1, 2))
            possible_move(message.chat.id, move(pos, -1, -2))
            possible_move(message.chat.id, move(pos, -1, 2))
            return True
        if (fig.fig == "♖" and games[message.chat.id]["turn"] == "white") or \
                (fig.fig == "♜" and games[message.chat.id]["turn"] == "black"):
            games[message.chat.id]["touched"]["pos"] = pos
            games[message.chat.id]["touched"]["fig"] = fig
            games[message.chat.id]["touch"] = True
            for i in range(1, 8):
                if fig.possible_m_p:
                    if games[message.chat.id]["board"][move(pos, 0, i)].fig != " ":
                        fig.possible_m_p = False
                    possible_move(message.chat.id, move(pos, 0, i))
                if fig.possible_p_p:
                    if games[message.chat.id]["board"][move(pos, 0, -i)].fig != " ":
                        fig.possible_p_p = False
                    possible_move(message.chat.id, move(pos, 0, -i))
                if fig.possible_m_m:
                    if games[message.chat.id]["board"][move(pos, i, 0)].fig != " ":
                        fig.possible_m_m = False
                    possible_move(message.chat.id, move(pos, i, 0))
                if fig.possible_p_m:
                    if games[message.chat.id]["board"][move(pos, -i, 0)].fig != " ":
                        fig.possible_p_m = False
                    possible_move(message.chat.id, move(pos, -i, 0))
            fig.possible_p_m = True
            fig.possible_p_p = True
            fig.possible_m_m = True
            fig.possible_m_p = True
            return True
        if (fig.fig == "♕" and games[message.chat.id]["turn"] == "white") or \
                (fig.fig == "♛" and games[message.chat.id]["turn"] == "black"):
            games[message.chat.id]["touched"]["pos"] = pos
            games[message.chat.id]["touched"]["fig"] = fig
            games[message.chat.id]["touch"] = True
            for i in range(1, 8):
                if fig.possible_m_p:
                    if games[message.chat.id]["board"][move(pos, 0, i)].fig != " ":
                        fig.possible_m_p = False
                    possible_move(message.chat.id, move(pos, 0, i))
                if fig.possible_p_p:
                    if games[message.chat.id]["board"][move(pos, 0, -i)].fig != " ":
                        fig.possible_p_p = False
                    possible_move(message.chat.id, move(pos, 0, -i))
                if fig.possible_m_m:
                    if games[message.chat.id]["board"][move(pos, i, 0)].fig != " ":
                        fig.possible_m_m = False
                    possible_move(message.chat.id, move(pos, i, 0))
                if fig.possible_p_m:
                    if games[message.chat.id]["board"][move(pos, -i, 0)].fig != " ":
                        fig.possible_p_m = False
                    possible_move(message.chat.id, move(pos, -i, 0))

                if fig.possible_m_p1:
                    if games[message.chat.id]["board"][move(pos, -i, i)].fig != " ":
                        fig.possible_m_p1 = False
                    possible_move(message.chat.id, move(pos, -i, i))
                if fig.possible_p_p1:
                    if games[message.chat.id]["board"][move(pos, i, i)].fig != " ":
                        fig.possible_p_p1 = False
                    possible_move(message.chat.id, move(pos, i, i))
                if fig.possible_m_m1:
                    if games[message.chat.id]["board"][move(pos, -i, -i)].fig != " ":
                        fig.possible_m_m1 = False
                    possible_move(message.chat.id, move(pos, -i, -i))
                if fig.possible_p_m1:
                    if games[message.chat.id]["board"][move(pos, i, -i)].fig != " ":
                        fig.possible_p_m1 = False
                    possible_move(message.chat.id, move(pos, i, -i))
            fig.possible_p_m = True
            fig.possible_p_p = True
            fig.possible_m_m = True
            fig.possible_m_p = True
            fig.possible_p_m1 = True
            fig.possible_p_p1 = True
            fig.possible_m_m1 = True
            fig.possible_m_p1 = True
            return True

        if not games[message.chat.id]["moved"]:
            games[message.chat.id]["touch"] = False
            games[message.chat.id]["touched"]["fig"] = None
            games[message.chat.id]["touched"]["pos"] = None
            games[message.chat.id]["moved"] = True

    return False


@bot.message_handler(commands=['game'])
def game(message):
    games[message.chat.id] = new_board()
    markup_first = markup_maker(message, False)
    bot.send_message(message.chat.id, 'White move', reply_markup=markup_first)
    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if touch(message, call.data) and games[message.chat.id]["moved"]:
            for i in games[message.chat.id]["board"]:#----------to redo loop---------
                if i[1] == "1" and games[message.chat.id]["board"][i].fig == "♟":
                    games[message.chat.id]["pawn"] = True
                    games[message.chat.id]["touched"]["pos"] = i
                if i[1] == "8" and games[message.chat.id]["board"][i].fig == "♙":
                    games[message.chat.id]["pawn"] = True
                    games[message.chat.id]["touched"]["pos"] = i
            markup = markup_maker(message, games[message.chat.id]["pawn"])
            if games[message.chat.id]["turn"] == "white" and not games[message.chat.id]["is_check"]:
                txt = "White move"
            elif games[message.chat.id]["turn"] == "black" and not games[message.chat.id]["is_check"]:
                txt = "Black move"
            elif games[message.chat.id]["turn"] == "white" and games[message.chat.id]["is_check"]:
                txt = "CHECK! White move"
            elif games[message.chat.id]["turn"] == "black" and games[message.chat.id]["is_check"]:
                txt = "CHECK! Black move"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup,
                                  text=txt)


bot.polling()